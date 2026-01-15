package com.lwyr.ai.integration.controller

import com.fasterxml.jackson.databind.ObjectMapper
import com.lwyr.ai.dto.auth.LoginRequest
import com.lwyr.ai.dto.auth.SignupRequest
import com.lwyr.ai.integration.BaseIntegrationTest
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.http.MediaType
import org.springframework.test.web.servlet.MockMvc
import org.springframework.test.web.servlet.ResultActions
import kotlin.text.Charsets.UTF_8

/**
 * Configuration class for AuthController integration tests.
 * Contains helper methods and test data factories.
 * This class should NOT contain any @Test methods.
 * Extend AuthControllerIT for actual tests.
 */
abstract class AuthControllerTestConfiguration : BaseIntegrationTest() {

    @Autowired
    protected lateinit var mockMvc: MockMvc

    @Autowired
    protected lateinit var objectMapper: ObjectMapper

    protected fun createSignupRequest(
        email: String = "test@example.com",
        password: String = "password123"
    ): String {
        return objectMapper.writeValueAsString(SignupRequest(email, password))
    }

    protected fun createLoginRequest(
        email: String = "test@example.com",
        password: String = "password123"
    ): String {
        return objectMapper.writeValueAsString(LoginRequest(email, password))
    }

    protected fun performSignup(request: String): ResultActions {
        return mockMvc.perform(
            org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post("/auth/signup")
                .contentType(MediaType.APPLICATION_JSON)
                .content(request.toByteArray(UTF_8))
        )
    }

    protected fun performLogin(request: String): ResultActions {
        return mockMvc.perform(
            org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post("/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(request.toByteArray(UTF_8))
        )
    }
}
