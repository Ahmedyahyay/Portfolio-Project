// Simple simulated state
let isAuthenticated = false;
let currentUser = { id: 1, email: 'user@example.com' };

// Nav elements
const navLogin = document.getElementById('navLogin');
const navRegister = document.getElementById('navRegister');
const navLogout = document.getElementById('navLogout');
const navWelcome = document.getElementById('navWelcome');

// Cards
const loginCard = document.getElementById('loginCard');
const registerCard = document.getElementById('registerCard');
const mealCard = document.getElementById('mealCard');
const bmiCard = document.getElementById('bmiCard');

// Auth fields
const loginEmail = document.getElementById('loginEmail');
const loginPassword = document.getElementById('loginPassword');
const regEmail = document.getElementById('regEmail');
const regPassword = document.getElementById('regPassword');

// Buttons and messages
const btnLogin = document.getElementById('btnLogin');
const btnRegister = document.getElementById('btnRegister');
const loginMsg = document.getElementById('loginMsg');
const registerMsg = document.getElementById('registerMsg');

// Meal suggestion elements
const maxCalories = document.getElementById('maxCalories');
const btnSuggest = document.getElementById('btnSuggest');
const suggestError = document.getElementById('suggestError');
const results = document.getElementById('results');

// BMI elements
const bmiHeight = document.getElementById('bmiHeight');
const bmiWeight = document.getElementById('bmiWeight');
const btnCalcBMI = document.getElementById('btnCalcBMI');
const bmiResult = document.getElementById('bmiResult');

function renderUI() {
  if (isAuthenticated) {
    loginCard.classList.add('hidden');
    registerCard.classList.add('hidden');
    mealCard.classList.remove('hidden');
    bmiCard.classList.remove('hidden');
    navLogin.classList.add('hidden');
    navRegister.classList.add('hidden');
    navLogout.classList.remove('hidden');
    navWelcome.classList.remove('hidden');
    navWelcome.textContent = `أهلاً، ${currentUser.email}`;
  } else {
    loginCard.classList.remove('hidden');
    registerCard.classList.remove('hidden');
    mealCard.classList.add('hidden');
    bmiCard.classList.add('hidden');
    navLogin.classList.remove('hidden');
    navRegister.classList.remove('hidden');
    navLogout.classList.add('hidden');
    navWelcome.classList.add('hidden');
    navWelcome.textContent = '';
  }
}

navLogin.addEventListener('click', () => {
  isAuthenticated = true;
  renderUI();
});
navRegister.addEventListener('click', () => {
  isAuthenticated = true;
  renderUI();
});
navLogout.addEventListener('click', () => {
  isAuthenticated = false;
  renderUI();
});

btnLogin.addEventListener('click', () => {
  if (!loginEmail.value || !loginPassword.value) {
    loginMsg.textContent = 'يرجى إدخال البريد وكلمة المرور';
    return;
  }
  loginMsg.textContent = '';
  isAuthenticated = true;
  currentUser.email = loginEmail.value;
  renderUI();
});

btnRegister.addEventListener('click', () => {
  if (!regEmail.value || !regPassword.value) {
    registerMsg.textContent = 'يرجى إدخال البريد وكلمة المرور';
    return;
  }
  registerMsg.textContent = '';
  isAuthenticated = true;
  currentUser.email = regEmail.value;
  renderUI();
});

btnSuggest.addEventListener('click', () => {
  suggestError.textContent = '';
  results.innerHTML = '';
  const max = Number(maxCalories.value);
  if (!max) {
    suggestError.textContent = 'Please enter max calories';
    return;
  }
  // Simulate an API call
  setTimeout(() => {
    const allMeals = [
      { name: 'Grilled Chicken Salad', calories: 450, ingredients: 'chicken, lettuce, tomato, olive oil' },
      { name: 'Oatmeal with Berries', calories: 320, ingredients: 'oats, milk, blueberries' },
      { name: 'Salmon with Quinoa', calories: 520, ingredients: 'salmon, quinoa, lemon' },
      { name: 'Veggie Omelette', calories: 300, ingredients: 'eggs, bell pepper, spinach' },
    ];
    const meals = allMeals.filter(m => m.calories <= max);
    if (meals.length === 0) {
      results.innerHTML = '<div class="subtle">لا توجد وجبات ضمن الحد الأقصى للسعرات.</div>';
      return;
    }
    for (const m of meals) {
      const div = document.createElement('div');
      div.className = 'meal-item';
      div.innerHTML = `<h3>${m.name}</h3><div class="subtle">${m.calories} kcal</div><div class="subtle">${m.ingredients}</div>`;
      results.appendChild(div);
    }
  }, 500);
});

btnCalcBMI.addEventListener('click', () => {
  const h = Number(bmiHeight.value);
  const w = Number(bmiWeight.value);
  if (!h || !w) {
    bmiResult.textContent = 'الرجاء إدخال الطول والوزن';
    return;
  }
  const bmi = (w / ((h / 100) ** 2));
  const msg = bmi >= 30
    ? "Your BMI indicates that you’re in the overweight range. Don’t worry — small, consistent steps can lead to big changes! 💪 Keep going!"
    : "Great job maintaining a healthy weight! Keep up your balanced habits 🌿";
  bmiResult.textContent = `BMI: ${bmi.toFixed(2)} — ${msg}`;
});

renderUI();
