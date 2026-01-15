CREATE TABLE trained_documents (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    filename VARCHAR(255) NOT NULL,
    checksum VARCHAR(64) NOT NULL,
    embedded_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    chunk_count INTEGER DEFAULT 0
);