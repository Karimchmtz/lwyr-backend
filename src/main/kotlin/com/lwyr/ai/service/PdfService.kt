package com.lwyr.ai.service

import dev.langchain4j.data.document.Document
import dev.langchain4j.data.document.DocumentSplitter
import dev.langchain4j.data.document.splitter.DocumentByCharacterSplitter
import dev.langchain4j.data.segment.TextSegment
import mu.KotlinLogging
import org.apache.pdfbox.Loader
import org.apache.pdfbox.pdmodel.PDDocument
import org.apache.pdfbox.text.PDFTextStripper
import org.springframework.beans.factory.annotation.Value
import org.springframework.stereotype.Service
import java.io.ByteArrayOutputStream
import java.io.InputStream
import java.security.MessageDigest

private val logger = KotlinLogging.logger(PdfService::class.java.name)

@Service
class PdfService(
    @Value("\${pdf.chunk-size:1000}")
    private val chunkSize: Int,

    @Value("\${pdf.chunk-overlap:200}")
    private val chunkOverlap: Int
) {

    private val documentSplitter: DocumentSplitter = DocumentByCharacterSplitter(
        chunkSize,
        chunkOverlap
    )

    fun extractText(inputStream: InputStream, filename: String): String {
        logger.info { "Extracting text from PDF: $filename" }
        val bytes = inputStream.readBytes()
        val pdfDocument: PDDocument = Loader.loadPDF(bytes)
        val text = pdfDocument.use { doc ->
            PDFTextStripper().getText(doc)
        }
        logger.info { "Extracted ${text.length} characters from PDF" }
        return text
    }

    fun chunkText(text: String, filename: String): List<TextSegment> {
        logger.info { "Chunking text from $filename into segments" }
        val document = Document.from(text)
        val segments = documentSplitter.split(document)
        logger.info { "Created ${segments.size} chunks from $filename" }
        return segments
    }

    fun calculateChecksum(inputStream: InputStream): String {
        val digest = MessageDigest.getInstance("SHA-256")
        val buffer = ByteArray(8192)
        var bytesRead: Int
        while (inputStream.read(buffer).also { bytesRead = it } != -1) {
            digest.update(buffer, 0, bytesRead)
        }
        return digest.digest().joinToString("") { "%02x".format(it) }
    }
}
