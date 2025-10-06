import React, { useEffect, useState } from 'react';

export default function ProfilePage({ userId }) {
  const [form, setForm] = useState({ first_name:'', last_name:'', weight:'', allergies:'' });
  const [msg, setMsg] = useState('');

  useEffect(() => {
    (async () => {
      const res = await fetch(`/api/profile?user_id=${userId}`);
      const data = await res.json();
      if (res.ok) {
        setForm({
          first_name: data.first_name || '',
          last_name: data.last_name || '',
          weight: data.weight || '',
          allergies: data.allergies || ''
        });
      }
    })();
  }, [userId]);

  const save = async () => {
    const res = await fetch('/api/profile', {
      method: 'PUT',
      headers: { 'Content-Type':'application/json' },
      body: JSON.stringify({ user_id: userId, ...form })
    });
    setMsg(res.ok ? 'Saved' : 'Save failed');
  };

  return (
    <div>
      <h2>الملف الشخصي</h2>
      <input placeholder="First Name" value={form.first_name} onChange={e=>setForm({...form, first_name:e.target.value})} />
      <input placeholder="Last Name" value={form.last_name} onChange={e=>setForm({...form, last_name:e.target.value})} />
      <input type="number" placeholder="Weight (kg)" value={form.weight} onChange={e=>setForm({...form, weight:e.target.value})} />
      <input placeholder="Allergies" value={form.allergies} onChange={e=>setForm({...form, allergies:e.target.value})} />
      <button onClick={save}>Save</button>
      <div>{msg}</div>
    </div>
  );
}


