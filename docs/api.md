# Executive Career OS — API Contract

Version: 0.1

## Scope

This API exposes the first executable part of the Executive Search Workflow:

```text
Candidate → Campaign → Company → Opportunity
```

Vacancy import, AI analysis, application, and authentication are intentionally
outside this slice.

## Conventions

- Base path: `/v1`
- Payload format: JSON
- Identifiers: UUID
- Successful create: `201 Created`
- Missing related entity: `404 Not Found`
- Duplicate candidate email: `409 Conflict`
- Request validation failure: `422 Unprocessable Entity`

## Endpoints

| Method | Path | Purpose |
| --- | --- | --- |
| `POST` | `/v1/candidates` | Create the MVP candidate profile |
| `GET` | `/v1/candidates/{id}` | Read a candidate profile |
| `POST` | `/v1/campaigns` | Create a candidate's search campaign |
| `GET` | `/v1/campaigns/{id}` | Read a campaign |
| `POST` | `/v1/companies` | Create a company record |
| `GET` | `/v1/companies/{id}` | Read a company |
| `POST` | `/v1/opportunities` | Create the central hiring-process aggregate |
| `GET` | `/v1/opportunities/{id}` | Read an opportunity |

## Create Opportunity

`POST /v1/opportunities`

```json
{
  "campaign_id": "UUID",
  "company_id": "UUID",
  "role_title": "Chief Operating Officer",
  "status": "discovered",
  "priority": 1,
  "discovery_source": "recruiter"
}
```

`campaign_id` and `company_id` must exist. Opportunity status is constrained to
the lifecycle approved in ADR-002.
