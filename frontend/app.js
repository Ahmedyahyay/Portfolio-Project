const API_BASE = 'http://127.0.0.1:5000';
let currentUser = null;

// API call helper function
async function makeAPICall(endpoint, data) {
    try {
        const response = await fetch(`${API_BASE}${endpoint}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });
        
        const result = await response.json();
        return { success: response.ok, data: result };
    } catch (error) {
        return { success: false, data: { error: `Network error: ${error.message}` } };
    }
}

// Display result helper
function displayResult(elementId, message, isSuccess) {
    const element = document.getElementById(elementId);
    element.innerHTML = message;
    element.className = `result ${isSuccess ? 'success' : 'error'}`;
}

// Register function
async function register() {
    const data = {
        email: document.getElementById('regEmail').value,
        password: document.getElementById('regPassword').value,
        height: parseFloat(document.getElementById('regHeight').value),
        weight: parseFloat(document.getElementById('regWeight').value)
    };

    // Validate required fields
    if (!data.email || !data.password || !data.height || !data.weight) {
        displayResult('regResult', 'Please fill all fields', false);
        return;
    }

    // Calculate BMI for eligibility check
    const bmi = data.weight / ((data.height / 100) ** 2);
    if (bmi < 30) {
        displayResult('regResult', `BMI: ${bmi.toFixed(2)} - This service is for adults with BMI ≥ 30`, false);
        return;
    }

    const result = await makeAPICall('/register', data);
    const message = result.success ? 
        `✓ ${result.data.message} (BMI: ${bmi.toFixed(2)})` : 
        `✗ ${result.data.error}`;
    
    displayResult('regResult', message, result.success);
    
    if (result.success) {
        // Clear form on success
        document.getElementById('regEmail').value = '';
        document.getElementById('regPassword').value = '';
        document.getElementById('regHeight').value = '';
        document.getElementById('regWeight').value = '';
    }
}

// Login function
async function login() {
    const data = {
        email: document.getElementById('loginEmail').value,
        password: document.getElementById('loginPassword').value
    };

    if (!data.email || !data.password) {
        displayResult('loginResult', 'Please fill all fields', false);
        return;
    }

    const result = await makeAPICall('/login', data);
    const message = result.success ? 
        `✓ ${result.data.message}` : 
        `✗ ${result.data.error}`;
    
    displayResult('loginResult', message, result.success);
    
    if (result.success) {
        // Store user session (simple example)
        sessionStorage.setItem('user_id', result.data.user_id);
        // Clear form on success
        document.getElementById('loginEmail').value = '';
        document.getElementById('loginPassword').value = '';
    }
}

// Enhanced BMI Calculator
async function calculateBMI(event) {
    if (event) event.preventDefault();
    
    const data = {
        height: parseFloat(document.getElementById('bmiHeight').value),
        weight: parseFloat(document.getElementById('bmiWeight').value)
    };

    if (!data.height || !data.weight) {
        displayResult('bmiResult', '⚠️ Please fill all fields', false);
        return;
    }

    displayResult('bmiResult', '⏳ Calculating your BMI...', true);

    const result = await makeAPICall('/calculate', data);
    
    if (result.success) {
        const bmi = result.data.BMI;
        let category = getBMICategory(bmi);
        let eligible = bmi >= 30 ? 
            '<br>✅ <strong>Eligible for nutrition assistance!</strong>' : 
            '<br>ℹ️ Our service is designed for BMI ≥ 30';
        
        const message = `📊 <strong>BMI: ${bmi}</strong><br>
                        📋 Category: ${category}${eligible}`;
        
        displayResult('bmiResult', message, true);
        
        // Show recommendations button if eligible
        if (bmi >= 30) {
            setTimeout(() => {
                const recommendBtn = `<br><button onclick="switchTab('meals')" class="btn-primary" style="margin-top: 10px;">
                    <i class="fas fa-utensils"></i> Get Meal Recommendations</button>`;
                document.getElementById('bmiResult').innerHTML += recommendBtn;
            }, 1000);
        }
    } else {
        displayResult('bmiResult', `❌ ${result.data.error}`, false);
    }
}

// Enhanced Meal Search
async function searchMeals(event) {
    if (event) event.preventDefault();
    
    const data = {
        query: document.getElementById('mealQuery').value,
        meal_type: document.getElementById('mealType').value,
        max_calories: document.getElementById('maxCalories').value
    };

    if (!data.query && !data.meal_type) {
        displayResult('mealResults', '⚠️ Please enter a search term or select meal type', false);
        return;
    }

    displayResult('mealResults', '🔍 Searching USDA nutrition database...', true);

    const result = await makeAPICall('/search', data);
    
    if (result.success) {
        const meals = result.data.meals;
        if (meals.length > 0) {
            displayResult('mealResults', 
                `✅ Found ${meals.length} meals matching your criteria`, true);
            displayMealCards(meals);
        } else {
            displayResult('mealResults', 
                '😔 No meals found. Try adjusting your search criteria.', false);
            document.getElementById('mealCards').innerHTML = '';
        }
    } else {
        displayResult('mealResults', `❌ ${result.data.error}`, false);
    }
}

// Get Personalized Recommendations
async function getRecommendations() {
    const userId = sessionStorage.getItem('user_id');
    if (!userId) {
        displayResult('mealResults', '⚠️ Please login to get personalized recommendations', false);
        return;
    }

    displayResult('mealResults', '🤖 Generating your personalized meal plan...', true);

    const result = await makeAPICall('/recommendations', { user_id: userId });
    
    if (result.success) {
        displayResult('mealResults', 
            `✅ Your daily meal plan (${result.data.daily_calorie_goal} calories)`, true);
        displayMealPlan(result.data);
    } else {
        displayResult('mealResults', `❌ ${result.data.error}`, false);
    }
}

// Display meal cards
function displayMealCards(meals) {
    const container = document.getElementById('mealCards');
    container.innerHTML = meals.map(meal => `
        <div class="meal-card" data-meal-id="${meal.id}">
            <h4><i class="fas fa-utensils"></i> ${meal.name}</h4>
            <div class="meal-info">
                <span class="meal-type">${meal.type.toUpperCase()}</span>
                <span class="calories">${meal.calories} kcal</span>
            </div>
            <div class="nutrition-grid">
                <div class="nutrition-item">
                    <i class="fas fa-drumstick-bite"></i>
                    <span>Protein: ${meal.protein}g</span>
                </div>
                <div class="nutrition-item">
                    <i class="fas fa-bread-slice"></i>
                    <span>Carbs: ${meal.carbs}g</span>
                </div>
                <div class="nutrition-item">
                    <i class="fas fa-cheese"></i>
                    <span>Fat: ${meal.fat}g</span>
                </div>
                <div class="nutrition-item">
                    <i class="fas fa-leaf"></i>
                    <span>Fiber: ${meal.fiber}g</span>
                </div>
            </div>
            <div class="meal-ingredients">
                <strong>Ingredients:</strong> ${meal.ingredients}
            </div>
            <div class="meal-serving">
                <strong>Serving:</strong> ${meal.serving_size}
            </div>
            ${meal.allergens && meal.allergens !== 'None' ? 
                `<div class="meal-allergens">⚠️ Contains: ${meal.allergens}</div>` : ''}
            <div class="meal-actions">
                <button onclick="addToHistory(${meal.id})" class="btn-secondary">
                    <i class="fas fa-plus"></i> Add to History
                </button>
                <small class="usda-ref">USDA ID: ${meal.usda_id}</small>
            </div>
        </div>
    `).join('');
}

// Display personalized meal plan
function displayMealPlan(planData) {
    const container = document.getElementById('mealCards');
    const mealPlan = planData.meal_plan;
    
    container.innerHTML = `
        <div class="meal-plan-header">
            <h3>🎯 Your Personalized Daily Meal Plan</h3>
            <p><strong>Target:</strong> ${planData.daily_calorie_goal} calories | <strong>BMI:</strong> ${planData.user_bmi}</p>
        </div>
        <div class="meal-plan-grid">
            ${Object.entries(mealPlan).map(([mealType, meal]) => {
                if (!meal) return `
                    <div class="meal-plan-card empty">
                        <h4><i class="fas fa-utensils"></i> ${mealType.toUpperCase()}</h4>
                        <p>No suitable meal found for your criteria</p>
                    </div>`;
                
                return `
                    <div class="meal-plan-card">
                        <h4><i class="fas fa-clock"></i> ${mealType.toUpperCase()}</h4>
                        <h5>${meal.name}</h5>
                        <div class="nutrition-summary">
                            <span class="calories">${meal.calories} kcal</span>
                            <div class="macros">
                                <span>P: ${meal.protein}g</span>
                                <span>C: ${meal.carbs}g</span>
                                <span>F: ${meal.fat}g</span>
                            </div>
                        </div>
                        <p class="ingredients">${meal.ingredients}</p>
                        <p class="serving"><strong>Serving:</strong> ${meal.serving_size}</p>
                        <button onclick="addToHistory(${meal.id})" class="btn-primary full-width">
                            <i class="fas fa-check"></i> Mark as Consumed
                        </button>
                    </div>`;
            }).join('')}
        </div>
        <div class="nutrition-tips">
            <h4><i class="fas fa-lightbulb"></i> Personalized Nutrition Tips</h4>
            <ul>
                ${planData.nutrition_tips.map(tip => `<li>${tip}</li>`).join('')}
            </ul>
        </div>
    `;
}

// Add meal to history
async function addToHistory(mealId) {
    const userId = sessionStorage.getItem('user_id');
    if (!userId) {
        alert('Please login to track your meals');
        return;
    }

    const result = await makeAPICall('/add_to_history', { 
        user_id: userId, 
        meal_id: mealId 
    });
    
    if (result.success) {
        // Visual feedback
        const button = event.target;
        const originalText = button.innerHTML;
        button.innerHTML = '<i class="fas fa-check"></i> Added!';
        button.style.background = '#28a745';
        
        setTimeout(() => {
            button.innerHTML = originalText;
            button.style.background = '';
        }, 2000);
    } else {
        alert('Failed to add meal to history');
    }
}

// Load user dashboard
async function loadUserDashboard() {
    const userId = sessionStorage.getItem('user_id');
    if (!userId) return;

    // Add recommendations button to meals tab
    const mealsTab = document.getElementById('meals-tab');
    const existingBtn = mealsTab.querySelector('.recommendations-btn');
    if (!existingBtn) {
        const recommendationsBtn = document.createElement('button');
        recommendationsBtn.className = 'btn-secondary full-width recommendations-btn';
        recommendationsBtn.innerHTML = '<i class="fas fa-robot"></i> Get AI Recommendations';
        recommendationsBtn.onclick = getRecommendations;
        recommendationsBtn.style.marginBottom = '20px';
        
        mealsTab.querySelector('.form-card').insertBefore(
            recommendationsBtn, 
            mealsTab.querySelector('form')
        );
    }
}

// Utility functions
function getBMICategory(bmi) {
    if (bmi < 18.5) return 'Underweight';
    if (bmi < 25) return 'Normal weight';
    if
