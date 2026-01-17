package com.lwyr.ai.integration

import com.fasterxml.jackson.databind.ObjectMapper
import com.lwyr.ai.repository.UserRepository
import org.jooq.DSLContext
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Tag
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.test.context.ActiveProfiles
import org.springframework.test.web.servlet.MockMvc
import org.testcontainers.junit.jupiter.Testcontainers

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Testcontainers
@Tag("integration")
abstract class BaseIT {

    @Autowired
    protected lateinit var mockMvc: MockMvc

    @Autowired
    protected lateinit var objectMapper: ObjectMapper

    @Autowired
    protected lateinit var dsl: DSLContext

    @Autowired
    protected lateinit var userRepository: UserRepository

    @AfterEach
    fun cleanup() {
        userRepository.deleteAll()  // Centralized DB reset
    }
}