package com.lwyr.ai.service

import com.github.tomakehurst.wiremock.client.WireMock
import com.github.tomakehurst.wiremock.junit5.WireMockTest
import com.lwyr.ai.exception.OpenRouterBadRequestException
import com.lwyr.ai.exception.OpenRouterRateLimitException
import com.lwyr.ai.exception.OpenRouterServerException
import com.lwyr.ai.exception.OpenRouterUnauthorizedException
import dev.langchain4j.model.openai.OpenAiEmbeddingModel
import org.assertj.core.api.Assertions.assertThat
import org.junit.jupiter.api.Test
import org.junit.jupiter.api.extension.ExtendWith
import org.mockito.junit.jupiter.MockitoExtension
import org.springframework.beans.factory.annotation.Autowired
import org.springframework.boot.test.context.SpringBootTest
import org.springframework.test.context.TestPropertySource

@WireMockTest(httpPort = 8081)
@SpringBootTest
@TestPropertySource(
    properties = [
        "openrouter.api-key=test-api-key",
        "openrouter.base-url=http://localhost:8081/v1",
        "openrouter.embedding-model=qwen/qwen3-embedding-0.6b"
    ]
)
class OpenRouterServiceTest {

    @Autowired
    private lateinit var openRouterService: OpenRouterService

    @Test
    fun `generate embedding successfully`() {
        WireMock.stubFor(
            WireMock.post(WireMock.urlPathEqualTo("/v1/embeddings"))
                .willReturn(
                    WireMock.okJson("""{
                        "object": "list",
                        "data": [{
                            "embedding": ${generate8192DimEmbedding()},
                            "index": 0
                        }],
                        "model": "qwen/qwen3-embedding-0.6b",
                        "usage": {
                            "prompt_tokens": 5,
                            "total_tokens": 5
                        }
                    }""")
                )
        )

        val embedding = openRouterService.generateEmbedding("test text")

        assertThat(embedding).hasSize(8192)
        assertThat(embedding[0]).isEqualTo(0.1f)
    }

    @Test
    fun `throw OpenRouterBadRequestException on 400 error`() {
        WireMock.stubFor(
            WireMock.post(WireMock.urlPathEqualTo("/v1/embeddings"))
                .willReturn(
                    WireMock.badRequest()
                        .withBody("""{"status":400,"error": {"message": "Invalid request"}}""")
                )
        )

        org.junit.jupiter.api.assertThrows<OpenRouterBadRequestException> {
            openRouterService.generateEmbedding("test text")
        }
    }

    @Test
    fun `throw OpenRouterUnauthorizedException on 401 error`() {
        WireMock.stubFor(
            WireMock.post(WireMock.urlPathEqualTo("/v1/embeddings"))
                .willReturn(
                    WireMock.unauthorized()
                        .withBody("""{"status":401,"error": {"message": "Invalid API key"}}""")
                )
        )

        org.junit.jupiter.api.assertThrows<OpenRouterUnauthorizedException> {
            openRouterService.generateEmbedding("test text")
        }
    }

    @Test
    fun `throw OpenRouterRateLimitException on 429 error`() {
        WireMock.stubFor(
            WireMock.post(WireMock.urlPathEqualTo("/v1/embeddings"))
                .willReturn(
                    WireMock.aResponse()
                        .withStatus(429)
                        .withBody("""{"status":429,"error": {"message": "Rate limit exceeded"}}""")
                )
        )

        org.junit.jupiter.api.assertThrows<OpenRouterRateLimitException> {
            openRouterService.generateEmbedding("test text")
        }
    }

    @Test
    fun `throw OpenRouterServerException on 500 error`() {
        WireMock.stubFor(
            WireMock.post(WireMock.urlPathEqualTo("/v1/embeddings"))
                .willReturn(
                    WireMock.serverError()
                        .withBody("""{"status":500,"error": {"message": "Internal server error"}}""")
                )
        )

        org.junit.jupiter.api.assertThrows<OpenRouterServerException> {
            openRouterService.generateEmbedding("test text")
        }
    }

    @Test
    fun `throw OpenRouterServerException on 502 error`() {
        WireMock.stubFor(
            WireMock.post(WireMock.urlPathEqualTo("/v1/embeddings"))
                .willReturn(
                    WireMock.aResponse()
                        .withStatus(502)
                        .withBody("""{"status":502,"error": {"message": "Bad gateway"}}""")
                )
        )

        org.junit.jupiter.api.assertThrows<OpenRouterServerException> {
            openRouterService.generateEmbedding("test text")
        }
    }

    private fun generate8192DimEmbedding(): String {
        val values = (1..8192).map { 0.1f }.joinToString(",")
        return "[$values]"
    }
}
