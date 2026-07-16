-- Executive Career OS
-- Companies
-- Version 0.1

CREATE TABLE IF NOT EXISTS companies.companies (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    name VARCHAR(255) NOT NULL,
    website TEXT,
    linkedin_url TEXT,
    headquarters VARCHAR(255),
    industry VARCHAR(255),
    company_size VARCHAR(100),

    external_ids JSONB NOT NULL DEFAULT '{}'::JSONB,
    company_profile JSONB NOT NULL DEFAULT '{}'::JSONB,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP

);

CREATE INDEX IF NOT EXISTS idx_companies_name_lower
    ON companies.companies (LOWER(name));

DROP TRIGGER IF EXISTS companies_set_updated_at ON companies.companies;
CREATE TRIGGER companies_set_updated_at
BEFORE UPDATE ON companies.companies
FOR EACH ROW
EXECUTE FUNCTION career.set_updated_at();
