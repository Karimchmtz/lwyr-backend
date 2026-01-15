package com.lwyr.ai.entity

import java.time.OffsetDateTime
import java.util.UUID

data class User(
    val id: UUID,
    val email: String,
    val passwordHash: String,
    val role: UserRole,
    val createdAt: OffsetDateTime,
    val updatedAt: OffsetDateTime
)

enum class UserRole {
    USER,
    ADMIN
}
