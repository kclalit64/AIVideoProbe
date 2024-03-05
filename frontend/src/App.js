// src/App.js

import React from 'react';
import InputForm from './components/InputForm';
import VideoWindow from './components/VideoWindow'; // Import the VideoWindow component
import Results from './components/Results'; // Import the Results component
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
        <VideoWindow /> {/* Include the VideoWindow component */}
        <Results /> {/* Include the Results component */}
        {/* Add other components here if needed */}
      </main>
      <footer>
        <p>&copy; 2024 InterviewForge. All rights reserved by <a href="https://saastalent.co/">SaaSTalent</a>.</p>
      </footer>
    </div>
  );
};

export default App;
