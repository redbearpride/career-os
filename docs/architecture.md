# Executive Career OS

## Architecture

Version: 1.0

---

# Mission

Executive Career OS is an AI-powered Executive Career Copilot.

The primary objective of the system is not storing resumes.

The primary objective is helping an executive receive the strongest possible job offer through intelligent decision support and workflow automation.

---

# Product Philosophy

The system is designed around real executive career workflows.

Every feature must answer one question:

"Does it increase the probability of receiving a better offer?"

If not, it does not belong in MVP.

---

# Architecture Principles

1. Domain Driven Design (DDD)

2. Modular Architecture

3. AI First

4. API First

5. Automation First

6. Human in Control

---

# Core Business Object

The central business object is not Candidate.

The central business object is Opportunity.

Opportunity represents one real possibility of obtaining a position inside a company.

Everything related to this opportunity is grouped together.

## Core Relationship

```text
Candidate
    ↓
Campaign
    ↓
Opportunity
    ├── Company
    ├── Vacancy (one or more sources or versions)
    ├── Recruiter
    ├── AI Analysis
    └── Application Flow
```

---

# High-Level Structure

Campaign

↓

Opportunity

↓

Application Flow

---

# Domains

Candidate Domain

Opportunity Domain

Company Domain

Recruiter Domain

AI Domain

Automation Domain

Analytics Domain

---

# MVP Goal

Build the smallest possible system capable of helping one executive successfully find a new position.

The MVP is the first module of the future Executive Career OS platform.

---

# Development Principles

The project is developed using iterative vertical slices.

Every sprint must produce a working business capability.

Development order:

1. Architecture
2. Database
3. API
4. Business Logic
5. Automation
6. User Interface

Nothing is implemented without architectural justification.

Every completed step must be verified before moving to the next one.

---

# Architecture Decisions

## ADR-001

Title:
Opportunity is the central business entity.

Status:
Accepted

Decision:

The system is centered around Opportunity rather than Candidate or Vacancy.

Opportunity represents one complete hiring process inside one company.

Every business artifact belongs to one Opportunity.

Reason:

Executives manage opportunities, not resumes.

One opportunity may include:

- several vacancies;
- multiple recruiters;
- several interviews;
- multiple resume versions;
- negotiation;
- offer.

Consequences:

The system remains stable even if the vacancy changes during the hiring process.

This architecture better reflects executive hiring workflows.

---

## ADR-002

Title:
Campaign owns the search context; Opportunity owns the hiring process.

Status:
Accepted

Decision:

- A Campaign is a bounded job-search initiative for one Candidate. It stores the
  search strategy, targets, period, and status.
- An Opportunity belongs to exactly one Campaign and represents one hiring
  process at one Company.
- A Company may have multiple Opportunities within a Campaign when they are
  distinct hiring processes.
- A Vacancy is not a core aggregate. It is an imported job posting or a version
  of a position and belongs to one Opportunity.
- An Opportunity may contain zero or more Vacancies, which allows the process
  to continue when a posting is replaced, closed, or never published.

Opportunity lifecycle for MVP:

```text
discovered → qualifying → pursuing → applied → interviewing → offer → negotiating → accepted
                                      ↘ rejected
any non-terminal state → archived
```

Reason:

Campaign separates a Candidate's search strategy from individual employer
processes. Opportunity remains stable when the vacancy, recruiter, or application
materials change.

Consequences:

- The first opportunity vertical slice requires Campaign, Company, Opportunity,
  and Vacancy data models.
- Vacancy import starts only after an Opportunity exists; the import enriches an
  existing hiring process rather than creating the aggregate itself.
- Application, interview, offer, and negotiation records will be attached to
  Opportunity in later slices.
