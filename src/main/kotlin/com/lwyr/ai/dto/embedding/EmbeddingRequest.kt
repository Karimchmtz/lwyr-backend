package com.lwyr.ai.dto.embedding

import jakarta.validation.constraints.NotBlank

data class EmbeddingRequest(
    @field:NotBlank(message = "Text is required")
    val text: String
)
