import React, { useState } from 'react';

export default function BMIInput() {
  const [h, setH] = useState('');
  const [w, setW] = useState('');
  const [res, setRes] = useState('');

  const calc = () => {
    const height = Number(h);
    const weight = Number(w);
    if (!height || !weight) {
      setRes('الرجاء إدخال الطول والوزن');
      return;
    }
    const bmi = weight / ((height/100)**2);
    const msg = bmi >= 30
      ? "Your BMI indicates that you’re in the overweight range. Don’t worry — small, consistent steps can lead to big changes! 💪 Keep going!"
      : "Great job maintaining a healthy weight! Keep up your balanced habits 🌿";
    setRes(`BMI: ${bmi.toFixed(2)} — ${msg}`);
  };

  return (
    <div>
      <input type="number" placeholder="Height (cm)" value={h} onChange={e=>setH(e.target.value)} />
      <input type="number" placeholder="Weight (kg)" value={w} onChange={e=>setW(e.target.value)} />
      <button onClick={calc}>Calculate BMI</button>
      <div>{res}</div>
    </div>
  );
}


