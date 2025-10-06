import React, { useState, useEffect } from 'react';

export default function ProfilePage({ userId }) {
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: '',
    last_name: '',
    weight_kg: '',
    allergies: ''
  });
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchProfile();
  }, [userId]);

  const fetchProfile = async () => {
    try {
      const response = await fetch(`/api/profile?user_id=${userId}`);
      const data = await response.json();
      
      if (response.ok) {
        setProfile(data);
        setFormData({
          first_name: data.first_name || '',
          last_name: data.last_name || '',
          weight_kg: data.weight || '',
          allergies: data.allergies || ''
        });
      } else {
        setMessage('Failed to load profile');
      }
    } catch (error) {
      setMessage('Error loading profile');
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSave = async () => {
    try {
      const response = await fetch('/api/profile', {
      method: 'PUT',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          user_id: userId,
          ...formData
        })
      });

      const data = await response.json();
      
      if (response.ok) {
        setMessage('Profile updated successfully!');
        setEditing(false);
        fetchProfile(); // Refresh profile data
      } else {
        setMessage(data.error || 'Failed to update profile');
      }
    } catch (error) {
      setMessage('Error updating profile');
    }
  };

  const handleCancel = () => {
    setFormData({
      first_name: profile?.first_name || '',
      last_name: profile?.last_name || '',
      weight_kg: profile?.weight || '',
      allergies: profile?.allergies || ''
    });
    setEditing(false);
    setMessage('');
  };

  if (loading) {
    return <div>Loading profile...</div>;
  }

  if (!profile) {
    return <div>Profile not found</div>;
  }

  return (
    <div className="profile-page">
      <h2>Profile Page</h2>
      
      {message && (
        <div className={`msg ${message.includes('success') ? 'success' : 'error'}`}>
          {message}
        </div>
      )}

      <div style={{ marginBottom: '20px' }}>
        <h3>Personal Information</h3>
        
        <div className="profile-field">
          <label>
            First Name:
          </label>
          {editing ? (
            <input
              type="text"
              name="first_name"
              value={formData.first_name}
              onChange={handleInputChange}
            />
          ) : (
            <p>
              {profile.first_name}
            </p>
          )}
        </div>

        <div className="profile-field">
          <label>
            Last Name:
          </label>
          {editing ? (
            <input
              type="text"
              name="last_name"
              value={formData.last_name}
              onChange={handleInputChange}
            />
          ) : (
            <p>
              {profile.last_name}
            </p>
          )}
        </div>

        <div className="profile-field">
          <label>
            Email:
          </label>
          <p>
            {profile.email}
          </p>
        </div>

        <div className="profile-field">
          <label>
            Weight (kg):
          </label>
          {editing ? (
            <input
              type="number"
              name="weight_kg"
              value={formData.weight_kg}
              onChange={handleInputChange}
              min="1"
              max="500"
            />
          ) : (
            <p>
              {profile.weight} kg
            </p>
          )}
        </div>

        <div className="profile-field">
          <label>
            Allergies:
          </label>
          {editing ? (
            <textarea
              name="allergies"
              value={formData.allergies}
              onChange={handleInputChange}
              placeholder="Enter your allergies separated by commas"
              rows="3"
            />
          ) : (
            <p>
              {profile.allergies || 'No allergies specified'}
            </p>
          )}
        </div>
      </div>

      <div className="profile-buttons">
        {editing ? (
          <>
            <button onClick={handleSave} className="save">
              Save Changes
            </button>
            <button onClick={handleCancel} className="cancel">
              Cancel
            </button>
          </>
        ) : (
          <button onClick={() => setEditing(true)} className="edit">
            Edit Profile
          </button>
        )}
      </div>
    </div>
  );
}