package com.lwyr.ai.entity

import java.time.OffsetDateTime
import java.util.UUID

data class Embedding(
    val id: UUID,
    val trainedDocumentId: UUID,
    val chunkIndex: Int,
    val content: String,
    val embedding: FloatArray,
    val pageNumbers: List<Int>?,
    val metadata: Map<String, Any>?,
    val createdAt: OffsetDateTime
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is Embedding) return false
        return embedding.contentEquals(other.embedding)
    }

    override fun hashCode(): Int {
        return embedding.contentHashCode()
    }
}
