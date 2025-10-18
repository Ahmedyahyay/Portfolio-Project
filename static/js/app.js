// Enhanced JavaScript for modern interactive elements following copilot patterns

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive components
    initializeNavigation();
    initializeFormValidation();
    initializeAnimations();
    initializeBMICalculator();
    initializeAlerts();
    initializeTableEnhancements();
    
    console.log('✅ Personal Nutrition Assistant - Frontend initialized');
});

// Navigation functionality with mobile support
function initializeNavigation() {
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (navToggle && navLinks) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
            navToggle.classList.toggle('active');
        });
        
        // Close mobile menu when clicking on links
        navLinks.querySelectorAll('a').forEach(link => {
            link.addEventListener('click', () => {
                navLinks.classList.remove('active');
                navToggle.classList.remove('active');
            });
        });
        
        // Close mobile menu when clicking outside
        document.addEventListener('click', function(e) {
            if (!navToggle.contains(e.target) && !navLinks.contains(e.target)) {
                navLinks.classList.remove('active');
                navToggle.classList.remove('active');
            }
        });
    }
}

// Enhanced form validation with real-time feedback
function initializeFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        const inputs = form.querySelectorAll('.form-control');
        
        inputs.forEach(input => {
            // Real-time validation feedback
            input.addEventListener('input', function() {
                validateField(this);
            });
            
            input.addEventListener('blur', function() {
                validateField(this);
            });
        });
        
        // Form submission validation
        form.addEventListener('submit', function(e) {
            let isValid = true;
            
            inputs.forEach(input => {
                if (!validateField(input)) {
                    isValid = false;
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                showNotification('Please correct the highlighted fields', 'error');
            }
        });
    });
}

function validateField(field) {
    const value = field.value.trim();
    const fieldType = field.type;
    const fieldName = field.name;
    let isValid = true;
    let message = '';
    
    // Remove existing validation styling
    field.classList.remove('is-valid', 'is-invalid');
    
    // Check required fields
    if (field.hasAttribute('required') && !value) {
        isValid = false;
        message = 'This field is required';
    }
    
    // Email validation
    else if (fieldType === 'email' && value) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(value)) {
            isValid = false;
            message = 'Please enter a valid email address';
        }
    }
    
    // Password validation
    else if (fieldType === 'password' && value) {
        if (value.length < 6) {
            isValid = false;
            message = 'Password must be at least 6 characters';
        }
    }
    
    // Height validation (BMI context)
    else if (fieldName === 'height' && value) {
        const height = parseFloat(value);
        if (isNaN(height) || height < 100 || height > 250) {
            isValid = false;
            message = 'Height must be between 100-250 cm';
        }
    }
    
    // Weight validation (BMI context)
    else if (fieldName === 'weight' && value) {
        const weight = parseFloat(value);
        if (isNaN(weight) || weight < 30 || weight > 300) {
            isValid = false;
            message = 'Weight must be between 30-300 kg';
        }
    }
    
    // Apply validation styling
    field.classList.add(isValid ? 'is-valid' : 'is-invalid');
    
    // Show/hide validation message
    let feedbackElement = field.parentNode.querySelector('.validation-feedback');
    if (!isValid && message) {
        if (!feedbackElement) {
            feedbackElement = document.createElement('div');
            feedbackElement.className = 'validation-feedback';
            field.parentNode.appendChild(feedbackElement);
        }
        feedbackElement.textContent = message;
        feedbackElement.style.display = 'block';
    } else if (feedbackElement) {
        feedbackElement.style.display = 'none';
    }
    
    return isValid;
}

// Animation and intersection observer for fade-in effects
function initializeAnimations() {
    // Add fade-in animation to elements as they enter viewport
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements for animation
    document.querySelectorAll('.content-card, .stat-card, .feature-card').forEach(el => {
        observer.observe(el);
    });
    
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ 
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
}

// Enhanced BMI calculator with real-time preview
function initializeBMICalculator() {
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');
    const bmiPreview = document.getElementById('bmiPreview');
    
    if (heightInput && weightInput) {
        function updateBMIPreview() {
            const height = parseFloat(heightInput.value);
            const weight = parseFloat(weightInput.value);
            
            if (height && weight && height >= 100 && height <= 250 && weight >= 30 && weight <= 300) {
                const bmi = weight / ((height / 100) ** 2);
                const category = getBMICategory(bmi);
                const eligible = bmi >= 30;
                const eligibleClass = eligible ? 'success' : 'warning';
                
                if (bmiPreview) {
                    bmiPreview.innerHTML = `
                        <div class="bmi-preview-card ${eligibleClass}">
                            <div class="bmi-value">BMI: ${bmi.toFixed(1)}</div>
                            <div class="bmi-category">${category}</div>
                            <div class="bmi-eligibility">
                                ${eligible ? '✅ Eligible for service' : '⚠️ BMI must be ≥ 30'}
                            </div>
                        </div>
                    `;
                }
                
                // Add visual feedback to inputs
                [heightInput, weightInput].forEach(input => {
                    input.classList.remove('bmi-eligible', 'bmi-not-eligible');
                    input.classList.add(eligible ? 'bmi-eligible' : 'bmi-not-eligible');
                });
            } else {
                if (bmiPreview) {
                    bmiPreview.innerHTML = '';
                }
                [heightInput, weightInput].forEach(input => {
                    input.classList.remove('bmi-eligible', 'bmi-not-eligible');
                });
            }
        }
        
        // Debounced input listeners
        let updateTimeout;
        [heightInput, weightInput].forEach(input => {
            input.addEventListener('input', function() {
                clearTimeout(updateTimeout);
                updateTimeout = setTimeout(updateBMIPreview, 300);
            });
        });
        
        // Initial calculation if values present
        updateBMIPreview();
    }
}

function getBMICategory(bmi) {
    if (bmi < 18.5) return 'Underweight';
    if (bmi < 25) return 'Normal weight';
    if (bmi < 30) return 'Overweight';
    if (bmi < 35) return 'Class I Obesity';
    if (bmi < 40) return 'Class II Obesity';
    return 'Class III Obesity';
}

// Enhanced alert system with auto-dismiss and animations
function initializeAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach((alert, index) => {
        // Add close button
        if (!alert.querySelector('.alert-close')) {
            const closeBtn = document.createElement('button');
            closeBtn.className = 'alert-close';
            closeBtn.innerHTML = '&times;';
            closeBtn.style.cssText = `
                background: none;
                border: none;
                font-size: 1.5rem;
                cursor: pointer;
                padding: 0;
                margin-left: auto;
                opacity: 0.7;
                transition: opacity 0.2s;
            `;
            
            closeBtn.addEventListener('click', () => dismissAlert(alert));
            closeBtn.addEventListener('mouseenter', () => closeBtn.style.opacity = '1');
            closeBtn.addEventListener('mouseleave', () => closeBtn.style.opacity = '0.7');
            
            alert.appendChild(closeBtn);
        }
        
        // Auto-dismiss after delay (longer for errors)
        const dismissDelay = alert.classList.contains('error') ? 8000 : 5000;
        setTimeout(() => dismissAlert(alert), dismissDelay);
    });
}

function dismissAlert(alert) {
    if (alert && alert.parentNode) {
        alert.style.transform = 'translateX(-100%)';
        alert.style.opacity = '0';
        setTimeout(() => {
            if (alert.parentNode) {
                alert.parentNode.removeChild(alert);
            }
        }, 300);
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert ${type}`;
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'times-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle'}"></i>
        <span>${message}</span>
    `;
    
    // Insert at top of page
    const container = document.querySelector('.container') || document.body;
    container.insertBefore(notification, container.firstChild);
    
    // Initialize alert functionality
    initializeAlerts();
}

// Table enhancements for better UX
function initializeTableEnhancements() {
    const tables = document.querySelectorAll('.meals-table');
    
    tables.forEach(table => {
        // Add row click highlighting
        const rows = table.querySelectorAll('tbody tr');
        rows.forEach(row => {
            row.addEventListener('click', function() {
                // Remove active class from other rows
                rows.forEach(r => r.classList.remove('table-row-active'));
                // Add active class to clicked row
                this.classList.add('table-row-active');
            });
        });
        
        // Add column sorting (basic implementation)
        const headers = table.querySelectorAll('th');
        headers.forEach((header, index) => {
            if (header.textContent.includes('Calories') || header.textContent.includes('Protein') || header.textContent.includes('Score')) {
                header.style.cursor = 'pointer';
                header.addEventListener('click', () => sortTableByColumn(table, index));
            }
        });
    });
}

function sortTableByColumn(table, columnIndex) {
    const tbody = table.querySelector('tbody');
    const rows = Array.from(tbody.querySelectorAll('tr'));
    
    const isNumeric = (str) => !isNaN(str) && !isNaN(parseFloat(str));
    
    rows.sort((a, b) => {
        const aText = a.cells[columnIndex].textContent.trim();
        const bText = b.cells[columnIndex].textContent.trim();
        
        if (isNumeric(aText) && isNumeric(bText)) {
            return parseFloat(bText) - parseFloat(aText); // Descending for numbers
        } else {
            return aText.localeCompare(bText); // Ascending for text
        }
    });
    
    rows.forEach(row => tbody.appendChild(row));
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// Add custom styles for validation
const validationStyles = document.createElement('style');
validationStyles.textContent = `
    .form-control.is-valid {
        border-color: var(--success-color);
        box-shadow: 0 0 0 3px rgba(40, 167, 69, 0.1);
    }
    
    .form-control.is-invalid {
        border-color: var(--error-color);
        box-shadow: 0 0 0 3px rgba(220, 53, 69, 0.1);
    }
    
    .validation-feedback {
        display: none;
        font-size: 0.875rem;
        color: var(--error-color);
        margin-top: 0.5rem;
    }
    
    .bmi-preview-card {
        background: rgba(255, 255, 255, 0.9);
        padding: 1rem;
        border-radius: var(--border-radius);
        text-align: center;
        margin-top: 1rem;
        border: 2px solid;
        transition: var(--transition);
    }
    
    .bmi-preview-card.success {
        border-color: var(--success-color);
        background: linear-gradient(135deg, #d4edda, #c3e6cb);
    }
    
    .bmi-preview-card.warning {
        border-color: var(--warning-color);
        background: linear-gradient(135deg, #fff3cd, #ffeaa7);
    }
    
    .bmi-value {
        font-size: 1.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .bmi-category {
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .bmi-eligibility {
        font-size: 0.875rem;
        font-weight: 500;
    }
    
    .form-control.bmi-eligible {
        border-color: var(--success-color);
    }
    
    .form-control.bmi-not-eligible {
        border-color: var(--warning-color);
    }
    
    .table-row-active {
        background: linear-gradient(135deg, rgba(76, 175, 80, 0.1), rgba(69, 160, 73, 0.1)) !important;
        transform: scale(1.001);
    }
`;
document.head.appendChild(validationStyles);
