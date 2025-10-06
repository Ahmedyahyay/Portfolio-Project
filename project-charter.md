# Project Charter – Personal Nutrition Assistant

## Vision
Empower users to make healthier choices through personalized, safe, and accessible nutrition guidance.

## Objectives (SMART)
- Launch MVP within 6 weeks with secure auth, BMI, and meal suggestions.
- Achieve <300ms average API latency for core endpoints.
- Ensure 100% of recommended meals respect user allergies and BMI rules.

## Scope (MVP)
- User registration/login with first/last name.
- BMI calculation with supportive messaging.
- Allergy-aware meal recommendations using verified nutrition data.
- User profile management (name, weight, allergies).

## Out of Scope (MVP)
- Payments, social features, full nutrition planning.

## Stakeholders
- Product Owner, Tech Lead, Engineering, QA, End Users, Clinical Advisor.

## Constraints
- Privacy compliance, reliable datasets, limited infra budget.

## Risks & Mitigations
- Data accuracy: use verified sources (USDA, Edamam).
- Privacy: anonymize analytics; clear consent and retention policy.
- Availability: health checks and monitoring; staged rollouts.

## Success Metrics
- Task completion rate for registration and first suggestion > 90%.
- <1% error rate for BMI calculations.
- Zero critical incidents related to allergy violations.
