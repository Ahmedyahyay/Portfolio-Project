/**
 * Profile Management Page
 * Handles user profile editing and preferences
 */

class ProfilePage {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.currentUserData = null;
    }

    /**
     * Initialize DOM elements
     */
    initializeElements() {
        this.elements = {
            profileSection: document.getElementById('profile-section'),
            basicForm: document.getElementById('profile-basic-form'),
            preferencesForm: document.getElementById('profile-preferences-form'),
            heightInput: document.getElementById('profile-height'),
            weightInput: document.getElementById('profile-weight'),
            allergiesInput: document.getElementById('profile-allergies'),
            preferencesInput: document.getElementById('profile-preferences'),
            bmiDisplay: document.getElementById('profile-bmi-display')
        };
    }

    /**
     * Bind event listeners
     */
    bindEvents() {
        // Form submissions
        this.elements.basicForm?.addEventListener('submit', (e) => this.handleBasicInfoUpdate(e));
        this.elements.preferencesForm?.addEventListener('submit', (e) => this.handlePreferencesUpdate(e));

        // Real-time BMI calculation
        const bmiInputs = [this.elements.heightInput, this.elements.weightInput];
        bmiInputs.forEach(input => {
            if (input) {
                input.addEventListener('input', () => this.calculateBMIRealTime());
            }
        });

        // Input validation
        this.setupInputValidation();
    }

    /**
     * Setup input validation
     */
    setupInputValidation() {
        // Height validation
        if (this.elements.heightInput) {
            this.elements.heightInput.addEventListener('blur', () => {
                this.validateHeightInput();
            });
        }

        // Weight validation
        if (this.elements.weightInput) {
            this.elements.weightInput.addEventListener('blur', () => {
                this.validateWeightInput();
            });
        }
    }

    /**
     * Validate height input
     */
    validateHeightInput() {
        const height = parseFloat(this.elements.heightInput.value);
        const validation = window.authManager.validateHeight(height);
        
        const errorElement = this.elements.heightInput.parentNode.querySelector('.form-error');
        if (errorElement) {
            if (!validation.isValid && height) {
                errorElement.textContent = validation.error;
                errorElement.classList.remove('hidden');
            } else {
                errorElement.textContent = '';
                errorElement.classList.add('hidden');
            }
        }
    }

    /**
     * Validate weight input
     */
    validateWeightInput() {
        const weight = parseFloat(this.elements.weightInput.value);
        const validation = window.authManager.validateWeight(weight);
        
        const errorElement = this.elements.weightInput.parentNode.querySelector('.form-error');
        if (errorElement) {
            if (!validation.isValid && weight) {
                errorElement.textContent = validation.error;
                errorElement.classList.remove('hidden');
            } else {
                errorElement.textContent = '';
                errorElement.classList.add('hidden');
            }
        }
    }

    /**
     * Calculate BMI in real-time
     */
    calculateBMIRealTime() {
        const height = parseFloat(this.elements.heightInput.value);
        const weight = parseFloat(this.elements.weightInput.value);
        
        if (height && weight && height >= 100 && weight >= 40) {
            const bmiData = window.authManager.calculateBMI(height, weight);
            this.displayBMI(bmiData);
        } else {
            this.clearBMIDisplay();
        }
    }

    /**
     * Display BMI calculation
     * @param {Object} bmiData - BMI calculation data
     */
    displayBMI(bmiData) {
        if (!this.elements.bmiDisplay) return;

        const eligibilityClass = bmiData.isEligible ? 'bmi-status--eligible' : 'bmi-status--ineligible';
        const eligibilityIcon = bmiData.isEligible ? '✓' : '⚠';
        const eligibilityText = bmiData.isEligible ? 'Eligible for program' : 'Below program threshold';
        
        this.elements.bmiDisplay.innerHTML = `
            <div class="bmi-result">
                <div class="bmi-value">
                    <span class="bmi-number">${bmiData.bmi}</span>
                    <span class="bmi-category">${bmiData.category}</span>
                </div>
                <div class="bmi-status ${eligibilityClass}">
                    <span>${eligibilityIcon} ${eligibilityText}</span>
                </div>
                <p class="bmi-message text-small text-muted">${bmiData.message}</p>
            </div>
        `;
    }

    /**
     * Clear BMI display
     */
    clearBMIDisplay() {
        if (this.elements.bmiDisplay) {
            this.elements.bmiDisplay.innerHTML = '';
        }
    }

    /**
     * Load user profile data
     */
    async loadUserProfile() {
        const user = window.apiClient?.getCurrentUser();
        if (!user) {
            window.appRouter?.navigate('login');
            return;
        }

        try {
            // For now, we'll simulate loading user data since the backend doesn't have profile endpoints yet
            // In a real implementation, this would be an API call
            this.currentUserData = {
                id: user.id,
                email: user.email,
                height: 170, // Placeholder data
                weight: 85,  // Placeholder data
                allergies: 'None specified',
                preferences: 'None specified'
            };

            this.populateForm();
            this.calculateBMIRealTime();
            
        } catch (error) {
            console.error('Failed to load user profile:', error);
            window.notificationManager.error('Failed to load profile data');
        }
    }

    /**
     * Populate form with user data
     */
    populateForm() {
        if (!this.currentUserData) return;

        // Basic information
        if (this.elements.heightInput) {
            this.elements.heightInput.value = this.currentUserData.height || '';
        }
        if (this.elements.weightInput) {
            this.elements.weightInput.value = this.currentUserData.weight || '';
        }

        // Preferences
        if (this.elements.allergiesInput) {
            this.elements.allergiesInput.value = this.currentUserData.allergies || '';
        }
        if (this.elements.preferencesInput) {
            this.elements.preferencesInput.value = this.currentUserData.preferences || '';
        }
    }

    /**
     * Handle basic information update
     * @param {Event} e - Form submit event
     */
    async handleBasicInfoUpdate(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const height = parseFloat(formData.get('height'));
        const weight = parseFloat(formData.get('weight'));
        
        // Validate inputs
        if (!this.validateBasicInfo(height, weight)) {
            return;
        }
        
        // Set loading state
        this.setFormLoading('basic', true);
        
        try {
            // For now, simulate the update since we don't have profile update endpoints
            // In a real implementation, this would be an API call
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Update local data
            this.currentUserData.height = height;
            this.currentUserData.weight = weight;
            
            window.notificationManager.success('Basic information updated successfully');
            
            // Update BMI calculation in dashboard if visible
            this.updateDashboardBMI();
            
        } catch (error) {
            console.error('Failed to update basic info:', error);
            window.notificationManager.error('Failed to update basic information');
        } finally {
            this.setFormLoading('basic', false);
        }
    }

    /**
     * Handle preferences update
     * @param {Event} e - Form submit event
     */
    async handlePreferencesUpdate(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const allergies = formData.get('allergies')?.trim() || '';
        const preferences = formData.get('preferences')?.trim() || '';
        
        // Set loading state
        this.setFormLoading('preferences', true);
        
        try {
            // For now, simulate the update
            await new Promise(resolve => setTimeout(resolve, 800));
            
            // Update local data
            this.currentUserData.allergies = allergies;
            this.currentUserData.preferences = preferences;
            
            window.notificationManager.success('Dietary preferences updated successfully');
            
        } catch (error) {
            console.error('Failed to update preferences:', error);
            window.notificationManager.error('Failed to update dietary preferences');
        } finally {
            this.setFormLoading('preferences', false);
        }
    }

    /**
     * Validate basic information
     * @param {number} height - Height value
     * @param {number} weight - Weight value
     * @returns {boolean} Validation result
     */
    validateBasicInfo(height, weight) {
        let isValid = true;
        
        // Clear previous errors
        this.clearFormErrors();
        
        // Height validation
        const heightValidation = window.authManager.validateHeight(height);
        if (!heightValidation.isValid) {
            this.showFieldError('height', heightValidation.error);
            isValid = false;
        }
        
        // Weight validation
        const weightValidation = window.authManager.validateWeight(weight);
        if (!weightValidation.isValid) {
            this.showFieldError('weight', weightValidation.error);
            isValid = false;
        }
        
        return isValid;
    }

    /**
     * Show field error
     * @param {string} field - Field name
     * @param {string} message - Error message
     */
    showFieldError(field, message) {
        const input = document.getElementById(`profile-${field}`);
        if (input) {
            const errorElement = input.parentNode.querySelector('.form-error') || this.createErrorElement(input);
            errorElement.textContent = message;
            errorElement.classList.remove('hidden');
        }
    }

    /**
     * Create error element if it doesn't exist
     * @param {HTMLElement} input - Input element
     * @returns {HTMLElement} Error element
     */
    createErrorElement(input) {
        const errorElement = document.createElement('div');
        errorElement.className = 'form-error hidden';
        input.parentNode.appendChild(errorElement);
        return errorElement;
    }

    /**
     * Clear form errors
     */
    clearFormErrors() {
        const errorElements = this.elements.profileSection.querySelectorAll('.form-error');
        errorElements.forEach(element => {
            element.textContent = '';
            element.classList.add('hidden');
        });
    }

    /**
     * Set form loading state
     * @param {string} formType - 'basic' or 'preferences'
     * @param {boolean} loading - Loading state
     */
    setFormLoading(formType, loading) {
        const form = formType === 'basic' ? this.elements.basicForm : this.elements.preferencesForm;
        const submitBtn = form?.querySelector('button[type="submit"]');
        
        if (submitBtn) {
            if (loading) {
                submitBtn.disabled = true;
                submitBtn.classList.add('loading');
                submitBtn.textContent = 'Saving...';
            } else {
                submitBtn.disabled = false;
                submitBtn.classList.remove('loading');
                submitBtn.textContent = formType === 'basic' ? 'Update Information' : 'Save Preferences';
            }
        }
    }

    /**
     * Update BMI display in dashboard
     */
    updateDashboardBMI() {
        const dashboardBMI = document.getElementById('bmi-display');
        const dashboardStatus = document.getElementById('bmi-status');
        
        if (dashboardBMI && this.currentUserData) {
            const bmiData = window.authManager.calculateBMI(
                this.currentUserData.height, 
                this.currentUserData.weight
            );
            
            dashboardBMI.textContent = `${bmiData.bmi}`;
            
            if (dashboardStatus) {
                const eligibilityClass = bmiData.isEligible ? 'bmi-status--eligible' : 'bmi-status--ineligible';
                const eligibilityText = bmiData.isEligible ? '✓ Eligible for Program' : '⚠ Below Program Threshold';
                
                dashboardStatus.className = `bmi-status ${eligibilityClass}`;
                dashboardStatus.innerHTML = `<span>${eligibilityText}</span>`;
                dashboardStatus.classList.remove('hidden');
            }
        }
    }

    /**
     * Show profile section
     */
    show() {
        this.elements.profileSection?.classList.remove('hidden');
        this.loadUserProfile();
    }

    /**
     * Hide profile section
     */
    hide() {
        this.elements.profileSection?.classList.add('hidden');
    }

    /**
     * Get current user data
     * @returns {Object|null} Current user data
     */
    getCurrentUserData() {
        return this.currentUserData;
    }
}

// Add profile-specific styles
const profileStyles = `
.bmi-result {
    text-align: center;
    padding: var(--spacing-base);
    background-color: var(--secondary-color);
    border-radius: var(--border-radius);
    border: 1px solid var(--border-color-light);
    margin-top: var(--spacing-base);
}

.bmi-value {
    display: flex;
    align-items: baseline;
    justify-content: center;
    gap: var(--spacing-sm);
    margin-bottom: var(--spacing-sm);
}

.bmi-number {
    font-size: var(--font-size-2xl);
    font-weight: var(--font-weight-bold);
    color: var(--primary-color);
}

.bmi-category {
    font-size: var(--font-size-sm);
    color: var(--text-secondary-color);
    font-weight: var(--font-weight-medium);
}

.bmi-message {
    margin-top: var(--spacing-sm);
    line-height: var(--line-height-relaxed);
}

.profile-grid .card h3 {
    color: var(--text-primary-color);
    margin-bottom: var(--spacing-lg);
    padding-bottom: var(--spacing-sm);
    border-bottom: 2px solid var(--primary-color-light);
}

.form-group small {
    display: block;
    margin-top: var(--spacing-xs);
}
`;

// Inject styles
const profileStyleSheet = document.createElement('style');
profileStyleSheet.textContent = profileStyles;
document.head.appendChild(profileStyleSheet);

// Create global profile page instance
window.profilePage = new ProfilePage();