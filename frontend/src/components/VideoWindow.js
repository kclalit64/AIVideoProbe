import React, { useEffect } from 'react';
import './VideoWindow.css'; // Import the CSS file for styling

const VideoWindow = () => {
  useEffect(() => {
    // Function to start capturing the live video stream from the front camera
    const startVideoStream = async () => {
      try {
        // Access the user's camera
        const stream = await navigator.mediaDevices.getUserMedia({ video: { facingMode: 'user' }, audio: false });
        const videoElement = document.getElementById('self-video');

        if (videoElement) {
          // Attach the stream to the video element
          videoElement.srcObject = stream;
        }
      } catch (error) {
        console.error('Error accessing the camera:', error);
      }
    };

    // Call the function to start capturing the video stream
    startVideoStream();

    // Cleanup function to stop the video stream when component unmounts
    return () => {
      const videoElement = document.getElementById('self-video');
      if (videoElement && videoElement.srcObject) {
        const stream = videoElement.srcObject;
        const tracks = stream.getTracks();
        tracks.forEach(track => track.stop());
      }
    };
  }, []);

  return (
    <div className="video-window-container">
      <div className="ai-image">
        {/* Placeholder for AI image */}
        <img src="path/to/ai-image.jpg" alt="AI" />
      </div>
      <div className="user-video">
        {/* Placeholder for user's self-reflection video */}
        <video id="self-video" autoPlay muted>
          {/* This video element will be populated with the live video stream */}
          Your browser does not support the video tag.
        </video>
      </div>
    </div>
  );
};

export default VideoWindow;
