// Personal Nutrition Assistant - Frontend JavaScript
// Following copilot instructions for interactive elements

document.addEventListener('DOMContentLoaded', function() {
    // Mobile navigation toggle
    const navToggle = document.getElementById('navToggle');
    const navLinks = document.querySelector('.nav-links');
    
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            navLinks.classList.toggle('active');
        });
    }
    
    // Auto-hide alerts following copilot API response conventions
    setTimeout(function() {
        document.querySelectorAll('.alert').forEach(function(alert) {
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(-100%)';
            setTimeout(() => alert.remove(), 300);
        });
    }, 5000);
    
    // Form validation for BMI calculator following copilot input sanitization
    const bmiForm = document.getElementById('bmiForm');
    if (bmiForm) {
        bmiForm.addEventListener('submit', function(e) {
            const height = parseFloat(document.getElementById('height').value);
            const weight = parseFloat(document.getElementById('weight').value);
            
            if (!height || !weight || height < 100 || height > 250 || weight < 30 || weight > 300) {
                e.preventDefault();
                alert('Please enter valid height (100-250 cm) and weight (30-300 kg)');
                return false;
            }
        });
    }
    
    // Real-time BMI calculation preview
    const heightInput = document.getElementById('height');
    const weightInput = document.getElementById('weight');
    const bmiPreview = document.getElementById('bmiPreview');
    
    if (heightInput && weightInput && bmiPreview) {
        function updateBMIPreview() {
            const height = parseFloat(heightInput.value);
            const weight = parseFloat(weightInput.value);
            
            if (height && weight && height >= 100 && height <= 250 && weight >= 30 && weight <= 300) {
                const bmi = weight / ((height / 100) ** 2);
                const category = bmi >= 30 ? 'Eligible for service' : 'Not eligible (BMI < 30)';
                const eligibleClass = bmi >= 30 ? 'text-success' : 'text-warning';
                
                bmiPreview.innerHTML = `
                    <div class="bmi-preview ${eligibleClass}">
                        <strong>BMI: ${bmi.toFixed(1)}</strong><br>
                        <small>${category}</small>
                    </div>
                `;
            } else {
                bmiPreview.innerHTML = '';
            }
        }
        
        heightInput.addEventListener('input', updateBMIPreview);
        weightInput.addEventListener('input', updateBMIPreview);
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({ behavior: 'smooth' });
            }
        });
    });
    
    // Form validation following copilot security patterns
    const forms = document.querySelectorAll('form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    field.style.borderColor = '#dc3545';
                    isValid = false;
                } else {
                    field.style.borderColor = '#e9ecef';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields');
            }
        });
    });
    
    // API interaction for meal search (if on meals page)
    const mealSearchInput = document.getElementById('mealSearch');
    if (mealSearchInput) {
        let searchTimeout;
        
        mealSearchInput.addEventListener('input', function() {
            clearTimeout(searchTimeout);
            searchTimeout = setTimeout(() => {
                const query = this.value.trim();
                if (query.length >= 2) {
                    searchMeals(query);
                }
            }, 300);
        });
    }
    
    // AJAX meal search function
    function searchMeals(query) {
        fetch(`/meals/api/search?q=${encodeURIComponent(query)}`)
            .then(response => response.json())
            .then(data => {
                displaySearchResults(data.meals);
            })
            .catch(error => {
                console.error('Search error:', error);
            });
    }
    
    function displaySearchResults(meals) {
        const resultsContainer = document.getElementById('searchResults');
        if (!resultsContainer) return;
        
        if (meals.length === 0) {
            resultsContainer.innerHTML = '<p>No meals found matching your search.</p>';
            return;
        }
        
        const resultsHTML = meals.map(meal => `
            <div class="meal-result">
                <h4>${meal.name}</h4>
                <p><strong>Type:</strong> ${meal.type} | <strong>Calories:</strong> ${meal.calories}</p>
                <p><strong>Protein:</strong> ${meal.protein}g | <strong>Score:</strong> ${meal.nutrition_score}/50</p>
            </div>
        `).join('');
        
        resultsContainer.innerHTML = resultsHTML;
    }
});

// Utility functions following copilot patterns
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function calculateBMI(height, weight) {
    // Height in cm, following copilot health-centric patterns
    return weight / ((height / 100) ** 2);
}

function getBMICategory(bmi) {
    if (bmi < 18.5) return 'Underweight';
    if (bmi < 25) return 'Normal weight';
    if (bmi < 30) return 'Overweight';
    if (bmi < 35) return 'Class I Obesity';
    if (bmi < 40) return 'Class II Obesity';
    return 'Class III Obesity';
}

function isEligibleForService(bmi) {
    // Following copilot business rules
    return bmi >= 30.0;
}
