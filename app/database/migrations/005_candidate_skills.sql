-- Executive Career OS
-- Candidate Skills
-- Version 0.1


CREATE TABLE IF NOT EXISTS candidates.skills (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    candidate_id UUID NOT NULL,

    skill_name VARCHAR(255) NOT NULL,

    category VARCHAR(100),

    proficiency_level VARCHAR(100),

    years_experience INTEGER,

    evidence TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_skill_candidate
        FOREIGN KEY(candidate_id)
        REFERENCES candidates.profiles(id)
        ON DELETE CASCADE

);