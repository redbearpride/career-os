# Executive Career OS — Database Model

Version: 0.2

## Purpose

Executive Career OS is an AI-powered career intelligence platform.

The database stores structured information about:
- candidates;
- professional experience;
- skills;
- career strategy;
- campaigns;
- opportunities;
- vacancies;
- companies;
- AI analysis;
- actions and decisions.

---

# Core Entities

## 1. Candidate Profile

Main digital profile of a person.

Stores:
- personal information;
- location;
- target positions;
- industries;
- compensation expectations;
- career goals;
- preferences.

---

## 2. Professional Experience

Stores career history.

Includes:
- company;
- position;
- period;
- responsibilities;
- achievements;
- measurable results.

---

## 3. Skills

Stores professional competencies.

Categories:
- management skills;
- industry expertise;
- technical skills;
- soft skills.

---

## 4. Campaign

A bounded job-search initiative for one candidate.

Includes:
- target roles;
- target industries;
- geography;
- compensation strategy;
- search period;
- campaign status.

Campaign is the parent context for all opportunities created during that search.

## 5. Opportunity

The central business entity. Represents one hiring process at one company inside
one campaign.

Includes:
- lifecycle status;
- source and discovery context;
- strategic priority;
- decision and archive reason;
- links to company, vacancies, recruiters, AI analyses, and application flow.

## 6. Company

Stores company intelligence shared by one or more opportunities.

Includes:
- company profile;
- business scale;
- market position;
- risks;
- management signals;
- culture indicators.

## 7. Vacancy

Stores an imported job posting or position version attached to an existing
opportunity. A vacancy is evidence and source data, not the hiring-process
aggregate.

Sources:
- HH;
- LinkedIn;
- recruiters;
- direct applications.


## 8. AI Analysis

AI-generated analysis of a vacancy, company, or opportunity.

Includes:
- match score;
- strengths;
- risks;
- hidden requirements;
- estimated compensation;
- motivation package;
- recommended actions.

---

## 9. Action Tracker

Tracks activities in an opportunity's application flow.

Examples:
- application;
- recruiter contact;
- interview;
- follow-up;
- decision.

---

# Core Relationships

```text
Candidate 1 ── * Campaign 1 ── * Opportunity * ── 1 Company
                                     │
                                     ├── * Vacancy
                                     ├── * Recruiter
                                     ├── * AI Analysis
                                     └── * Application Action
```

The first database vertical slice will introduce Campaign, Company, Opportunity,
and Vacancy in that dependency order. Existing candidate profile, experience, and
skills tables remain unchanged.
