package com.lwyr.ai.controller

import com.lwyr.ai.repository.UserRepository
import org.jooq.DSLContext
import org.junit.jupiter.api.AfterEach
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.test.context.ActiveProfiles
import org.testcontainers.junit.jupiter.Testcontainers

@SpringBootTest
@AutoConfigureMockMvc
@ActiveProfiles("test")
@Testcontainers
abstract class DatabaseCleanupTest {

    @Autowired
    private lateinit var dsl: DSLContext

    @Autowired
    private lateinit var userRepository: UserRepository

    @AfterEach
    fun cleanupDatabase() {
        // Clear all user-created tables but preserve Flyway schema history
        userRepository.deleteAll()

        // Add cleanup for any other tables that might be created in future tests
        // For now, we only have the users table
    }
}