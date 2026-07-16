from typing import Any, Dict
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from psycopg import Connection
from psycopg.errors import ForeignKeyViolation, UniqueViolation
from psycopg.types.json import Json

from app.api.models import (
    CampaignCreate,
    CampaignResponse,
    CandidateCreate,
    CandidateResponse,
    CompanyCreate,
    CompanyResponse,
    OpportunityCreate,
    OpportunityResponse,
)
from app.database.connection import get_connection

router = APIRouter(prefix="/v1", tags=["Career search"])


def get_or_404(connection: Connection, query: str, entity_id: UUID, entity_name: str) -> Dict[str, Any]:
    with connection.cursor() as cursor:
        cursor.execute(query, {"id": entity_id})
        row = cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name} not found.",
        )

    return row


def foreign_key_error(error: ForeignKeyViolation) -> HTTPException:
    entity_by_constraint = {
        "fk_campaigns_candidate": "Candidate",
        "fk_opportunities_campaign": "Campaign",
        "fk_opportunities_company": "Company",
    }
    entity_name = entity_by_constraint.get(error.diag.constraint_name, "Related resource")
    return HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"{entity_name} not found.",
    )


@router.post(
    "/candidates",
    response_model=CandidateResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_candidate(
    payload: CandidateCreate,
    connection: Connection = Depends(get_connection),
) -> Dict[str, Any]:
    try:
        with connection.transaction():
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO candidates.profiles (
                        first_name, last_name, email, phone, location, target_roles,
                        target_industries, compensation_expectation, career_goals
                    )
                    VALUES (
                        %(first_name)s, %(last_name)s, %(email)s, %(phone)s, %(location)s,
                        %(target_roles)s, %(target_industries)s,
                        %(compensation_expectation)s, %(career_goals)s
                    )
                    RETURNING *
                    """,
                    {
                        "first_name": payload.first_name,
                        "last_name": payload.last_name,
                        "email": payload.email,
                        "phone": payload.phone,
                        "location": payload.location,
                        "target_roles": Json(payload.target_roles),
                        "target_industries": Json(payload.target_industries),
                        "compensation_expectation": Json(payload.compensation_expectation),
                        "career_goals": payload.career_goals,
                    },
                )
                return cursor.fetchone()
    except UniqueViolation as error:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Candidate email already exists.",
        ) from error


@router.get("/candidates/{candidate_id}", response_model=CandidateResponse)
def get_candidate(
    candidate_id: UUID,
    connection: Connection = Depends(get_connection),
) -> Dict[str, Any]:
    return get_or_404(
        connection,
        "SELECT * FROM candidates.profiles WHERE id = %(id)s",
        candidate_id,
        "Candidate",
    )


@router.post(
    "/campaigns",
    response_model=CampaignResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_campaign(
    payload: CampaignCreate,
    connection: Connection = Depends(get_connection),
) -> Dict[str, Any]:
    try:
        with connection.transaction():
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO career.campaigns (
                        candidate_id, name, status, target_roles, target_industries,
                        target_locations, compensation_target, search_strategy, notes
                    )
                    VALUES (
                        %(candidate_id)s, %(name)s, %(status)s, %(target_roles)s,
                        %(target_industries)s, %(target_locations)s,
                        %(compensation_target)s, %(search_strategy)s, %(notes)s
                    )
                    RETURNING *
                    """,
                    {
                        "candidate_id": payload.candidate_id,
                        "name": payload.name,
                        "status": payload.status.value,
                        "target_roles": Json(payload.target_roles),
                        "target_industries": Json(payload.target_industries),
                        "target_locations": Json(payload.target_locations),
                        "compensation_target": Json(payload.compensation_target),
                        "search_strategy": Json(payload.search_strategy),
                        "notes": payload.notes,
                    },
                )
                return cursor.fetchone()
    except ForeignKeyViolation as error:
        raise foreign_key_error(error) from error


@router.get("/campaigns/{campaign_id}", response_model=CampaignResponse)
def get_campaign(
    campaign_id: UUID,
    connection: Connection = Depends(get_connection),
) -> Dict[str, Any]:
    return get_or_404(
        connection,
        "SELECT * FROM career.campaigns WHERE id = %(id)s",
        campaign_id,
        "Campaign",
    )


@router.post(
    "/companies",
    response_model=CompanyResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_company(
    payload: CompanyCreate,
    connection: Connection = Depends(get_connection),
) -> Dict[str, Any]:
    with connection.transaction():
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO companies.companies (
                    name, website, linkedin_url, headquarters, industry, company_size,
                    external_ids, company_profile
                )
                VALUES (
                    %(name)s, %(website)s, %(linkedin_url)s, %(headquarters)s,
                    %(industry)s, %(company_size)s, %(external_ids)s, %(company_profile)s
                )
                RETURNING *
                """,
                {
                    "name": payload.name,
                    "website": payload.website,
                    "linkedin_url": payload.linkedin_url,
                    "headquarters": payload.headquarters,
                    "industry": payload.industry,
                    "company_size": payload.company_size,
                    "external_ids": Json(payload.external_ids),
                    "company_profile": Json(payload.company_profile),
                },
            )
            return cursor.fetchone()


@router.get("/companies/{company_id}", response_model=CompanyResponse)
def get_company(
    company_id: UUID,
    connection: Connection = Depends(get_connection),
) -> Dict[str, Any]:
    return get_or_404(
        connection,
        "SELECT * FROM companies.companies WHERE id = %(id)s",
        company_id,
        "Company",
    )


@router.post(
    "/opportunities",
    response_model=OpportunityResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_opportunity(
    payload: OpportunityCreate,
    connection: Connection = Depends(get_connection),
) -> Dict[str, Any]:
    try:
        with connection.transaction():
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO career.opportunities (
                        campaign_id, company_id, role_title, status, priority,
                        discovery_source, decision_reason, archived_reason, notes
                    )
                    VALUES (
                        %(campaign_id)s, %(company_id)s, %(role_title)s, %(status)s,
                        %(priority)s, %(discovery_source)s, %(decision_reason)s,
                        %(archived_reason)s, %(notes)s
                    )
                    RETURNING *
                    """,
                    {
                        "campaign_id": payload.campaign_id,
                        "company_id": payload.company_id,
                        "role_title": payload.role_title,
                        "status": payload.status.value,
                        "priority": payload.priority,
                        "discovery_source": payload.discovery_source,
                        "decision_reason": payload.decision_reason,
                        "archived_reason": payload.archived_reason,
                        "notes": payload.notes,
                    },
                )
                return cursor.fetchone()
    except ForeignKeyViolation as error:
        raise foreign_key_error(error) from error


@router.get("/opportunities/{opportunity_id}", response_model=OpportunityResponse)
def get_opportunity(
    opportunity_id: UUID,
    connection: Connection = Depends(get_connection),
) -> Dict[str, Any]:
    return get_or_404(
        connection,
        "SELECT * FROM career.opportunities WHERE id = %(id)s",
        opportunity_id,
        "Opportunity",
    )
