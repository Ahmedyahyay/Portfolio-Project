import React, { useState } from 'react';
import RegistrationForm from './components/RegistrationForm.jsx';
import LoginForm from './components/LoginForm.jsx';
import BMIInput from './components/BMIInput.jsx';
import AllergyPreferenceSelector from './components/AllergyPreferenceSelector.jsx';
import ProfilePage from './components/ProfilePage.jsx';

export default function App() {
  const [auth, setAuth] = useState({ userId: null, firstName: '', lastName: '' });
  const [route, setRoute] = useState('home');
  const [prefs, setPrefs] = useState({ specific_allergies: '' });
  const [meals, setMeals] = useState([]);

  const fetchMeals = async () => {
    const res = await fetch('/api/meals', {
      method: 'POST',
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify({ ...prefs, max_calories: 600 })
    });
    const data = await res.json();
    setMeals(Array.isArray(data) ? data : []);
  };

  if (!auth.userId) {
    return (
      <div>
        <RegistrationForm onRegistered={()=>{}} />
        <LoginForm onLoggedIn={(u)=>{ setAuth(u); setRoute('dashboard'); }} />
      </div>
    );
  }

  return (
    <div>
      <nav>
        <button onClick={()=>setRoute('dashboard')}>Dashboard</button>
        <button onClick={()=>setRoute('profile')}>Profile</button>
        <button onClick={()=>{ setAuth({ userId:null, firstName:'', lastName:'' }); setRoute('home'); }}>Logout</button>
      </nav>
      {route === 'profile' ? (
        <ProfilePage userId={auth.userId} />
      ) : (
        <div>
          <h2>أهلاً, {auth.firstName} {auth.lastName}!</h2>
          <AllergyPreferenceSelector onApply={setPrefs} />
          <button onClick={fetchMeals}>Fetch Meals</button>
          <ul>
            {meals.map(m => (
              <li key={m.id}>{m.name} — {m.calories} kcal</li>
            ))}
          </ul>
          <BMIInput />
        </div>
      )}
    </div>
  );
}


