import React, { useState } from 'react';

export default function LoginForm({ onLoggedIn }) {
  const [form, setForm] = useState({ email:'', password:'' });
  const [msg, setMsg] = useState('');

  const submit = async (e) => {
    e.preventDefault();
    setMsg('جارٍ الدخول...');
    const res = await fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify(form)
    });
    const data = await res.json();
    if (res.ok) {
      onLoggedIn && onLoggedIn({ userId: data.user_id, firstName: data.first_name, lastName: data.last_name });
      setMsg('');
    } else {
      setMsg(data.error || 'فشل تسجيل الدخول');
    }
  };

  return (
    <form onSubmit={submit}>
      <input placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} />
      <input type="password" placeholder="Password" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} />
      <button type="submit">Login</button>
      <div>{msg}</div>
    </form>
  );
}


