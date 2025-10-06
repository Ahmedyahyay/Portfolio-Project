import React, { useState } from 'react';

export default function RegistrationForm({ onRegistered }) {
  const [form, setForm] = useState({ first_name:'', last_name:'', email:'', password:'', height_cm:'', weight_kg:'' });
  const [msg, setMsg] = useState('');
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    
    // التحقق من أن جميع الحقول مملوءة
    if (!form.first_name || !form.last_name || !form.email || !form.password || !form.height_cm || !form.weight_kg) {
      setMsg('Please fill in all fields');
      return;
    }
    
    setLoading(true);
    setMsg('Registering...');
    
    try {
      const res = await fetch('/api/register', {
        method: 'POST',
        headers: { 'Content-Type':'application/json' },
        body: JSON.stringify({
          ...form,
          height_cm: Number(form.height_cm),
          weight_kg: Number(form.weight_kg)
        })
      });
      const data = await res.json();
      
      if (res.ok) {
        setMsg('Registration successful!');
        onRegistered && onRegistered(data);
      } else {
        if (data.details) {
          setMsg(`Validation errors: ${JSON.stringify(data.details)}`);
        } else {
          setMsg(data.error || 'Registration failed');
        }
      }
    } catch (error) {
      setMsg('Network error during registration');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <form onSubmit={submit}>
        <h3>Register</h3>
        <input placeholder="First Name" value={form.first_name} onChange={e=>setForm({...form, first_name:e.target.value})} required />
        <input placeholder="Last Name" value={form.last_name} onChange={e=>setForm({...form, last_name:e.target.value})} required />
        <input type="email" placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} required />
        <input type="password" placeholder="Password (min 8 chars, uppercase, lowercase, number)" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} required />
        <input type="number" placeholder="Height (cm)" value={form.height_cm} onChange={e=>setForm({...form, height_cm:e.target.value})} required />
        <input type="number" placeholder="Weight (kg)" value={form.weight_kg} onChange={e=>setForm({...form, weight_kg:e.target.value})} required />
        <button type="submit" disabled={loading}>
          {loading ? 'Registering...' : 'Register'}
        </button>
        {msg && <div className={`msg ${msg.includes('success') ? 'success' : msg.includes('error') ? 'error' : 'info'}`}>{msg}</div>}
      </form>
    </div>
  );
}


