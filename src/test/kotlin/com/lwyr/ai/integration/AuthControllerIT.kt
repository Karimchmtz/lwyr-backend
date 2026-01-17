package com.lwyr.ai.integration

import com.lwyr.ai.dto.auth.LoginRequest
import com.lwyr.ai.dto.auth.SignupRequest
import org.junit.jupiter.api.Test
import org.springframework.http.MediaType
import org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post
import org.springframework.test.web.servlet.result.MockMvcResultMatchers.*
import kotlin.text.Charsets.UTF_8

class AuthControllerIT : BaseIT() {

    private fun createSignupRequest(email: String = "test@example.com", password: String = "password123") =
        objectMapper.writeValueAsString(SignupRequest(email, password))

    private fun createLoginRequest(email: String = "test@example.com", password: String = "password123") =
        objectMapper.writeValueAsString(LoginRequest(email, password))

    private fun performSignup(request: String) = mockMvc.perform(
        post("/auth/signup").contentType(MediaType.APPLICATION_JSON).content(request.toByteArray(UTF_8))
    )

    private fun performLogin(request: String) = mockMvc.perform(
        post("/auth/login").contentType(MediaType.APPLICATION_JSON).content(request.toByteArray(UTF_8))
    )

    @Test
    fun testSignupSuccess() {
        val request = createSignupRequest()
        performSignup(request)
            .andExpect(status().isCreated)
            .andExpect(jsonPath("$.userId").exists())
            .andExpect(jsonPath("$.email").value("test@example.com"))
            .andExpect(jsonPath("$.role").value("USER"))
    }

    @Test
    fun testSignupEmptyEmail() {
        val request = createSignupRequest(email = "")
        performSignup(request).andExpect(status().isBadRequest)
    }

    @Test
    fun testSignupInvalidEmail() {
        val request = createSignupRequest(email = "invalid")
        performSignup(request).andExpect(status().isBadRequest)
    }

    @Test
    fun testSignupShortPassword() {
        val request = createSignupRequest(password = "short")
        performSignup(request).andExpect(status().isBadRequest)
    }

    @Test
    fun testSignupEmailAlreadyExists() {
        val request = createSignupRequest()
        performSignup(request)
        performSignup(request).andExpect(status().isConflict)
    }

    @Test
    fun testLoginSuccess() {
        val signupRequest = createSignupRequest()
        performSignup(signupRequest)  // Setup user
        val loginRequest = createLoginRequest()
        performLogin(loginRequest)
            .andExpect(status().isOk)
            .andExpect(jsonPath("$.userId").exists())
            .andExpect(jsonPath("$.email").value("test@example.com"))
            .andExpect(jsonPath("$.role").value("USER"))
    }

    @Test
    fun testLoginUserNotFound() {
        val request = createLoginRequest(email = "unknown@example.com")
        performLogin(request).andExpect(status().isUnauthorized)
    }

    @Test
    fun testLoginWrongPassword() {
        val signupRequest = createSignupRequest()
        performSignup(signupRequest)  // Setup user
        val request = createLoginRequest(password = "wrong")
        performLogin(request).andExpect(status().isUnauthorized)
    }
}