-- Create embeddings table for storing PDF text chunks with vectors
CREATE TABLE IF NOT EXISTS embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    trained_document_id UUID NOT NULL REFERENCES trained_documents(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    content TEXT NOT NULL,
    embedding vector(8192) NOT NULL,
    page_numbers INTEGER[],
    metadata JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_chunk UNIQUE (trained_document_id, chunk_index)
);

-- Create index for foreign key lookups
CREATE INDEX IF NOT EXISTS idx_embeddings_trained_document_id ON embeddings(trained_document_id);

-- Note: Vector similarity indexes (ivfflat, hnsw) require pgvector 0.8.0+ and have dimension limits.
-- For 8192-dimensional Qwen embeddings, consider:
-- - Using a separate database optimized for vector search (Pinecone, Weaviate, etc.)
-- - Dimensionality reduction before storage
-- - Upgrading to pgvector with HNSW support (if available)
-- For small datasets, sequential scan will work adequately.

-- Add unique constraint to trained_documents filename if it doesn't exist
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM information_schema.table_constraints
        WHERE constraint_name = 'unique_filename'
        AND table_name = 'trained_documents'
    ) THEN
        ALTER TABLE trained_documents ADD CONSTRAINT unique_filename UNIQUE (filename);
    END IF;
END $$;
