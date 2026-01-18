package com.lwyr.ai.service

import com.lwyr.ai.exception.OpenRouterBadRequestException
import com.lwyr.ai.exception.OpenRouterRateLimitException
import com.lwyr.ai.exception.OpenRouterServerException
import com.lwyr.ai.exception.OpenRouterUnauthorizedException
import dev.langchain4j.data.segment.TextSegment
import dev.langchain4j.model.openai.OpenAiEmbeddingModel
import mu.KotlinLogging
import org.springframework.stereotype.Service

private val logger = KotlinLogging.logger(OpenRouterService::class.java.name)

@Service
class OpenRouterService(
    private val embeddingModel: OpenAiEmbeddingModel
) {

    fun generateEmbedding(text: String): FloatArray {
        return try {
            logger.debug { "Generating embedding for text (${text.length} chars)" }
            val response = embeddingModel.embed(text)
            response.content().vector().copyOf()
        } catch (e: Exception) {
            handleOpenRouterError(e)
        }
    }

    fun generateEmbeddings(texts: List<String>): List<FloatArray> {
        return try {
            logger.debug { "Generating embeddings for ${texts.size} texts" }
            val textSegments = texts.map { TextSegment.from(it) }
            val response = embeddingModel.embedAll(textSegments)
            response.content().map { it.vector().copyOf() }
        } catch (e: Exception) {
            handleOpenRouterError(e)
        }
    }

    private fun handleOpenRouterError(e: Exception): Nothing {
        logger.error(e) { "OpenRouter API error" }

        val message = e.message ?: "Unknown error occurred"
        val statusCode = extractStatusCode(message)
        val errorMessage = extractErrorMessage(message)

        when (statusCode) {
            400 -> throw OpenRouterBadRequestException(errorMessage)
            401 -> throw OpenRouterUnauthorizedException("Invalid API key or unauthorized access")
            429 -> throw OpenRouterRateLimitException("Rate limit exceeded, please try again later")
            500, 502, 503 -> throw OpenRouterServerException("OpenRouter service error: $errorMessage")
            else -> throw OpenRouterServerException(errorMessage)
        }
    }

    private fun extractStatusCode(message: String): Int {
        return try {
            when {
                message.contains("\"status\":400") || message.contains("400") -> 400
                message.contains("\"status\":401") || message.contains("401") -> 401
                message.contains("\"status\":429") || message.contains("429") -> 429
                message.contains("\"status\":500") || message.contains("500") -> 500
                message.contains("\"status\":502") || message.contains("502") -> 502
                message.contains("\"status\":503") || message.contains("503") -> 503
                message.contains("bad request", ignoreCase = true) -> 400
                message.contains("unauthorized", ignoreCase = true) -> 401
                message.contains("rate limit", ignoreCase = true) -> 429
                message.contains("internal server error", ignoreCase = true) -> 500
                else -> 500
            }
        } catch (e: Exception) {
            500
        }
    }

    private fun extractErrorMessage(message: String): String {
        return try {
            val jsonMatch = Regex(""""message"\s*:\s*"([^"]+)"""").find(message)
            jsonMatch?.groupValues?.get(1) ?: message
        } catch (e: Exception) {
            message
        }
    }
}
