const API_BASE = 'http://127.0.0.1:5000';

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

// BMI Calculator function
async function calculateBMI() {
    const data = {
        height: parseFloat(document.getElementById('bmiHeight').value),
        weight: parseFloat(document.getElementById('bmiWeight').value)
    };

    if (!data.height || !data.weight) {
        displayResult('bmiResult', 'Please fill all fields', false);
        return;
    }

    const result = await makeAPICall('/calculate', data);
    
    if (result.success) {
        const bmi = result.data.BMI;
        let category = '';
        let eligible = '';
        
        if (bmi < 18.5) category = 'Underweight';
        else if (bmi < 25) category = 'Normal weight';
        else if (bmi < 30) category = 'Overweight';
        else category = 'Obese';
        
        eligible = bmi >= 30 ? ' - ✓ Eligible for nutrition assistance' : ' - Service for BMI ≥ 30';
        
        displayResult('bmiResult', `BMI: ${bmi} (${category})${eligible}`, true);
    } else {
        displayResult('bmiResult', `✗ ${result.data.error}`, false);
    }
}

// Clear results on page load
window.onload = function() {
    document.getElementById('regResult').innerHTML = '';
    document.getElementById('loginResult').innerHTML = '';
    document.getElementById('bmiResult').innerHTML = '';
};
