import React, { useRef, useEffect, useState } from 'react';

function StreamPageVideoPlayer({ filename, line1, line2, isStreamStopped }) {
  const videoURL = `http://localhost:5000/api/stream?source=${filename}&line1=${line1}&line2=${line2}`;
  const imgRef = useRef(null);

  useEffect(() => {
    const imgDisplay = imgRef.current;
    if (imgDisplay) {
      imgDisplay.src = isStreamStopped ? "" : videoURL;
    }

    return () => {
      if (imgDisplay) {
        imgDisplay.src = "";
      }
    };
  }, [isStreamStopped, imgRef]);

  return (
    <div>
      <img ref={imgRef} alt="Wait for detection .." />
    </div>
  );
};

export default StreamPageVideoPlayer;
