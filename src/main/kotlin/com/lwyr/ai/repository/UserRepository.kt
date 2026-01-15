package com.lwyr.ai.repository

import com.lwyr.ai.entity.User
import com.lwyr.ai.entity.UserRole
import org.jooq.DSLContext
import org.jooq.Record
import org.jooq.impl.DSL.*
import org.springframework.stereotype.Repository
import java.time.OffsetDateTime
import java.util.UUID

@Repository
class UserRepository(private val dsl: DSLContext) {

    private val users = table("users")
    private val id = field("id", UUID::class.java)
    private val email = field("email", String::class.java)
    private val passwordHash = field("password_hash", String::class.java)
    private val role = field("role", String::class.java)
    private val createdAt = field("created_at", OffsetDateTime::class.java)
    private val updatedAt = field("updated_at", OffsetDateTime::class.java)

    private val allFields = arrayOf(id, email, passwordHash, role, createdAt, updatedAt)

    fun findById(userId: UUID): User? {
        return dsl.select(*allFields)
            .from(users)
            .where(id.eq(userId))
            .fetchOne(::mapToUser)
    }

    fun findByEmail(userEmail: String): User? {
        return dsl.select(*allFields)
            .from(users)
            .where(email.eq(userEmail))
            .fetchOne(::mapToUser)
    }

    fun existsByEmail(userEmail: String): Boolean {
        return dsl.fetchExists(
            dsl.selectOne()
                .from(users)
                .where(email.eq(userEmail))
        )
    }

    fun save(user: User): User {
        val now = OffsetDateTime.now()

        dsl.insertInto(users)
            .set(id, user.id)
            .set(email, user.email)
            .set(passwordHash, user.passwordHash)
            .set(role, user.role.name)
            .set(createdAt, user.createdAt)
            .set(updatedAt, now)
            .onConflict(id)
            .doUpdate()
            .set(email, user.email)
            .set(passwordHash, user.passwordHash)
            .set(role, user.role.name)
            .set(updatedAt, now)
            .execute()

        return user.copy(updatedAt = now)
    }

    fun findAll(): List<User> {
        return dsl.select(*allFields)
            .from(users)
            .fetch(::mapToUser)
    }

    fun deleteById(userId: UUID) {
        dsl.deleteFrom(users)
            .where(id.eq(userId))
            .execute()
    }

    fun deleteAll() {
        dsl.deleteFrom(users).execute()
    }

    private fun mapToUser(record: Record): User = User(
        id = record[id]!!,
        email = record[email]!!,
        passwordHash = record[passwordHash]!!,
        role = UserRole.valueOf(record[role]!!),
        createdAt = record[createdAt]!!,
        updatedAt = record[updatedAt]!!
    )
}
