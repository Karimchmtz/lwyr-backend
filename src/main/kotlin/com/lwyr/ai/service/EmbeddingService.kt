package com.lwyr.ai.service

import com.lwyr.ai.dto.embedding.EmbeddingRequest
import com.lwyr.ai.dto.embedding.EmbeddingResponse
import com.lwyr.ai.entity.Embedding
import com.lwyr.ai.repository.EmbeddingRepository
import com.lwyr.ai.repository.TrainedDocumentRepository
import mu.KotlinLogging
import org.springframework.stereotype.Service
import org.springframework.transaction.annotation.Transactional
import java.util.UUID

private val logger = KotlinLogging.logger(EmbeddingService::class.java.name)

@Service
class EmbeddingService(
    private val openRouterService: OpenRouterService,
    private val embeddingRepository: EmbeddingRepository,
    private val trainedDocumentRepository: TrainedDocumentRepository
) {

    fun generateEmbedding(request: EmbeddingRequest): EmbeddingResponse {
        logger.info { "Generating embedding for text (${request.text.length} chars)" }
        val embedding = openRouterService.generateEmbedding(request.text)
        logger.debug { "Embedding generated with ${embedding.size} dimensions" }
        return EmbeddingResponse(embedding, embedding.size)
    }

    @Transactional
    fun storeEmbeddings(
        trainedDocumentId: UUID,
        chunks: List<String>
    ): Int {
        logger.info { "Storing ${chunks.size} embeddings for document $trainedDocumentId" }

        val embeddings = openRouterService.generateEmbeddings(chunks)

        chunks.forEachIndexed { index, chunk ->
            val embedding = Embedding(
                id = UUID.randomUUID(),
                trainedDocumentId = trainedDocumentId,
                chunkIndex = index,
                content = chunk,
                embedding = embeddings[index],
                pageNumbers = null,
                metadata = mapOf("chunk_size" to chunk.length),
                createdAt = java.time.OffsetDateTime.now()
            )
            embeddingRepository.save(embedding)
        }

        trainedDocumentRepository.updateChunkCount(trainedDocumentId, chunks.size)

        logger.info { "Successfully stored ${chunks.size} embeddings" }
        return chunks.size
    }
}
