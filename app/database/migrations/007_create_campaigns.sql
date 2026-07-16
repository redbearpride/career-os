-- Executive Career OS
-- Campaigns
-- Version 0.1

CREATE TABLE IF NOT EXISTS career.campaigns (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    candidate_id UUID NOT NULL,

    name VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'active',

    target_roles JSONB NOT NULL DEFAULT '[]'::JSONB,
    target_industries JSONB NOT NULL DEFAULT '[]'::JSONB,
    target_locations JSONB NOT NULL DEFAULT '[]'::JSONB,
    compensation_target JSONB NOT NULL DEFAULT '{}'::JSONB,
    search_strategy JSONB NOT NULL DEFAULT '{}'::JSONB,

    notes TEXT,

    started_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ended_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_campaigns_candidate
        FOREIGN KEY (candidate_id)
        REFERENCES candidates.profiles(id)
        ON DELETE CASCADE,

    CONSTRAINT campaigns_status_check
        CHECK (status IN ('active', 'paused', 'completed', 'archived')),

    CONSTRAINT campaigns_end_after_start_check
        CHECK (ended_at IS NULL OR ended_at >= started_at)

);

CREATE INDEX IF NOT EXISTS idx_campaigns_candidate_status
    ON career.campaigns (candidate_id, status);

DROP TRIGGER IF EXISTS campaigns_set_updated_at ON career.campaigns;
CREATE TRIGGER campaigns_set_updated_at
BEFORE UPDATE ON career.campaigns
FOR EACH ROW
EXECUTE FUNCTION career.set_updated_at();
