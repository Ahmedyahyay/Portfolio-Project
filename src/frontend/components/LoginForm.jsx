import React, { useState } from 'react';

export default function LoginForm({ onLoggedIn }) {
  const [form, setForm] = useState({ email:'', password:'' });
  const [msg, setMsg] = useState('');
  const [loading, setLoading] = useState(false);

  const submit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setMsg('Logging in...');
    
    try {
      const res = await fetch('/api/login', {
        method: 'POST',
        headers: { 'Content-Type':'application/json' },
        body: JSON.stringify(form)
      });
      const data = await res.json();
      
      if (res.ok) {
        onLoggedIn && onLoggedIn({ 
          userId: data.user_id, 
          firstName: data.first_name, 
          lastName: data.last_name,
          fullName: data.full_name,
          email: data.email,
          bmi: data.bmi
        });
        setMsg('');
      } else {
        setMsg(data.error || 'Login failed');
      }
    } catch (error) {
      setMsg('Network error during login');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <form onSubmit={submit}>
        <h3>Login</h3>
        <input type="email" placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} required />
        <input type="password" placeholder="Password" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} required />
        <button type="submit" disabled={loading}>
          {loading ? 'Logging in...' : 'Login'}
        </button>
        {msg && <div className={`msg ${msg.includes('success') ? 'success' : msg.includes('error') ? 'error' : 'info'}`}>{msg}</div>}
      </form>
    </div>
  );
}


