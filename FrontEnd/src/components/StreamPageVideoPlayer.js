import React, { useRef, useEffect, useState } from 'react';

function StreamPageVideoPlayer({ url, isStreamStopped,handleIsStreamStopped }) {
  // const videoURL = `http://localhost:5000/api/stream?source=${filename}&line1=${line1}&line2=${line2}&task=${task}`;
  const imgRef = useRef(null);
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
    handleIsStreamStopped(false);
};
const handleStop=(event)=>{
  event.preventDefault();
  const img = imgRef.current;
  img.src="";
  // handleIsStreamStopped(true);
};
  return (
    <div>
      <img ref={imgRef}  alt="Wait for detection .." style={{width: '1280px', height: '740px'}}/>
      <button onClick={handleRetry}>Retry</button>
      <button onClick={handleStop}>Stop Stream</button>
    </div>
  );
};

export default StreamPageVideoPlayer;
