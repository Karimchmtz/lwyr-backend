package com.lwyr.ai.controller

import com.fasterxml.jackson.databind.ObjectMapper
import com.lwyr.ai.dto.auth.LoginRequest
import com.lwyr.ai.dto.auth.SignupRequest
import com.lwyr.ai.repository.UserRepository
import org.junit.jupiter.api.BeforeEach
import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Nested
import org.junit.jupiter.api.Test
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.http.MediaType
import org.springframework.test.context.ActiveProfiles
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.ResultActions
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.status
import org.testcontainers.junit.jupiter.Testcontainers
import kotlin.text.Charsets.UTF_8

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Testcontainers
class AuthControllerTest {

    @Autowired
    private lateinit var mockMvc: MockMvc

    @Autowired
    private lateinit var userRepository: UserRepository

    @Autowired
    private lateinit var objectMapper: ObjectMapper

    @BeforeEach
    fun setup() {
        userRepository.deleteAll()
    }

    private fun signupRequest(email: String = "test@example.com", password: String = "password123"): String {
        return objectMapper.writeValueAsString(SignupRequest(email, password))
    }

    private fun loginRequest(email: String = "test@example.com", password: String = "password123"): String {
        return objectMapper.writeValueAsString(LoginRequest(email, password))
    }

    @Nested
    @DisplayName("POST /auth/signup")
    inner class SignupTests {

        @Test
        @DisplayName("should return 201 when signup is successful")
        fun signupSuccess() {
            val request = signupRequest()

            performSignup(request)
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.userId").exists())
                .andExpect(jsonPath("$.email").value("test@example.com"))
                .andExpect(jsonPath("$.role").value("USER"))
        }

        @Test
        @DisplayName("should return 400 when email is empty")
        fun signupEmptyEmail() {
            val request = signupRequest(email = "")

            performSignup(request)
                .andExpect(status().isBadRequest())
        }

        @Test
        @DisplayName("should return 400 when email is invalid")
        fun signupInvalidEmail() {
            val request = signupRequest(email = "invalid-email")

            performSignup(request)
                .andExpect(status().isBadRequest())
        }

        @Test
        @DisplayName("should return 400 when password is less than 8 characters")
        fun signupShortPassword() {
            val request = signupRequest(password = "short")

            performSignup(request)
                .andExpect(status().isBadRequest())
        }

        @Test
        @DisplayName("should return 409 when email already exists")
        fun signupEmailAlreadyExists() {
            val request = signupRequest()

            performSignup(request)
            performSignup(request)
                .andExpect(status().isConflict())
        }

        private fun performSignup(request: String): ResultActions {
            return mockMvc.perform(
                post("/auth/signup")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(request.toByteArray(UTF_8))
            )
        }
    }

    @Nested
    @DisplayName("POST /auth/login")
    inner class LoginTests {

        @BeforeEach
        fun setup() {
            userRepository.deleteAll()
            val request = signupRequest()
            mockMvc.perform(
                post("/auth/signup")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(request.toByteArray(UTF_8))
            )
        }

        @Test
        @DisplayName("should return 200 when login is successful")
        fun loginSuccess() {
            val request = loginRequest()

            mockMvc.perform(
                post("/auth/login")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(request.toByteArray(UTF_8))
            )
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.userId").exists())
                .andExpect(jsonPath("$.email").value("test@example.com"))
                .andExpect(jsonPath("$.role").value("USER"))
        }

        @Test
        @DisplayName("should return 401 when user does not exist")
        fun loginUserNotFound() {
            val request = loginRequest(email = "nonexistent@example.com")

            mockMvc.perform(
                post("/auth/login")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(request.toByteArray(UTF_8))
            )
                .andExpect(status().isUnauthorized())
        }

        @Test
        @DisplayName("should return 401 when password is incorrect")
        fun loginWrongPassword() {
            val request = loginRequest(password = "wrongpassword")

            mockMvc.perform(
                post("/auth/login")
                    .contentType(MediaType.APPLICATION_JSON)
                    .content(request.toByteArray(UTF_8))
            )
                .andExpect(status().isUnauthorized())
        }
    }

    private fun post(path: String) = org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post(path)
}
