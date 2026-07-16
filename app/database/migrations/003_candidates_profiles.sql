-- Executive Career OS
-- Candidates Profile
-- Version 0.1


CREATE TABLE IF NOT EXISTS candidates.profiles (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    first_name VARCHAR(100),
    last_name VARCHAR(100),

    email VARCHAR(255) UNIQUE,

    phone VARCHAR(50),

    location VARCHAR(255),

    target_roles JSONB,

    target_industries JSONB,

    compensation_expectation JSONB,

    career_goals TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);