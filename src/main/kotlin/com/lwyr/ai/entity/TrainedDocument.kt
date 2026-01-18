package com.lwyr.ai.entity

import java.time.OffsetDateTime
import java.util.UUID

data class TrainedDocument(
    val id: UUID,
    val filename: String,
    val checksum: String,
    val chunkCount: Int,
    val embeddedAt: OffsetDateTime
)
