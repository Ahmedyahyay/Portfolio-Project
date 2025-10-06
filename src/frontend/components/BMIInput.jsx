import React, { useState } from 'react';

export default function BMIInput({ onCalculate, bmiData }) {
  const [height, setHeight] = useState('');
  const [weight, setWeight] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!height || !weight) return;
    
    setLoading(true);
    try {
      const result = await onCalculate(Number(height), Number(weight));
      // BMI data will be displayed via bmiData prop
    } catch (error) {
      console.error('BMI calculation error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="bmi-calculator">
      <h3>BMI Calculator</h3>
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: '10px' }}>
          <label>Height (cm):</label>
          <input
            type="number"
            value={height}
            onChange={(e) => setHeight(e.target.value)}
            placeholder="Enter height in cm"
            min="1"
            max="300"
            required
            style={{ marginLeft: '10px', padding: '5px' }}
          />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label>Weight (kg):</label>
          <input
            type="number"
            value={weight}
            onChange={(e) => setWeight(e.target.value)}
            placeholder="Enter weight in kg"
            min="1"
            max="500"
            required
            style={{ marginLeft: '10px', padding: '5px' }}
          />
        </div>
        <button type="submit" disabled={loading} style={{ padding: '8px 16px' }}>
          {loading ? 'Calculating...' : 'Calculate BMI'}
        </button>
      </form>
      
      {bmiData && (
        <div className="bmi-result">
          <h4>BMI Result</h4>
          <p><strong>BMI:</strong> {bmiData.bmi}</p>
          <p><strong>Status:</strong> {bmiData.eligibility ? 'Overweight (BMI ≥ 30)' : 'Normal/Underweight'}</p>
          <p><strong>Message:</strong> {bmiData.message}</p>
        </div>
      )}
    </div>
  );
}