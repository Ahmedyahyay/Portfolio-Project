# QA Checklist - Personal Nutrition Assistant

## Authentication & Registration

### Registration
- [ ] User can register with first name, last name, email, password, height (cm), weight (kg)
- [ ] Password validation enforces minimum 8 characters, uppercase, lowercase, number
- [ ] Email validation rejects invalid email formats
- [ ] Height validation accepts 1-300 cm range
- [ ] Weight validation accepts 1-500 kg range
- [ ] Duplicate email registration returns 409 error
- [ ] BMI is calculated and stored during registration
- [ ] Registration success returns user_id, first_name, last_name, bmi

### Login
- [ ] User can login with valid email and password
- [ ] Invalid credentials return 401 error
- [ ] Missing email/password returns 400 error
- [ ] Login success returns user profile data
- [ ] Password is securely hashed (not stored in plain text)

### Password Reset (Future)
- [ ] Forgot password sends email with reset link
- [ ] Reset link expires after specified time
- [ ] New password follows validation rules

## BMI Calculation

### BMI Endpoint
- [ ] POST /api/bmi accepts height_cm and weight_kg
- [ ] BMI calculation: weight_kg / (height_cm/100)^2
- [ ] BMI >= 30 returns motivational message
- [ ] BMI 18.5-24.9 returns maintenance message
- [ ] Other BMI ranges return neutral guidance
- [ ] Invalid height/weight returns 400 error
- [ ] Response includes bmi, eligibility, message

### User BMI
- [ ] GET /api/bmi/user/<id> returns user's current BMI
- [ ] Missing user returns 404 error
- [ ] Missing height/weight returns 400 error

## Meal Recommendations

### Basic Functionality
- [ ] GET /api/meals?user_id=<id> returns personalized recommendations
- [ ] Meals are filtered by user allergies
- [ ] BMI >= 30 users get meals <= 700 calories
- [ ] Response includes 3 meals per type when available
- [ ] Insufficient data flag when < 3 meals found
- [ ] Allergy conflict detection works correctly

### Allergy Filtering
- [ ] User allergies are normalized (lowercase)
- [ ] Meal allergens are checked against user allergies
- [ ] Meals with conflicting allergens are excluded
- [ ] Uncertain allergen meals are flagged
- [ ] Allergy note appears when uncertain meals present

### External API Integration
- [ ] GET /api/meals/external fetches from USDA API
- [ ] API key configuration works
- [ ] Error handling for API failures
- [ ] Data processing converts external format

## Meal History

### Adding Meals
- [ ] POST /api/meals/history adds meal to user history
- [ ] Valid user_id and meal_id required
- [ ] Invalid user/meal returns 404 error
- [ ] Success returns confirmation message

### Retrieving History
- [ ] GET /api/meals/history/<user_id> returns user's meal history
- [ ] History limited to last 30 days
- [ ] Results ordered by date (most recent first)
- [ ] Includes meal name, type, calories, date consumed

## Frontend Integration

### Registration Form
- [ ] Form validates all required fields
- [ ] Password strength indicator works
- [ ] Error messages display validation details
- [ ] Success redirects to dashboard
- [ ] Loading states work correctly

### Login Form
- [ ] Form validates email and password
- [ ] Error messages for invalid credentials
- [ ] Success stores user data and redirects
- [ ] Loading states work correctly

### Dashboard
- [ ] Personalized greeting shows "Hello, [FirstName] [LastName] 👋"
- [ ] BMI calculator integrates with backend
- [ ] Meal recommendations display correctly
- [ ] Allergy warnings show for uncertain meals
- [ ] Navigation between dashboard and profile works

### Profile Page
- [ ] Displays current user information
- [ ] Allows updating name, weight, allergies
- [ ] Changes persist to database
- [ ] Success/error messages display

## Security & Performance

### Security
- [ ] Passwords are hashed with bcrypt
- [ ] API endpoints validate input data
- [ ] CORS configured correctly
- [ ] Environment variables used for secrets
- [ ] No sensitive data in logs

### Performance
- [ ] API responses under 300ms average
- [ ] Database queries optimized with indexes
- [ ] Error handling doesn't expose internals
- [ ] Frontend loads quickly

## Error Handling

### API Errors
- [ ] 400 errors for validation failures
- [ ] 401 errors for authentication failures
- [ ] 404 errors for missing resources
- [ ] 409 errors for conflicts
- [ ] 500 errors for server issues
- [ ] Error responses include helpful messages

### Frontend Errors
- [ ] Network errors handled gracefully
- [ ] Form validation errors display clearly
- [ ] Loading states prevent double submissions
- [ ] User-friendly error messages

## Data Validation

### Input Validation
- [ ] All numeric inputs validated for range
- [ ] String inputs validated for length
- [ ] Email format validation
- [ ] Required field validation
- [ ] SQL injection prevention

### Business Rules
- [ ] BMI calculation accuracy
- [ ] Calorie cap enforcement for obese users
- [ ] Allergy filtering logic
- [ ] Meal type categorization

## Browser Compatibility

### Modern Browsers
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)

### Mobile Responsiveness
- [ ] Mobile layout works on small screens
- [ ] Touch interactions work correctly
- [ ] Forms are usable on mobile
- [ ] Navigation is mobile-friendly

## Accessibility

### Basic Accessibility
- [ ] Form labels associated with inputs
- [ ] Error messages announced to screen readers
- [ ] Keyboard navigation works
- [ ] Color contrast meets standards
- [ ] Alt text for images (if any)

## Testing Scenarios

### Happy Path
1. User registers with valid data
2. User logs in successfully
3. User calculates BMI
4. User gets meal recommendations
5. User adds meal to history
6. User updates profile

### Edge Cases
1. User with many allergies gets limited recommendations
2. User with BMI >= 30 gets calorie-capped meals
3. User with no allergies gets full recommendations
4. External API fails gracefully
5. Database connection issues handled

### Error Cases
1. Invalid registration data
2. Invalid login credentials
3. Missing user for meal recommendations
4. Invalid BMI calculation inputs
5. Network connectivity issues
