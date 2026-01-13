package com.lwyr.ai.service

import com.lwyr.ai.dto.auth.LoginRequest
import com.lwyr.ai.dto.auth.SignupRequest
import com.lwyr.ai.entity.User
import com.lwyr.ai.entity.UserRole
import com.lwyr.ai.exception.AuthenticationException
import com.lwyr.ai.exception.ResourceAlreadyExistsException
import com.lwyr.ai.repository.UserRepository
import org.slf4j.LoggerFactory
import org.springframework.security.crypto.password.PasswordEncoder
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional

@Service
class AuthService(
    private val userRepository: UserRepository,
    private val passwordEncoder: PasswordEncoder
) {

    private val logger = LoggerFactory.getLogger(AuthService::class.java)

    @Transactional
    fun signup(request: SignupRequest): User {
        logger.info("Processing signup for email: {}", request.email)

        if (userRepository.existsByEmail(request.email)) {
            logger.warn("Signup failed - email already exists: {}", request.email)
            throw ResourceAlreadyExistsException("Email already registered")
        }

        val user = User(
            email = request.email,
            passwordHash = passwordEncoder.encode(request.password),
            role = UserRole.USER
        )

        val savedUser = userRepository.save(user)
        logger.info("User registered successfully: {}", savedUser.id)

        return savedUser
    }

    fun login(request: LoginRequest): User {
        logger.info("Processing login for email: {}", request.email)

        val user = userRepository.findByEmail(request.email)
            ?: run {
                logger.warn("Login failed - user not found: {}", request.email)
                throw AuthenticationException("Invalid email or password")
            }

        if (!passwordEncoder.matches(request.password, user.passwordHash)) {
            logger.warn("Login failed - invalid password for email: {}", request.email)
            throw AuthenticationException("Invalid email or password")
        }

        logger.info("Login successful for user: {}", user.id)
        return user
    }
}
