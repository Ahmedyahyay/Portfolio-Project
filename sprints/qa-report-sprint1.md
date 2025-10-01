# Sprint 1 QA Report

## Test Cases
| Test Case ID | Description | Status | Notes |
|--------------|-------------|--------|-------|
| TC1 | Register new user (valid data) | Pass | User created successfully |
| TC2 | Register user (duplicate email) | Pass | Returns 409 error, email already registered |
| TC3 | Login with valid credentials | Pass | Returns 200, login successful |
| TC4 | Login with invalid credentials | Pass | Returns 401 error, invalid credentials |
| TC5 | Password reset (valid email) | Pass | Returns 200, reset instructions sent |
| TC6 | Password reset (invalid email) | Pass | Returns 404 error, email not found |
| TC7 | BMI calculation (valid input) | Pass | Returns 200, correct BMI value |
| TC8 | BMI calculation (invalid input) | Pass | Returns 400 error, invalid input |

## Bugs
- See [bug-tracker-sprint1.md](./bug-tracker-sprint1.md)

## QA Notes
- Add test results and notes after each test run.

[Back to Sprint 1 Plan](./sprint1-plan.md)
