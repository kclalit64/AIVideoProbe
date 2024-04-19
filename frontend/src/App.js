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

/*To fetch requests from Flask backend in a component*/
// import React, { useState, useEffect } from 'react';

// function MyComponent() {
//   const [data, setData] = useState(null);

//   useEffect(() => {
//     fetchData();
//   }, []);

//   const fetchData = async () => {
//     try {
//       const response = await fetch('http://localhost:5000/api/data');
//       const jsonData = await response.json();
//       setData(jsonData);
//     } catch (error) {
//       console.error('Error fetching data:', error);
//     }
//   };

//   return (
//     <div>
//       {data && (
//         <div>
//           <h2>{data.message}</h2>
//         </div>
//       )}
//     </div>
//   );
// }

// export default MyComponent;
