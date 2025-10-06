import React, { useState } from 'react';
import RegistrationForm from './components/RegistrationForm.jsx';
import LoginForm from './components/LoginForm.jsx';
import BMIInput from './components/BMIInput.jsx';
import AllergyPreferenceSelector from './components/AllergyPreferenceSelector.jsx';
import ProfilePage from './components/ProfilePage.jsx';
import './styles.css';

export default function App() {
  const [auth, setAuth] = useState({ userId: null, firstName: '', lastName: '', fullName: '', email: '', bmi: null });
  const [route, setRoute] = useState('home');
  const [prefs, setPrefs] = useState({ specific_allergies: '' });
  const [meals, setMeals] = useState([]);
  const [bmiData, setBmiData] = useState(null);

  const fetchMeals = async () => {
    if (!auth.userId) return;
    
    const res = await fetch(`/api/meals?user_id=${auth.userId}`, {
      method: 'GET',
      headers: { 'Content-Type':'application/json' }
    });
    const data = await res.json();
    setMeals(data.meals || []);
  };

  const calculateBMI = async (height, weight) => {
    const res = await fetch('/api/bmi', {
      method: 'POST',
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify({ height_cm: height, weight_kg: weight })
    });
    const data = await res.json();
    setBmiData(data);
    return data;
  };

  if (!auth.userId) {
    return (
      <div>
        <RegistrationForm onRegistered={(userData) => {
          setAuth({
            userId: userData.user_id,
            firstName: userData.first_name,
            lastName: userData.last_name,
            fullName: userData.full_name,
            email: userData.email || '',
            bmi: userData.bmi
          });
          setRoute('dashboard');
        }} />
        <LoginForm onLoggedIn={(u)=>{ setAuth(u); setRoute('dashboard'); }} />
      </div>
    );
  }

  return (
    <div className="container">
      <nav>
        <button onClick={()=>setRoute('dashboard')}>Dashboard</button>
        <button onClick={()=>setRoute('profile')}>Profile</button>
        <button className="logout" onClick={()=>{ setAuth({ userId:null, firstName:'', lastName:'', fullName:'', email:'', bmi:null }); setRoute('home'); }}>Logout</button>
      </nav>
      {route === 'profile' ? (
        <ProfilePage userId={auth.userId} />
      ) : (
        <div className="dashboard">
          <h2>Hello, {auth.fullName || `${auth.firstName} ${auth.lastName}`} 👋</h2>
          <AllergyPreferenceSelector onApply={setPrefs} />
          <button onClick={fetchMeals}>Get Meal Recommendations</button>
          {meals.length > 0 && (
            <div className="meals-list">
              <h3>Recommended Meals</h3>
              <ul>
                {meals.map(m => (
                  <li key={m.id} className={m.uncertain_allergens ? 'uncertain' : ''}>
                    <strong>{m.name}</strong> — {m.calories} kcal ({m.type})
                    {m.uncertain_allergens && <span> ⚠️ Uncertain allergens</span>}
                  </li>
                ))}
              </ul>
            </div>
          )}
          <BMIInput onCalculate={calculateBMI} bmiData={bmiData} />
        </div>
      )}
    </div>
  );
}


