-- Executive Career OS
-- Opportunities
-- Version 0.1

CREATE TABLE IF NOT EXISTS career.opportunities (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    campaign_id UUID NOT NULL,
    company_id UUID NOT NULL,

    role_title VARCHAR(255) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT 'discovered',
    priority SMALLINT NOT NULL DEFAULT 3,
    discovery_source VARCHAR(100),

    decision_reason TEXT,
    archived_reason TEXT,
    notes TEXT,

    discovered_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    status_changed_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_opportunities_campaign
        FOREIGN KEY (campaign_id)
        REFERENCES career.campaigns(id)
        ON DELETE CASCADE,

    CONSTRAINT fk_opportunities_company
        FOREIGN KEY (company_id)
        REFERENCES companies.companies(id)
        ON DELETE RESTRICT,

    CONSTRAINT opportunities_status_check
        CHECK (
            status IN (
                'discovered',
                'qualifying',
                'pursuing',
                'applied',
                'interviewing',
                'offer',
                'negotiating',
                'accepted',
                'rejected',
                'archived'
            )
        ),

    CONSTRAINT opportunities_priority_check
        CHECK (priority BETWEEN 1 AND 5)

);

CREATE INDEX IF NOT EXISTS idx_opportunities_campaign_status
    ON career.opportunities (campaign_id, status);

CREATE INDEX IF NOT EXISTS idx_opportunities_company
    ON career.opportunities (company_id);

DROP TRIGGER IF EXISTS opportunities_set_updated_at ON career.opportunities;
CREATE TRIGGER opportunities_set_updated_at
BEFORE UPDATE ON career.opportunities
FOR EACH ROW
EXECUTE FUNCTION career.set_updated_at();
