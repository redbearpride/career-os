from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import UUID

from pydantic import BaseModel, Field


class CampaignStatus(str, Enum):
    active = "active"
    paused = "paused"
    completed = "completed"
    archived = "archived"


class OpportunityStatus(str, Enum):
    discovered = "discovered"
    qualifying = "qualifying"
    pursuing = "pursuing"
    applied = "applied"
    interviewing = "interviewing"
    offer = "offer"
    negotiating = "negotiating"
    accepted = "accepted"
    rejected = "rejected"
    archived = "archived"


class CandidateCreate(BaseModel):
    first_name: str = Field(min_length=1, max_length=100)
    last_name: str = Field(min_length=1, max_length=100)
    email: str = Field(min_length=3, max_length=255)
    phone: Optional[str] = Field(default=None, max_length=50)
    location: Optional[str] = Field(default=None, max_length=255)
    target_roles: List[str] = Field(default_factory=list)
    target_industries: List[str] = Field(default_factory=list)
    compensation_expectation: Dict[str, Any] = Field(default_factory=dict)
    career_goals: Optional[str] = None


class CandidateResponse(CandidateCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime


class CampaignCreate(BaseModel):
    candidate_id: UUID
    name: str = Field(min_length=1, max_length=255)
    status: CampaignStatus = CampaignStatus.active
    target_roles: List[str] = Field(default_factory=list)
    target_industries: List[str] = Field(default_factory=list)
    target_locations: List[str] = Field(default_factory=list)
    compensation_target: Dict[str, Any] = Field(default_factory=dict)
    search_strategy: Dict[str, Any] = Field(default_factory=dict)
    notes: Optional[str] = None


class CampaignResponse(CampaignCreate):
    started_at: datetime
    ended_at: Optional[datetime]
    id: UUID
    created_at: datetime
    updated_at: datetime


class CompanyCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    website: Optional[str] = None
    linkedin_url: Optional[str] = None
    headquarters: Optional[str] = Field(default=None, max_length=255)
    industry: Optional[str] = Field(default=None, max_length=255)
    company_size: Optional[str] = Field(default=None, max_length=100)
    external_ids: Dict[str, Any] = Field(default_factory=dict)
    company_profile: Dict[str, Any] = Field(default_factory=dict)


class CompanyResponse(CompanyCreate):
    id: UUID
    created_at: datetime
    updated_at: datetime


class OpportunityCreate(BaseModel):
    campaign_id: UUID
    company_id: UUID
    role_title: str = Field(min_length=1, max_length=255)
    status: OpportunityStatus = OpportunityStatus.discovered
    priority: int = Field(default=3, ge=1, le=5)
    discovery_source: Optional[str] = Field(default=None, max_length=100)
    decision_reason: Optional[str] = None
    archived_reason: Optional[str] = None
    notes: Optional[str] = None


class OpportunityResponse(OpportunityCreate):
    id: UUID
    discovered_at: datetime
    status_changed_at: datetime
    created_at: datetime
    updated_at: datetime
