import React, { useEffect, useState } from 'react';
import io from 'socket.io-client';

const SocketComponent = () => {
  const [processedData, setProcessedData] = useState('');

  const socket = io('http://localhost:5000/');  // Replace with your server URL
  useEffect(() => {
    // Connect to the Socket.IO server

    socket.on('connect', () => {
        console.log('Connected to the server');
    });

    socket.on("image",(data)=>{
        console.log(data);
        console.log(data.message);
    });
    // Listen for the 'processed_image' event
    socket.on('processed_image', (data) => {
      setProcessedData(data.processed_data);
    });

    // Clean up the socket connection on component unmount
    return () => {
      socket.disconnect();
    };
  }, [socket]);

  return (
    <div>
      {processedData && <img src={processedData} alt="Processed Image" />}
    </div>
  );
};

export default SocketComponent;