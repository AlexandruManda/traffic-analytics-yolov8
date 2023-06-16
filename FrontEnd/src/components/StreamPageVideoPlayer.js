import React, { useRef, useEffect, useState } from 'react';
import './StreamPageVideoPlayer.css';
import loadingSpinner from './../assets/loading.gif'; // replace with your own spinner

function StreamPageVideoPlayer({ url, isStreamStopped }) {
  // const videoURL = `http://localhost:5000/api/stream?source=${filename}&line1=${line1}&line2=${line2}&task=${task}`;
  const imgRef = useRef(null);
  const [isLoading, setIsLoading] = useState(true);
  const videoUrl= `http://localhost:5000/api` + url

  useEffect(() => {
    const imgDisplay = imgRef.current;
    if (imgDisplay) {
      imgDisplay.src = isStreamStopped ? "" : videoUrl;
    }
    // console.log(url);
    return () => {
      if (imgDisplay) {
        imgDisplay.src = "";
      }
    };

  }, [isStreamStopped,url]);

  const handleRetry = (event)=>{
    event.preventDefault();
    const img = imgRef.current;
    // img.src="";
    img.src = videoUrl;
    setIsLoading(true);
  };

  const handleStop=(event)=>{
    event.preventDefault();
    const img = imgRef.current;
    img.src="";
    setIsLoading(true);
  };

  const handleImageLoad = () => {
    setIsLoading(false);
  };

  return (
    <div className="stream-container">
      {isLoading && <img src={loadingSpinner} className="loading-spinner" alt="Loading..." />}
      <img 
        ref={imgRef} 
        className="stream-img" 
        alt="Wait for detection .."
        style={{display: isLoading ? 'none' : 'block'}}
        onLoad={handleImageLoad}
      />
      <div className="button-container">
        <button onClick={handleRetry} className="retry-button">Retry</button>
        <button onClick={handleStop} className="stop-button">Stop Stream</button>
      </div>
    </div>
  );
};

export default StreamPageVideoPlayer;
