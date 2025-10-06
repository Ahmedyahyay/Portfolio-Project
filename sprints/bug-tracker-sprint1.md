# Sprint 1 Bug Tracker

### Bug ID: 001
- **Title:** Incorrect BMI calculation for heights entered in meters instead of centimeters.
- **Status:** Closed
- **Priority:** High
- **Description:** If a user enters height as "1.75" instead of "175", the BMI is calculated incorrectly, leading to a wrong eligibility check.
- **Resolution:** Added frontend validation to ensure height is a reasonable integer value for centimeters. Added a clear "(cm)" label next to the input field.

### Bug ID: 002
- **Title:** Password field accepts weak passwords during registration.
- **Status:** Closed
- **Priority:** High
- **Description:** The registration form allows users to submit passwords like "12345". This violates our security requirements.
- **Resolution:** Implemented frontend and backend validation to enforce a strong password policy (min 8 characters, at least one number, one uppercase letter).

### Bug ID: 003
- **Title:** User is not redirected to the dashboard after successful login.
- **Status:** Closed
- **Priority:** Medium
- **Description:** After submitting correct credentials, the login form clears, but the user remains on the login page.
- **Resolution:** Fixed the state handling logic in the React app. The router now correctly redirects the user to `/dashboard` upon successful authentication.

### Bug ID: 004
- **Title:** Meal list endpoint returns items with missing allergen data without flagging.
- **Status:** Closed
- **Priority:** Medium
- **Description:** Some meals lacked allergen metadata causing potential risk.
- **Resolution:** Added `uncertain_allergens` flag and deprioritized such meals in recommendations.

### Bug ID: 005
- **Title:** Registration allows zero height or weight.
- **Status:** Closed
- **Priority:** High
- **Description:** Validation missed non-positive height/weight leading to divide-by-zero risk.
- **Resolution:** Enforced ranges (1–300 cm, 1–500 kg) and error messages.

### Bug ID: 006
- **Title:** Login response missing full name for greeting.
- **Status:** Closed
- **Priority:** Low
- **Description:** Frontend greeting required concatenated name.
- **Resolution:** Backend now returns `full_name` in login and registration responses.
