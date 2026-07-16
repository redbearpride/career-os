-- Executive Career OS
-- Vacancies
-- Version 0.1

CREATE TABLE IF NOT EXISTS vacancies.vacancies (

    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),

    opportunity_id UUID NOT NULL,

    source VARCHAR(100) NOT NULL,
    external_id TEXT,
    source_url TEXT,

    title VARCHAR(255),
    description TEXT,
    employment_type VARCHAR(100),
    location VARCHAR(255),
    compensation JSONB NOT NULL DEFAULT '{}'::JSONB,
    raw_payload JSONB NOT NULL DEFAULT '{}'::JSONB,

    published_at TIMESTAMPTZ,
    imported_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_vacancies_opportunity
        FOREIGN KEY (opportunity_id)
        REFERENCES career.opportunities(id)
        ON DELETE CASCADE

);

CREATE INDEX IF NOT EXISTS idx_vacancies_opportunity_imported
    ON vacancies.vacancies (opportunity_id, imported_at DESC);

CREATE UNIQUE INDEX IF NOT EXISTS uq_vacancies_opportunity_source_external_id
    ON vacancies.vacancies (opportunity_id, source, external_id)
    WHERE external_id IS NOT NULL;

DROP TRIGGER IF EXISTS vacancies_set_updated_at ON vacancies.vacancies;
CREATE TRIGGER vacancies_set_updated_at
BEFORE UPDATE ON vacancies.vacancies
FOR EACH ROW
EXECUTE FUNCTION career.set_updated_at();
