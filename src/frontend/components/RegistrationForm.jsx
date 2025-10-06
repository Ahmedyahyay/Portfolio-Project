import React, { useState } from 'react';

export default function RegistrationForm({ onRegistered }) {
  const [form, setForm] = useState({ first_name:'', last_name:'', email:'', password:'', height:'', weight:'' });
  const [msg, setMsg] = useState('');

  const submit = async (e) => {
    e.preventDefault();
    setMsg('جارٍ الإرسال...');
    const res = await fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify({
        ...form,
        height: Number(form.height),
        weight: Number(form.weight)
      })
    });
    const data = await res.json();
    if (res.ok) {
      setMsg('تم التسجيل بنجاح');
      onRegistered && onRegistered();
    } else {
      setMsg(data.error || 'فشل التسجيل');
    }
  };

  return (
    <form onSubmit={submit}>
      <input placeholder="First Name" value={form.first_name} onChange={e=>setForm({...form, first_name:e.target.value})} />
      <input placeholder="Last Name" value={form.last_name} onChange={e=>setForm({...form, last_name:e.target.value})} />
      <input placeholder="Email" value={form.email} onChange={e=>setForm({...form, email:e.target.value})} />
      <input type="password" placeholder="Password" value={form.password} onChange={e=>setForm({...form, password:e.target.value})} />
      <input type="number" placeholder="Height (cm)" value={form.height} onChange={e=>setForm({...form, height:e.target.value})} />
      <input type="number" placeholder="Weight (kg)" value={form.weight} onChange={e=>setForm({...form, weight:e.target.value})} />
      <button type="submit">Register</button>
      <div>{msg}</div>
    </form>
  );
}


