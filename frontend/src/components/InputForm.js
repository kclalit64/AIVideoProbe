// src/components/InputForm.js

import React, { useState } from 'react';
import './InputForm.css'; 

const InputForm = () => {
  // State for form inputs
  const [name, setName] = useState('');
  const [jobTitle, setJobTitle] = useState('');
  const [jobDescription, setJobDescription] = useState('');
  const [resume, setResume] = useState(null);

  // Function to handle form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    // Add logic for backend
  };

  return (
    <div className="input-form-container">
      <h2>Let's Get You Ready!</h2>
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

        <label for="interviewer-select">
    Select Interviewer:
    <select id="interviewer-select" name="interviewer">
        <option value="Komal">Komal</option>
        <option value="Mayank">Mayank</option>
        <option value="Lalit">Lalit</option>
        <option value="Abhay">Abhay</option>
    </select>
</label>

        <button type="submit">Start Interview</button>
      </form>
    </div>
  );
};

export default InputForm;
