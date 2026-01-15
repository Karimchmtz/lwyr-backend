-- Enable pgvector extension for embeddings (optional)
-- This extension is only needed for RAG/embeddings functionality
DO $$ BEGIN
    CREATE EXTENSION IF NOT EXISTS vector;
EXCEPTION
    WHEN insufficient_privilege OR undefined_file THEN
        RAISE NOTICE 'pgvector extension not available, skipping';
    WHEN OTHERS THEN
        RAISE NOTICE 'Error creating vector extension: %', SQLERRM;
END $$;