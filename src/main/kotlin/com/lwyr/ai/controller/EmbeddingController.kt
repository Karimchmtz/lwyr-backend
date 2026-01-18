package com.lwyr.ai.controller

import com.lwyr.ai.dto.embedding.EmbeddingRequest
import com.lwyr.ai.dto.embedding.EmbeddingResponse
import com.lwyr.ai.service.EmbeddingService
import jakarta.validation.Valid
import mu.KotlinLogging
import org.springframework.http.ResponseEntity
import org.springframework.web.bind.annotation.*

private val logger = KotlinLogging.logger(EmbeddingController::class.java.name)

@RestController
@RequestMapping("/embeddings")
class EmbeddingController(
    private val embeddingService: EmbeddingService
) {

    @PostMapping
    fun generateEmbedding(@Valid @RequestBody request: EmbeddingRequest): ResponseEntity<EmbeddingResponse> {
        logger.info { "Embedding generation request received" }
        val response = embeddingService.generateEmbedding(request)
        return ResponseEntity.ok(response)
    }
}
