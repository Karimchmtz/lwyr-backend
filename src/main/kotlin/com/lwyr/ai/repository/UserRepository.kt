package com.lwyr.ai.repository

import com.lwyr.ai.entity.User
import com.lwyr.ai.entity.UserRole
import org.jooq.DSLContext
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

    fun findById(userId: UUID): User? {
        return dsl.select(id, email, passwordHash, role, createdAt, updatedAt)
            .from(users)
            .where(id.eq(userId))
            .fetchOne { record ->
                User(
                    id = record.get(id)!!,
                    email = record.get(email)!!,
                    passwordHash = record.get(passwordHash)!!,
                    role = UserRole.valueOf(record.get(role)!!),
                    createdAt = record.get(createdAt)!!,
                    updatedAt = record.get(updatedAt)!!
                )
            }
    }

    fun findByEmail(userEmail: String): User? {
        return dsl.select(id, email, passwordHash, role, createdAt, updatedAt)
            .from(users)
            .where(email.eq(userEmail))
            .fetchOne { record ->
                User(
                    id = record.get(id)!!,
                    email = record.get(email)!!,
                    passwordHash = record.get(passwordHash)!!,
                    role = UserRole.valueOf(record.get(role)!!),
                    createdAt = record.get(createdAt)!!,
                    updatedAt = record.get(updatedAt)!!
                )
            }
    }

    fun existsByEmail(userEmail: String): Boolean {
        return dsl.fetchExists(
            dsl.select(id)
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
        return dsl.select(id, email, passwordHash, role, createdAt, updatedAt)
            .from(users)
            .fetch { record ->
                User(
                    id = record.get(id)!!,
                    email = record.get(email)!!,
                    passwordHash = record.get(passwordHash)!!,
                    role = UserRole.valueOf(record.get(role)!!),
                    createdAt = record.get(createdAt)!!,
                    updatedAt = record.get(updatedAt)!!
                )
            }
    }

    fun deleteById(userId: UUID) {
        dsl.deleteFrom(users)
            .where(id.eq(userId))
            .execute()
    }

    fun deleteAll() {
        dsl.deleteFrom(users).execute()
    }
}
