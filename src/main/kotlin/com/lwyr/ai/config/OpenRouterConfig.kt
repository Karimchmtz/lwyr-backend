package com.lwyr.ai.config

import dev.langchain4j.model.openai.OpenAiChatModel
import dev.langchain4j.model.openai.OpenAiEmbeddingModel
import org.springframework.beans.factory.annotation.Value
import org.springframework.boot.context.properties.ConfigurationProperties
import org.springframework.context.annotation.Bean
import org.springframework.context.annotation.Configuration

@Configuration
@ConfigurationProperties(prefix = "openrouter")
class OpenRouterConfig {

    var apiKey: String = ""

    var baseUrl: String = "https://openrouter.ai/api/v1"

    var chatModel: String = "qwen/qwen3-0.6b:free"

    var embeddingModel: String = "qwen/qwen3-embedding-0.6b"

    var temperature: Double = 0.7

    var maxTokens: Int = 2000

    @Bean
    fun embeddingModel(): OpenAiEmbeddingModel {
        return OpenAiEmbeddingModel.builder()
            .baseUrl(baseUrl)
            .apiKey(apiKey)
            .modelName(embeddingModel)
            .timeout(java.time.Duration.ofSeconds(60))
            .maxRetries(3)
            .build()
    }

    @Bean
    fun chatModel(): OpenAiChatModel {
        return OpenAiChatModel.builder()
            .baseUrl(baseUrl)
            .apiKey(apiKey)
            .modelName(chatModel)
            .temperature(temperature)
            .maxTokens(maxTokens)
            .timeout(java.time.Duration.ofSeconds(60))
            .maxRetries(3)
            .build()
    }
}
