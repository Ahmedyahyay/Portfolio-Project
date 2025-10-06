import React, { useState } from 'react';

export default function AllergyPreferenceSelector({ onApply }) {
  const [specific, setSpecific] = useState('');

  const apply = () => {
    onApply && onApply({ specific_allergies: specific });
  };

  return (
    <div>
      <input
        placeholder="هل لديك حساسية من أطعمة أخرى؟ (افصل بينها بفاصلة)"
        value={specific}
        onChange={e=>setSpecific(e.target.value)}
      />
      <button onClick={apply}>Apply</button>
    </div>
  );
}


