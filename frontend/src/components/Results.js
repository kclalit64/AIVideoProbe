import React, { useState } from 'react';
import './Results.css';

const Results = () => {
  // State to control the visibility of the Results component
  const [showResults, setShowResults] = useState(false);

  // Function to handle downloading the PDF file
  const downloadPDF = () => {
    // Replace 'result.pdf' with the actual path to your PDF file
    const pdfPath = 'result.pdf';
    window.open(pdfPath, '_blank');
  };

  return (
    <div>
      <button onClick={() => setShowResults(true)}>Show Results</button>
    </div>
  );
};

export default Results;
