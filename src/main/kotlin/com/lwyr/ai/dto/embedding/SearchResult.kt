package com.lwyr.ai.dto.embedding

import java.util.UUID

data class SearchResult(
    val id: UUID,
    val content: String,
    val similarity: Double,
    val metadata: Map<String, Any>?
)
