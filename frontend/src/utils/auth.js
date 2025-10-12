/**
 * Authentication Utilities
 * Handles user authentication state and validation
 */

class AuthManager {
    constructor() {
        this.loginCallbacks = [];
        this.logoutCallbacks = [];
    }

    /**
     * Add callback for login events
     * @param {Function} callback - Function to call on login
     */
    onLogin(callback) {
        this.loginCallbacks.push(callback);
    }

    /**
     * Add callback for logout events
     * @param {Function} callback - Function to call on logout
     */
    onLogout(callback) {
        this.logoutCallbacks.push(callback);
    }

    /**
     * Trigger login callbacks
     * @param {Object} user - User data
     */
    triggerLogin(user) {
        this.loginCallbacks.forEach(callback => callback(user));
    }

    /**
     * Trigger logout callbacks
     */
    triggerLogout() {
        this.logoutCallbacks.forEach(callback => callback());
    }

    /**
     * Validate email format
     * @param {string} email - Email to validate
     * @returns {boolean} Validation result
     */
    validateEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    /**
     * Validate password strength
     * @param {string} password - Password to validate
     * @returns {Object} Validation result with details
     */
    validatePassword(password) {
        const minLength = 8;
        const hasUpperCase = /[A-Z]/.test(password);
        const hasLowerCase = /[a-z]/.test(password);
        const hasNumbers = /\d/.test(password);
        const hasNonalphas = /\W/.test(password);

        return {
            isValid: password.length >= minLength && hasLowerCase && hasNumbers,
            errors: [
                ...(password.length < minLength ? [`Password must be at least ${minLength} characters long`] : []),
                ...(!hasLowerCase ? ['Password must contain at least one lowercase letter'] : []),
                ...(!hasNumbers ? ['Password must contain at least one number'] : []),
            ],
            strength: this.calculatePasswordStrength(password)
        };
    }

    /**
     * Calculate password strength
     * @param {string} password - Password to evaluate
     * @returns {string} Strength level
     */
    calculatePasswordStrength(password) {
        let score = 0;
        
        if (password.length >= 8) score++;
        if (password.length >= 12) score++;
        if (/[a-z]/.test(password)) score++;
        if (/[A-Z]/.test(password)) score++;
        if (/[0-9]/.test(password)) score++;
        if (/[^A-Za-z0-9]/.test(password)) score++;

        if (score < 3) return 'weak';
        if (score < 5) return 'medium';
        return 'strong';
    }

    /**
     * Validate height input
     * @param {number} height - Height in cm
     * @returns {Object} Validation result
     */
    validateHeight(height) {
        const numHeight = parseFloat(height);
        return {
            isValid: numHeight >= 100 && numHeight <= 250,
            error: numHeight < 100 || numHeight > 250 ? 'Height must be between 100-250 cm' : null
        };
    }

    /**
     * Validate weight input
     * @param {number} weight - Weight in kg
     * @returns {Object} Validation result
     */
    validateWeight(weight) {
        const numWeight = parseFloat(weight);
        return {
            isValid: numWeight >= 40 && numWeight <= 300,
            error: numWeight < 40 || numWeight > 300 ? 'Weight must be between 40-300 kg' : null
        };
    }

    /**
     * Calculate BMI and eligibility
     * @param {number} height - Height in cm
     * @param {number} weight - Weight in kg
     * @returns {Object} BMI calculation with eligibility status
     */
    calculateBMI(height, weight) {
        const heightInMeters = height / 100;
        const bmi = weight / (heightInMeters * heightInMeters);
        
        return {
            bmi: Math.round(bmi * 10) / 10,
            isEligible: bmi >= 30,
            category: this.getBMICategory(bmi),
            message: this.getBMIMessage(bmi)
        };
    }

    /**
     * Get BMI category
     * @param {number} bmi - BMI value
     * @returns {string} BMI category
     */
    getBMICategory(bmi) {
        if (bmi < 18.5) return 'Underweight';
        if (bmi < 25) return 'Normal weight';
        if (bmi < 30) return 'Overweight';
        return 'Obese';
    }

    /**
     * Get BMI message
     * @param {number} bmi - BMI value
     * @returns {string} BMI message
     */
    getBMIMessage(bmi) {
        if (bmi >= 30) {
            return 'You are eligible for our nutrition program. Let us help you on your health journey.';
        } else if (bmi >= 25) {
            return 'Our program is designed for individuals with BMI ≥30. Consider consulting with a healthcare provider.';
        } else {
            return 'Our program is specifically designed for individuals with BMI ≥30. You may not need our specialized approach.';
        }
    }

    /**
     * Format form validation errors
     * @param {Object} errors - Error object
     * @returns {string} Formatted error message
     */
    formatValidationErrors(errors) {
        if (typeof errors === 'string') return errors;
        
        if (Array.isArray(errors)) {
            return errors.join('. ');
        }
        
        if (typeof errors === 'object') {
            return Object.values(errors).flat().join('. ');
        }
        
        return 'Validation failed';
    }

    /**
     * Clear all form errors
     * @param {string} formPrefix - Form prefix for error IDs
     */
    clearFormErrors(formPrefix) {
        const errorElements = document.querySelectorAll(`[id^="${formPrefix}"][id$="-error"]`);
        errorElements.forEach(element => {
            element.textContent = '';
            element.classList.add('hidden');
        });
    }

    /**
     * Show form error
     * @param {string} fieldId - Field ID
     * @param {string} message - Error message
     */
    showFormError(fieldId, message) {
        const errorElement = document.getElementById(`${fieldId}-error`);
        if (errorElement) {
            errorElement.textContent = message;
            errorElement.classList.remove('hidden');
        }
    }

    /**
     * Sanitize input to prevent XSS
     * @param {string} input - Input to sanitize
     * @returns {string} Sanitized input
     */
    sanitizeInput(input) {
        if (typeof input !== 'string') return input;
        
        return input
            .replace(/[<>]/g, '')
            .trim();
    }

    /**
     * Format user data for display
     * @param {Object} user - User data
     * @returns {Object} Formatted user data
     */
    formatUserData(user) {
        return {
            ...user,
            email: this.sanitizeInput(user.email),
            allergies: user.allergies ? this.sanitizeInput(user.allergies) : '',
            preferences: user.preferences ? this.sanitizeInput(user.preferences) : ''
        };
    }

    /**
     * Check if user session is valid (client-side validation)
     * @returns {boolean} Session validity
     */
    isSessionValid() {
        const user = window.apiClient?.getCurrentUser();
        return user && user.id && user.email;
    }

    /**
     * Get session expiry time (placeholder for future implementation)
     * @returns {Date|null} Session expiry time
     */
    getSessionExpiry() {
        // For future implementation with JWT tokens
        return null;
    }
}

// Create global auth manager instance
window.authManager = new AuthManager();