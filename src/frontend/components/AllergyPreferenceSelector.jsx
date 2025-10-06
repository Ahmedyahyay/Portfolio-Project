import React, { useState } from 'react';

export default function AllergyPreferenceSelector({ onApply }) {
  const [allergies, setAllergies] = useState([]);
  const [preferences, setPreferences] = useState([]);
  const [customAllergy, setCustomAllergy] = useState('');
  const [customPreference, setCustomPreference] = useState('');

  const commonAllergies = [
    'Dairy', 'Nuts', 'Peanuts', 'Eggs', 'Soy', 'Wheat', 'Fish', 'Shellfish', 'Sesame'
  ];

  const commonPreferences = [
    'Vegetarian', 'Vegan', 'Gluten-Free', 'Low-Carb', 'High-Protein', 'Mediterranean', 'Keto'
  ];

  const toggleAllergy = (allergy) => {
    setAllergies(prev => 
      prev.includes(allergy) 
        ? prev.filter(a => a !== allergy)
        : [...prev, allergy]
    );
  };

  const togglePreference = (preference) => {
    setPreferences(prev => 
      prev.includes(preference) 
        ? prev.filter(p => p !== preference)
        : [...prev, preference]
    );
  };

  const addCustomAllergy = () => {
    if (customAllergy.trim() && !allergies.includes(customAllergy.trim())) {
      setAllergies(prev => [...prev, customAllergy.trim()]);
      setCustomAllergy('');
    }
  };

  const addCustomPreference = () => {
    if (customPreference.trim() && !preferences.includes(customPreference.trim())) {
      setPreferences(prev => [...prev, customPreference.trim()]);
      setCustomPreference('');
    }
  };

  const handleApply = () => {
    const data = {
      specific_allergies: allergies.join(','),
      preferences: preferences.join(',')
    };
    onApply && onApply(data);
  };

  return (
    <div className="allergy-selector">
      <h3>Allergies & Food Preferences</h3>
      
      <div style={{ marginBottom: '20px' }}>
        <h4>Allergies</h4>
        <div className="allergy-buttons">
          {commonAllergies.map(allergy => (
            <button
              key={allergy}
              type="button"
              onClick={() => toggleAllergy(allergy)}
              className={allergies.includes(allergy) ? 'selected' : ''}
            >
              {allergy}
            </button>
          ))}
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <input
            type="text"
            value={customAllergy}
            onChange={(e) => setCustomAllergy(e.target.value)}
            placeholder="Add custom allergy"
            style={{ padding: '5px', flex: 1 }}
          />
          <button type="button" onClick={addCustomAllergy} style={{ padding: '5px 10px' }}>
            Add
          </button>
        </div>
      </div>

      <div style={{ marginBottom: '20px' }}>
        <h4>Food Preferences</h4>
        <div className="allergy-buttons">
          {commonPreferences.map(preference => (
            <button
              key={preference}
              type="button"
              onClick={() => togglePreference(preference)}
              className={`preference ${preferences.includes(preference) ? 'selected' : ''}`}
            >
              {preference}
            </button>
          ))}
        </div>
        <div style={{ display: 'flex', gap: '8px' }}>
          <input
            type="text"
            value={customPreference}
            onChange={(e) => setCustomPreference(e.target.value)}
            placeholder="Add custom preference"
            style={{ padding: '5px', flex: 1 }}
          />
          <button type="button" onClick={addCustomPreference} style={{ padding: '5px 10px' }}>
            Add
          </button>
        </div>
      </div>

      <button 
        onClick={handleApply}
        style={{
          padding: '10px 20px',
          backgroundColor: '#007bff',
          color: 'white',
          border: 'none',
          borderRadius: '5px',
          cursor: 'pointer'
        }}
      >
        Apply Preferences
      </button>

      {(allergies.length > 0 || preferences.length > 0) && (
        <div className="selected-items">
          <h4>Selected:</h4>
          {allergies.length > 0 && (
            <p><strong>Allergies:</strong> {allergies.join(', ')}</p>
          )}
          {preferences.length > 0 && (
            <p><strong>Preferences:</strong> {preferences.join(', ')}</p>
          )}
        </div>
      )}
    </div>
  );
}