package com.lwyr.ai.repository

import com.lwyr.ai.entity.TrainedDocument
import org.springframework.jdbc.core.JdbcTemplate
import org.springframework.stereotype.Repository
import java.time.OffsetDateTime
import java.util.UUID

@Repository
class TrainedDocumentRepository(private val jdbcTemplate: JdbcTemplate) {

    fun findByFilename(name: String): TrainedDocument? {
        val rows = jdbcTemplate.queryForList(
            "SELECT id, filename, checksum, chunk_count, embedded_at FROM trained_documents WHERE filename = ?",
            name
        )

        return rows.firstOrNull()?.let { row ->
            TrainedDocument(
                id = UUID.fromString(row["id"] as String),
                filename = row["filename"] as String,
                checksum = row["checksum"] as String,
                chunkCount = (row["chunk_count"] as Number).toInt(),
                embeddedAt = OffsetDateTime.parse(row["embedded_at"] as String)
            )
        }
    }

    fun save(document: TrainedDocument): TrainedDocument {
        jdbcTemplate.update(
            """
            INSERT INTO trained_documents (id, filename, checksum, chunk_count, embedded_at)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT (filename) DO NOTHING
            """.trimIndent(),
            document.id,
            document.filename,
            document.checksum,
            document.chunkCount,
            document.embeddedAt
        )

        return document
    }

    fun updateChunkCount(idParam: UUID, newChunkCount: Int) {
        jdbcTemplate.update(
            "UPDATE trained_documents SET chunk_count = ? WHERE id = ?",
            newChunkCount,
            idParam
        )
    }

    fun findAll(): List<TrainedDocument> {
        val rows = jdbcTemplate.queryForList(
            "SELECT id, filename, checksum, chunk_count, embedded_at FROM trained_documents"
        )

        return rows.map { row ->
            TrainedDocument(
                id = UUID.fromString(row["id"] as String),
                filename = row["filename"] as String,
                checksum = row["checksum"] as String,
                chunkCount = (row["chunk_count"] as Number).toInt(),
                embeddedAt = OffsetDateTime.parse(row["embedded_at"] as String)
            )
        }
    }
}
