-- Executive Career OS
-- Candidate Professional Experience
-- Version 0.1


CREATE TABLE IF NOT EXISTS candidates.experiences (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    candidate_id UUID NOT NULL,

    company_name VARCHAR(255) NOT NULL,

    position VARCHAR(255) NOT NULL,

    start_date DATE,

    end_date DATE,

    is_current BOOLEAN DEFAULT FALSE,

    responsibilities TEXT,

    achievements TEXT,

    metrics JSONB,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_candidate
        FOREIGN KEY(candidate_id)
        REFERENCES candidates.profiles(id)
        ON DELETE CASCADE

);