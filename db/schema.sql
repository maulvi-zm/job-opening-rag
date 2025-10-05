CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Enable pgvector extension for RAG embeddings (if using vector search)
-- CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================
-- Table: jobs
-- Stores all job opening information
-- ============================================
CREATE TABLE jobs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    job_title VARCHAR(255) NOT NULL,
    company_name VARCHAR(255),
    location VARCHAR(255) NOT NULL,
    job_description TEXT NOT NULL,
    requirements TEXT NOT NULL,
    gender_preference VARCHAR(20) DEFAULT 'any', -- 'male', 'female', 'any'
    minimum_age INTEGER,
    maximum_age INTEGER,
    minimum_experience_months INTEGER DEFAULT 0,
    salary_range VARCHAR(100),
    job_type VARCHAR(50) DEFAULT 'full-time', -- 'full-time', 'part-time', 'contract'
    employment_status VARCHAR(20) DEFAULT 'permanent', -- 'permanent', 'temporary'
    education_level VARCHAR(100),
    skills_required TEXT[], -- PostgreSQL array for multiple skills
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'inactive', 'closed'
    openings_count INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    -- Uncomment below if using pgvector for RAG
    -- embedding vector(1536) -- For RAG with OpenAI embeddings, adjust dimension as needed
);

-- Indexes for jobs table
CREATE INDEX idx_jobs_status ON jobs(status);
CREATE INDEX idx_jobs_location ON jobs(location);
CREATE INDEX idx_jobs_created_at ON jobs(created_at DESC);
CREATE INDEX idx_jobs_job_title ON jobs(job_title);

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_jobs_updated_at BEFORE UPDATE ON jobs
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Table: user_sessions
-- Tracks user conversation sessions
-- ============================================
CREATE TABLE user_sessions (
    session_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    phone_number VARCHAR(20) NOT NULL,
    current_state VARCHAR(50) DEFAULT 'initial', -- e.g., 'initial', 'searching', 'viewing_job'
    conversation_context JSONB, -- Store current conversation state/variables
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_activity_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(20) DEFAULT 'active', -- 'active', 'expired', 'completed'
    expires_at TIMESTAMP
);

-- Indexes for user_sessions table
CREATE INDEX idx_sessions_phone ON user_sessions(phone_number);
CREATE INDEX idx_sessions_status ON user_sessions(status);
CREATE INDEX idx_sessions_expires_at ON user_sessions(expires_at);
CREATE INDEX idx_sessions_last_activity ON user_sessions(last_activity_at DESC);

-- ============================================
-- Table: conversations
-- Stores all chat messages
-- ============================================
CREATE TABLE conversations (
    id BIGSERIAL PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL,
    session_id UUID NOT NULL REFERENCES user_sessions(session_id) ON DELETE CASCADE,
    message_text TEXT NOT NULL,
    message_type VARCHAR(10) NOT NULL, -- 'user' or 'bot'
    intent VARCHAR(100), -- e.g., 'search_job', 'view_details', 'greeting'
    related_job_id UUID REFERENCES jobs(id) ON DELETE SET NULL,
    metadata JSONB, -- Store additional context (e.g., recognized entities, confidence scores)
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for conversations table
CREATE INDEX idx_conversations_phone ON conversations(phone_number);
CREATE INDEX idx_conversations_session ON conversations(session_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at DESC);
CREATE INDEX idx_conversations_phone_created ON conversations(phone_number, created_at DESC);

-- ============================================
-- Table: job_interactions
-- Tracks user viewing interactions with jobs
-- ============================================
CREATE TABLE job_interactions (
    id BIGSERIAL PRIMARY KEY,
    phone_number VARCHAR(20) NOT NULL,
    job_id UUID NOT NULL REFERENCES jobs(id) ON DELETE CASCADE,
    interaction_type VARCHAR(50) NOT NULL, -- 'viewed'
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT valid_interaction_type CHECK (interaction_type IN ('viewed', 'interested'))
);

-- Indexes for job_interactions table
CREATE INDEX idx_interactions_phone ON job_interactions(phone_number);
CREATE INDEX idx_interactions_job ON job_interactions(job_id);
CREATE INDEX idx_interactions_type ON job_interactions(interaction_type);
CREATE INDEX idx_interactions_phone_job ON job_interactions(phone_number, job_id);

-- ============================================
-- Comments for documentation
-- ============================================
COMMENT ON TABLE jobs IS 'Stores all job opening information for the RAG system';
COMMENT ON TABLE user_sessions IS 'Tracks active user conversation sessions identified by phone number';
COMMENT ON TABLE conversations IS 'Stores all chat message history between users and bot';
COMMENT ON TABLE job_interactions IS 'Tracks user interactions with job postings (viewed/interested only)';

COMMENT ON COLUMN jobs.gender_preference IS 'Gender requirement: male, female, or any';
COMMENT ON COLUMN jobs.minimum_experience_months IS 'Minimum required experience in months';
COMMENT ON COLUMN jobs.skills_required IS 'Array of required skills';
COMMENT ON COLUMN user_sessions.conversation_context IS 'JSON object storing current state variables and filters';
COMMENT ON COLUMN conversations.metadata IS 'JSON object storing NLP results, entities, confidence scores';
COMMENT ON COLUMN job_interactions.interaction_type IS 'Type of interaction: viewed or interested only';

