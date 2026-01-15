package com.lwyr.ai.controller

import com.lwyr.ai.dto.auth.AuthResponse
import com.lwyr.ai.dto.auth.LoginRequest
import com.lwyr.ai.dto.auth.SignupRequest
import com.lwyr.ai.entity.User
import com.lwyr.ai.service.AuthService
import jakarta.validation.Valid
import mu.KotlinLogging
import org.springframework.http.HttpStatus
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.PostMapping
import org.springframework.web.bind.annotation.RequestBody
import org.springframework.web.bind.annotation.RequestMapping
import org.springframework.web.bind.annotation.RestController

private val logger = KotlinLogging.logger(AuthController::class.java.name)

@RestController
@RequestMapping("/auth")
class AuthController(
    private val authService: AuthService
) {

    @PostMapping("/signup")
    fun signup(@Valid @RequestBody request: SignupRequest): ResponseEntity<AuthResponse> {
        logger.info { "Signup request received for email: ${request.email}" }

        val user = authService.signup(request)
        val response = user.toAuthResponse()

        logger.info { "User registered successfully: ${user.id}" }
        return ResponseEntity.status(HttpStatus.CREATED).body(response)
    }

    @PostMapping("/login")
    fun login(@Valid @RequestBody request: LoginRequest): ResponseEntity<AuthResponse> {
        logger.info { "Login request received for email: ${request.email}" }

        val user = authService.login(request)
        val response = user.toAuthResponse()

        logger.info { "User logged in successfully: ${user.id}" }
        return ResponseEntity.ok(response)
    }

    private fun User.toAuthResponse() = AuthResponse(
        userId = id.toString(),
        email = email,
        role = role.name
    )
}
