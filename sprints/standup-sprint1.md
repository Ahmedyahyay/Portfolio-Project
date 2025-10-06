# Sprint 1 Standup Log

### Day 1
**What I did yesterday:**
- Project setup: Initialized Git repo, set up Flask backend and React frontend boilerplate.
- Designed the PostgreSQL database schema for `users` and `meals` tables.
**What I'll do today:**
- Implement the `/api/register` endpoint with password hashing (bcrypt).
- Create the frontend `RegistrationForm` component.
**Blockers:**
- None.

### Day 2
**What I did yesterday:**
- Completed the registration endpoint and connected it to the frontend form.
- Wrote unit tests for user registration.
**What I'll do today:**
- Implement the `/api/login` endpoint with password verification.
- Implement session/token-based authentication.
**Blockers:**
- Deciding on JWT vs. session cookies for auth. Decided to go with JWT for statelessness.

### Day 3
**What I did yesterday:**
- Finished the login functionality, including JWT generation and validation.
- Built the frontend `LoginForm` component and state management for authentication.
**What I'll do today:**
- Start building the BMI calculation logic on the backend (`/api/bmi` endpoint).
- Create the `BMIInput` component on the frontend.
**Blockers:**
- None.

### Day 4
**What I did yesterday:**
- Completed the BMI endpoint and the frontend component.
- Implemented the BMI ≥ 30 eligibility gate on the front-end.
**What I'll do today:**
- Begin work on the `/api/meals` endpoint with basic filtering for common allergies (from dropdowns).
- Set up the initial `AllergyPreferenceSelector` component.
**Blockers:**
- Finding a good, free seed dataset for meals with allergen tags.

### Day 5
**What I did yesterday:**
- Completed the V1 of the meal recommendation endpoint and filtering logic.
- Integrated the frontend components to create the initial authenticated dashboard view.
**What I'll do today:**
- Conduct end-to-end testing of the registration-login-BMI-meal flow.
- Prepare for Sprint 1 review.
**Blockers:**
- None.

### Day 6
**What I did yesterday:**
- Completed initial end-to-end flow (register → login → BMI → meals).
- Connected to USDA API in a stubbed mode and documented env vars.
**What I'll do today:**
- Stabilize tests and fix flaky BMI message assertions.
- Prepare Sprint 1 demo and retrospective notes.
**Blockers:**
- None.

### Day 7
**What I did yesterday:**
- Finalized bug fixes for registration validation and meal filters.
- Wrote draft technical documentation and QA checklist.
**What I'll do today:**
- Sprint 1 review and planning Sprint 2.
**Blockers:**
- None.
