# Sprint 1 Plan

**Sprint Duration:** 2 weeks
**Sprint Start:** 2025-10-01
**Sprint End:** 2025-10-14

## Sprint Goal
Implement core authentication, BMI verification, and user profile management for the Personal Nutrition Assistant MVP.

## User Stories (from Technical Documentation)
- As an obese adult (BMI ≥ 30), I want to register securely with email and password, so that my health data is protected. (Must Have)
- As a user, I want to log in and recover my password via email, so that I can always access my account safely. (Must Have)
- As a user, I want to enter my height and weight, so that the system calculates my BMI and verifies my eligibility. (Must Have)

## Tasks & Assignments
| Task ID | Description | Priority | Assignee | Role | Deadline |
|---------|-------------|----------|----------|------|----------|
| 1 | Set up Flask backend project structure | Must Have | Saad Alarifi | Dev | 2025-10-02 |
| 2 | Implement user registration endpoint (/api/register) | Must Have | Saad Alarifi | Dev | 2025-10-04 |
| 3 | Implement login endpoint (/api/login) | Must Have | Saad Alarifi | Dev | 2025-10-06 |
| 4 | Implement password reset endpoint (/api/forgot-password) | Must Have | Abdullah Alameeri | Dev | 2025-10-08 |
| 5 | Implement BMI calculation endpoint (/api/bmi) | Must Have | Abdullah Alameeri | Dev | 2025-10-10 |
| 6 | Set up PostgreSQL database and user table | Must Have | Saad Alarifi | Dev | 2025-10-03 |
| 7 | Write unit tests for authentication and BMI | Must Have | Ahmed Dawwari | QA | 2025-10-12 |
| 8 | Set up Git branching and PR workflow | Must Have | Ahmed Dawwari | SCM | 2025-10-02 |
| 9 | Document API endpoints and usage | Should Have | Abdullah Alameeri | Dev | 2025-10-13 |

## Notes
- All code must follow PEP8 and be documented.
- PRs require at least one code review before merge.
- QA to report bugs in /sprints/bug-tracker-sprint1.md
- Daily standup notes in /sprints/standup-sprint1.md

---

[Reference: Technical_Documentation.md](../Technical_Documentation.md)
