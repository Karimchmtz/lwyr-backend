package com.lwyr.ai.repository

import com.lwyr.ai.entity.Embedding
import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.stereotype.Repository
import org.springframework.transaction.annotation.Transactional
import java.time.OffsetDateTime
import java.util.UUID

@Repository
class EmbeddingRepository(private val jdbcTemplate: JdbcTemplate) {

    fun save(embedding: Embedding) {
        val vectorString = embedding.embedding.joinToString(",")
        jdbcTemplate.update(
            """
            INSERT INTO embeddings (id, trained_document_id, chunk_index, content, embedding, metadata, created_at)
            VALUES (?, ?, ?, ?, ?::vector, ?, ?)
            """.trimIndent(),
            embedding.id,
            embedding.trainedDocumentId,
            embedding.chunkIndex,
            embedding.content,
            vectorString,
            embedding.metadata?.toString(),
            embedding.createdAt
        )
    }

    fun findByTrainedDocumentId(documentId: UUID): List<Embedding> {
        val rows = jdbcTemplate.queryForList(
            """
            SELECT id, trained_document_id, chunk_index, content, 
                   embedding::text as embedding_text, 
                   metadata, created_at
            FROM embeddings
            WHERE trained_document_id = ?
            ORDER BY chunk_index ASC
            """.trimIndent(),
            documentId
        )

        return rows.map { row ->
            parseEmbeddingRow(row)
        }
    }

    fun deleteByTrainedDocumentId(documentId: UUID) {
        jdbcTemplate.update(
            "DELETE FROM embeddings WHERE trained_document_id = ?",
            documentId
        )
    }

    private fun parseEmbeddingRow(row: Map<String, Any>): Embedding {
        val id = UUID.fromString(row["id"] as String)
        val trainedDocumentId = UUID.fromString(row["trained_document_id"] as String)
        val chunkIndex = (row["chunk_index"] as Number).toInt()
        val content = row["content"] as String
        val metadataStr = row["metadata"] as String?
        val metadata = if (metadataStr != null && metadataStr != "null") {
            try {
                val json = org.json.JSONObject(metadataStr)
                mutableMapOf<String, Any>().apply {
                    for (key in json.keys()) {
                        put(key, json.get(key))
                    }
                }
            } catch (e: Exception) {
                null
            }
        } else {
            null
        }
        val embeddingText = row["embedding_text"] as String
        val embedding = parseVectorText(embeddingText)

        return Embedding(
            id = id,
            trainedDocumentId = trainedDocumentId,
            chunkIndex = chunkIndex,
            content = content,
            embedding = embedding,
            pageNumbers = null,
            metadata = metadata,
            createdAt = OffsetDateTime.parse(row["created_at"] as String)
        )
    }

    private fun parseVectorText(text: String): FloatArray {
        val cleanText = text.removeSurrounding("[", "]")
        return if (cleanText.isBlank()) {
            FloatArray(0)
        } else {
            cleanText.split(",").map { it.trim().toFloat() }.toFloatArray()
        }
    }
}
