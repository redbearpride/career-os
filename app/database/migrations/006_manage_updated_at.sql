-- Executive Career OS
-- Maintain updated_at timestamps
-- Version 0.1

CREATE OR REPLACE FUNCTION career.set_updated_at()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$;

DROP TRIGGER IF EXISTS candidates_profiles_set_updated_at ON candidates.profiles;
CREATE TRIGGER candidates_profiles_set_updated_at
BEFORE UPDATE ON candidates.profiles
FOR EACH ROW
EXECUTE FUNCTION career.set_updated_at();

DROP TRIGGER IF EXISTS candidate_experiences_set_updated_at ON candidates.experiences;
CREATE TRIGGER candidate_experiences_set_updated_at
BEFORE UPDATE ON candidates.experiences
FOR EACH ROW
EXECUTE FUNCTION career.set_updated_at();

DROP TRIGGER IF EXISTS candidate_skills_set_updated_at ON candidates.skills;
CREATE TRIGGER candidate_skills_set_updated_at
BEFORE UPDATE ON candidates.skills
FOR EACH ROW
EXECUTE FUNCTION career.set_updated_at();
