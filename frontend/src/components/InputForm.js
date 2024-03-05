// src/components/InputForm.js

import React, { useState } from 'react';
import './InputForm.css'; // Import the CSS file for styling

const InputForm = () => {
  // State for form inputs
  const [name, setName] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [resume, setResume] = useState(null);

  // Function to handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // Add logic to handle form submission (send data to backend, etc.)
  };

  return (
    <div className="input-form-container">
      <h2>Let's </h2>
      <form onSubmit={handleSubmit}>
        <label>
          Your Name:
          <input type="text" value={name} onChange={(e) => setName(e.target.value)} />
        </label>

        <label>
          Aspiring Job Title:
          <input type="text" value={jobTitle} onChange={(e) => setJobTitle(e.target.value)} />
        </label>

        <label>
          Job Description:
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
          />
        </label>

        <label>
          Upload Resume (PDF/WORD):
          <input type="file" onChange={(e) => setResume(e.target.files[0])} />
        </label>

        <button type="submit">Start Interview</button>
      </form>
    </div>
  );
};

export default InputForm;
