// src/components/VideoWindow.js

import React from 'react';
//import '/VideoWindow.css'; // Import the CSS file for styling

const VideoWindow = () => {
  return (
    <div className="video-window-container">
      <div className="ai-image">
        {/* Placeholder for AI image */}
        <img src="path/to/ai-image.jpg" alt="AI" />
      </div>
      <div className="user-video">
        {/* Placeholder for user's self-reflection video */}
        {/* You can use HTML5 video tag or any other video component here */}
        <video controls>
          <source src="path/to/user-video.mp4" type="video/mp4" />
          Your browser does not support the video tag.
        </video>
      </div>
    </div>
  );
};

export default VideoWindow;
