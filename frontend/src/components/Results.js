// src/components/Results.js

import React, { useState } from 'react';
import './Results.css';

const Results = () => {
  // Mock data 
  const technicalResults = [
    { skill: 'Reactjs', score: 90, feedback: 'You were good with React basics...' },
    // Add more skills and results as needed
  ];

  const behavioralResults = [
    { skill: 'Communication', score: 85, feedback: 'You demonstrated strong communication skills...' },
    // Add more skills and results as needed
  ];

  const problemSolvingResults = [
    { skill: 'Analytical Thinking', score: 95, feedback: 'Impressive analytical thinking...' },
    // Add more skills and results as needed
  ];

  const culturalFitResults = [
    { skill: 'Alignment with Values', score: 80, feedback: 'You showed good alignment with our company values...' },
    // Add more skills and results as needed
  ];

  const workExperienceResults = [
    { skill: 'Relevant Experience', score: 88, feedback: 'Your past experiences are highly relevant to the role...' },
    // Add more skills and results as needed
  ];

  // State to control the visibility of the Results component
  const [showResults, setShowResults] = useState(false);

  return (
    <div>
      <button onClick={() => setShowResults(true)}>Show Results</button>

      {showResults && (
        <div className="results-container">
          <section className="result-section">
            <div className="result-pane technical-pane">
              <h2>Technical Performance</h2>
              {technicalResults.map((result, index) => (
                <div key={index}>
                  <h3>{result.skill}: Score = {result.score}%</h3>
                  <p>Metrics of Evaluation:</p>
                  <ul>
                    <li>Basics</li>
                    <li>ReactDOM</li>
                    <li>Components in React</li>
                  </ul>
                  <div className="feedback">
                    <p>{result.feedback}</p>
                  </div>
                </div>
              ))}
            </div>
            
          </section>
        </div>
      )}
    </div>
  );
};

export default Results;
