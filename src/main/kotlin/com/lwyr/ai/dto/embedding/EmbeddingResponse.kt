package com.lwyr.ai.dto.embedding

data class EmbeddingResponse(
    val embedding: FloatArray,
    val dimension: Int
) {
    override fun equals(other: Any?): Boolean {
        if (this === other) return true
        if (other !is EmbeddingResponse) return false
        return embedding.contentEquals(other.embedding)
    }

    override fun hashCode(): Int {
        return embedding.contentHashCode()
    }
}
