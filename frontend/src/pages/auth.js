/**
 * Authentication Pages
 * Handles login and registration forms
 */

class AuthPages {
    constructor() {
        this.initializeElements();
        this.bindEvents();
        this.currentForm = 'login';
    }

    /**
     * Initialize DOM elements
     */
    initializeElements() {
        this.elements = {
            authContainer: document.getElementById('auth-container'),
            loginForm: document.getElementById('login-form'),
            registerForm: document.getElementById('register-form'),
            loginFormElement: document.getElementById('login-form-element'),
            registerFormElement: document.getElementById('register-form-element'),
            showRegister: document.getElementById('show-register'),
            showLogin: document.getElementById('show-login'),
            forgotPasswordLink: document.getElementById('forgot-password-link')
        };
    }

    /**
     * Bind event listeners
     */
    bindEvents() {
        // Form submissions
        this.elements.loginFormElement?.addEventListener('submit', (e) => this.handleLogin(e));
        this.elements.registerFormElement?.addEventListener('submit', (e) => this.handleRegister(e));

        // Form switching
        this.elements.showRegister?.addEventListener('click', () => this.showRegisterForm());
        this.elements.showLogin?.addEventListener('click', () => this.showLoginForm());
        
        // Forgot password
        this.elements.forgotPasswordLink?.addEventListener('click', () => this.handleForgotPassword());

        // Real-time validation
        this.setupRealTimeValidation();
    }

    /**
     * Setup real-time form validation
     */
    setupRealTimeValidation() {
        // Password validation
        const registerPassword = document.getElementById('register-password');
        if (registerPassword) {
            registerPassword.addEventListener('input', () => this.validatePasswordReal());
        }

        // Email validation
        const emailInputs = ['login-email', 'register-email'].map(id => document.getElementById(id));
        emailInputs.forEach(input => {
            if (input) {
                input.addEventListener('blur', () => this.validateEmailReal(input));
            }
        });

        // Height and weight validation
        const heightInput = document.getElementById('register-height');
        const weightInput = document.getElementById('register-weight');
        
        if (heightInput && weightInput) {
            const validateBMI = () => this.calculateAndDisplayBMI();
            
            heightInput.addEventListener('input', validateBMI);
            weightInput.addEventListener('input', validateBMI);
        }
    }

    /**
     * Validate email in real-time
     * @param {HTMLElement} input - Email input element
     */
    validateEmailReal(input) {
        const email = input.value.trim();
        const isValid = window.authManager.validateEmail(email);
        
        const errorId = `${input.id}-error`;
        
        if (email && !isValid) {
            window.authManager.showFormError(input.id, 'Please enter a valid email address');
        } else {
            const errorElement = document.getElementById(errorId);
            if (errorElement) {
                errorElement.textContent = '';
                errorElement.classList.add('hidden');
            }
        }
    }

    /**
     * Validate password in real-time
     */
    validatePasswordReal() {
        const passwordInput = document.getElementById('register-password');
        if (!passwordInput) return;

        const password = passwordInput.value;
        const validation = window.authManager.validatePassword(password);
        
        if (password && !validation.isValid) {
            window.authManager.showFormError('register-password', validation.errors[0]);
        } else {
            const errorElement = document.getElementById('register-password-error');
            if (errorElement) {
                errorElement.textContent = '';
                errorElement.classList.add('hidden');
            }
        }
    }

    /**
     * Calculate and display BMI in real-time
     */
    calculateAndDisplayBMI() {
        const heightInput = document.getElementById('register-height');
        const weightInput = document.getElementById('register-weight');
        
        if (!heightInput || !weightInput) return;
        
        const height = parseFloat(heightInput.value);
        const weight = parseFloat(weightInput.value);
        
        if (height && weight) {
            const bmiData = window.authManager.calculateBMI(height, weight);
            this.displayBMIPreview(bmiData);
        }
    }

    /**
     * Display BMI preview
     * @param {Object} bmiData - BMI calculation data
     */
    displayBMIPreview(bmiData) {
        let previewElement = document.getElementById('bmi-preview');
        
        if (!previewElement) {
            previewElement = document.createElement('div');
            previewElement.id = 'bmi-preview';
            previewElement.className = 'bmi-preview';
            
            const weightInput = document.getElementById('register-weight');
            if (weightInput && weightInput.parentNode) {
                weightInput.parentNode.appendChild(previewElement);
            }
        }
        
        const eligibilityClass = bmiData.isEligible ? 'bmi-status--eligible' : 'bmi-status--ineligible';
        const eligibilityText = bmiData.isEligible ? '✓ Eligible for program' : '⚠ BMI below program threshold';
        
        previewElement.innerHTML = `
            <div class="bmi-preview-content">
                <p class="text-small"><strong>BMI: ${bmiData.bmi}</strong> (${bmiData.category})</p>
                <div class="bmi-status ${eligibilityClass}">
                    <span>${eligibilityText}</span>
                </div>
                <p class="text-small text-muted">${bmiData.message}</p>
            </div>
        `;
    }

    /**
     * Handle login form submission
     * @param {Event} e - Form submit event
     */
    async handleLogin(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const credentials = {
            email: formData.get('email').trim(),
            password: formData.get('password')
        };
        
        // Clear previous errors
        window.authManager.clearFormErrors('login');
        
        // Validate inputs
        if (!this.validateLoginForm(credentials)) {
            return;
        }
        
        // Set loading state
        this.setFormLoading('login', true);
        
        try {
            const response = await window.apiClient.login(credentials);
            
            // Trigger auth state update
            window.authManager.triggerLogin(window.apiClient.getCurrentUser());
            
            // Navigate to dashboard
            window.appRouter?.navigate('dashboard');
            
            window.notificationManager.success('Login successful! Welcome back.');
            
        } catch (error) {
            console.error('Login error:', error);
            window.notificationManager.error(error.message || 'Login failed. Please check your credentials.');
        } finally {
            this.setFormLoading('login', false);
        }
    }

    /**
     * Handle registration form submission
     * @param {Event} e - Form submit event
     */
    async handleRegister(e) {
        e.preventDefault();
        
        const formData = new FormData(e.target);
        const userData = {
            email: formData.get('email').trim(),
            password: formData.get('password'),
            height: parseFloat(formData.get('height')),
            weight: parseFloat(formData.get('weight'))
        };
        
        // Clear previous errors
        window.authManager.clearFormErrors('register');
        
        // Validate inputs
        if (!this.validateRegisterForm(userData)) {
            return;
        }
        
        // Set loading state
        this.setFormLoading('register', true);
        
        try {
            const response = await window.apiClient.register(userData);
            
            // Trigger auth state update
            window.authManager.triggerLogin(window.apiClient.getCurrentUser());
            
            // Navigate to dashboard
            window.appRouter?.navigate('dashboard');
            
            window.notificationManager.success('Account created successfully! Welcome to your health journey.');
            
        } catch (error) {
            console.error('Registration error:', error);
            
            if (error.message.includes('already registered')) {
                window.authManager.showFormError('register-email', 'This email is already registered. Try logging in instead.');
            } else {
                window.notificationManager.error(error.message || 'Registration failed. Please try again.');
            }
        } finally {
            this.setFormLoading('register', false);
        }
    }

    /**
     * Validate login form
     * @param {Object} credentials - Login credentials
     * @returns {boolean} Validation result
     */
    validateLoginForm(credentials) {
        let isValid = true;
        
        // Email validation
        if (!credentials.email) {
            window.authManager.showFormError('login-email', 'Email is required');
            isValid = false;
        } else if (!window.authManager.validateEmail(credentials.email)) {
            window.authManager.showFormError('login-email', 'Please enter a valid email address');
            isValid = false;
        }
        
        // Password validation
        if (!credentials.password) {
            window.authManager.showFormError('login-password', 'Password is required');
            isValid = false;
        }
        
        return isValid;
    }

    /**
     * Validate registration form
     * @param {Object} userData - Registration data
     * @returns {boolean} Validation result
     */
    validateRegisterForm(userData) {
        let isValid = true;
        
        // Email validation
        if (!userData.email) {
            window.authManager.showFormError('register-email', 'Email is required');
            isValid = false;
        } else if (!window.authManager.validateEmail(userData.email)) {
            window.authManager.showFormError('register-email', 'Please enter a valid email address');
            isValid = false;
        }
        
        // Password validation
        const passwordValidation = window.authManager.validatePassword(userData.password);
        if (!passwordValidation.isValid) {
            window.authManager.showFormError('register-password', passwordValidation.errors[0]);
            isValid = false;
        }
        
        // Height validation
        const heightValidation = window.authManager.validateHeight(userData.height);
        if (!heightValidation.isValid) {
            window.authManager.showFormError('register-height', heightValidation.error);
            isValid = false;
        }
        
        // Weight validation
        const weightValidation = window.authManager.validateWeight(userData.weight);
        if (!weightValidation.isValid) {
            window.authManager.showFormError('register-weight', weightValidation.error);
            isValid = false;
        }
        
        return isValid;
    }

    /**
     * Set form loading state
     * @param {string} formType - 'login' or 'register'
     * @param {boolean} loading - Loading state
     */
    setFormLoading(formType, loading) {
        const btnText = document.getElementById(`${formType}-btn-text`);
        const loadingSpinner = document.getElementById(`${formType}-loading`);
        const submitBtn = document.querySelector(`#${formType}-form-element button[type="submit"]`);
        
        if (loading) {
            btnText?.classList.add('hidden');
            loadingSpinner?.classList.remove('hidden');
            submitBtn?.setAttribute('disabled', 'true');
        } else {
            btnText?.classList.remove('hidden');
            loadingSpinner?.classList.add('hidden');
            submitBtn?.removeAttribute('disabled');
        }
    }

    /**
     * Show login form
     */
    showLoginForm() {
        this.elements.loginForm?.classList.remove('hidden');
        this.elements.registerForm?.classList.add('hidden');
        this.currentForm = 'login';
        
        // Focus first input
        const firstInput = document.getElementById('login-email');
        firstInput?.focus();
    }

    /**
     * Show register form
     */
    showRegisterForm() {
        this.elements.registerForm?.classList.remove('hidden');
        this.elements.loginForm?.classList.add('hidden');
        this.currentForm = 'register';
        
        // Focus first input
        const firstInput = document.getElementById('register-email');
        firstInput?.focus();
    }

    /**
     * Show auth container
     */
    show() {
        this.elements.authContainer?.classList.remove('hidden');
        
        // Focus appropriate form
        if (this.currentForm === 'login') {
            this.showLoginForm();
        } else {
            this.showRegisterForm();
        }
    }

    /**
     * Hide auth container
     */
    hide() {
        this.elements.authContainer?.classList.add('hidden');
    }

    /**
     * Handle forgot password
     */
    async handleForgotPassword() {
        const email = document.getElementById('login-email')?.value?.trim();
        
        if (!email) {
            window.notificationManager.warning('Please enter your email address first');
            return;
        }
        
        if (!window.authManager.validateEmail(email)) {
            window.notificationManager.error('Please enter a valid email address');
            return;
        }
        
        try {
            await window.apiClient.forgotPassword(email);
            window.notificationManager.success('Password reset instructions have been sent to your email');
        } catch (error) {
            window.notificationManager.error(error.message || 'Failed to send password reset email');
        }
    }
}

// Add auth-specific styles
const authStyles = `
.bmi-preview {
    margin-top: var(--spacing-sm);
    padding: var(--spacing-sm);
    background-color: var(--secondary-color);
    border-radius: var(--border-radius);
    border: 1px solid var(--border-color-light);
}

.bmi-preview-content {
    text-align: center;
}

.bmi-preview p {
    margin-bottom: var(--spacing-xs);
}

.bmi-preview .bmi-status {
    margin: var(--spacing-xs) 0;
}
`;

// Inject styles
const authStyleSheet = document.createElement('style');
authStyleSheet.textContent = authStyles;
document.head.appendChild(authStyleSheet);

// Create global auth pages instance
window.authPages = new AuthPages();