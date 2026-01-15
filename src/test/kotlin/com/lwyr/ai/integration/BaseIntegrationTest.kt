package com.lwyr.ai.integration

import com.lwyr.ai.repository.UserRepository
import org.jooq.DSLContext
import org.junit.jupiter.api.AfterEach
import org.junit.jupiter.api.Tag
import org.junit.jupiter.api.extension.ExtendWith
import org.mockito.junit.jupiter.MockitoExtension
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.test.context.ActiveProfiles
import org.testcontainers.junit.jupiter.Testcontainers

/**
 * Base integration test class that provides common configuration and utilities.
 * All integration tests should extend this class.
 *
 * Naming Convention:
 * - Integration tests: *IT suffix (e.g., AuthControllerIT)
 * - Unit tests: *Test suffix (e.g., AuthControllerTest)
 */
@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Testcontainers
@Tag("integration")
@ExtendWith(MockitoExtension::class)
abstract class BaseIntegrationTest {

    @Autowired
    protected lateinit var dsl: DSLContext

    @Autowired
    protected lateinit var userRepository: UserRepository

    @AfterEach
    fun cleanupDatabase() {
        userRepository.deleteAll()
    }
}
