// src/App.js

import React from 'react';
import InputForm from './components/InputForm';
import VideoWindow from './components/VideoWindow'; 
import Results from './components/Results';
import './App.css';

const App = () => {
  return (
    <div className="app-container">
      <header>
        <title>InterviewForge - Home</title>
        <h1>InterviewForge</h1>
      </header>
      <main>
        <InputForm />
        <VideoWindow /> 
        <Results />
      </main>
      <footer>
        <p>&copy; 2024 InterviewForge. All rights reserved by <a href="https://saastalent.co/">SaaSTalent</a>.</p>
      </footer>
    </div>
  );
};

export default App;
