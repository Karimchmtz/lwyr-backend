package com.lwyr.ai.integration.controller

import org.junit.jupiter.api.DisplayName
import org.junit.jupiter.api.Test
import org.springframework.http.MediaType
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.status
import kotlin.text.Charsets.UTF_8

/**
 * Integration tests for AuthController.
 * Uses *IT suffix to distinguish from unit tests.
 * Inherits global configuration from BaseIntegrationTest.
 */
class AuthControllerIT : AuthControllerTestConfiguration() {

    @Test
    @DisplayName("should return 201 when signup is successful")
    fun signupSuccess() {
        val request = createSignupRequest()

        performSignup(request)
            .andExpect(status().isCreated())
            .andExpect(jsonPath("$.userId").exists())
            .andExpect(jsonPath("$.email").value("test@example.com"))
            .andExpect(jsonPath("$.role").value("USER"))
    }

    @Test
    @DisplayName("should return 400 when email is empty")
    fun signupEmptyEmail() {
        val request = createSignupRequest(email = "")

        performSignup(request)
            .andExpect(status().isBadRequest())
    }

    @Test
    @DisplayName("should return 400 when email is invalid")
    fun signupInvalidEmail() {
        val request = createSignupRequest(email = "invalid-email")

        performSignup(request)
            .andExpect(status().isBadRequest())
    }

    @Test
    @DisplayName("should return 400 when password is less than 8 characters")
    fun signupShortPassword() {
        val request = createSignupRequest(password = "short")

        performSignup(request)
            .andExpect(status().isBadRequest())
    }

    @Test
    @DisplayName("should return 409 when email already exists")
    fun signupEmailAlreadyExists() {
        val request = createSignupRequest()

        performSignup(request)
        performSignup(request)
            .andExpect(status().isConflict())
    }

    @Test
    @DisplayName("should return 200 when login is successful")
    fun loginSuccess() {
        // Setup user for login test
        val signupRequest = createSignupRequest()
        mockMvc.perform(
            org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post("/auth/signup")
                .contentType(MediaType.APPLICATION_JSON)
                .content(signupRequest.toByteArray(UTF_8))
        )

        val request = createLoginRequest()

        performLogin(request)
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.userId").exists())
            .andExpect(jsonPath("$.email").value("test@example.com"))
            .andExpect(jsonPath("$.role").value("USER"))
    }

    @Test
    @DisplayName("should return 401 when user does not exist")
    fun loginUserNotFound() {
        val request = createLoginRequest(email = "nonexistent@example.com")

        performLogin(request)
            .andExpect(status().isUnauthorized())
    }

    @Test
    @DisplayName("should return 401 when password is incorrect")
    fun loginWrongPassword() {
        // Setup user for login test
        val signupRequest = createSignupRequest()
        mockMvc.perform(
            org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post("/auth/signup")
                .contentType(MediaType.APPLICATION_JSON)
                .content(signupRequest.toByteArray(UTF_8))
        )

        val request = createLoginRequest(password = "wrongpassword")

        performLogin(request)
            .andExpect(status().isUnauthorized())
    }
}
