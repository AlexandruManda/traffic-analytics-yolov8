import React, { useRef, useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ReactPlayer from 'react-player';

export default function VideoPreview({ file,task, onLineDrawing, handleFileReset,handleUrl }) {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [startPoint, setStartPoint] = useState(null);
    const [lines, setLines] = useState([]);
    const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
    const [currentLine, setCurrentLine] = useState(null);
    const [isVideoLoaded, setIsVideoLoaded] = useState(false);

    const navigate = useNavigate();

    const buildURL = () => {
        let builtUrl = `/stream?source=${file?.name }`;
        lines.forEach((line, index) => {
            builtUrl += `&line${index + 1}=(${line.start.x},${line.start.y})(${line.end.x},${line.end.y})`;
        });
        builtUrl +=`&task=${task}`
        return builtUrl;
    };

    useEffect(() => {
        if (file) {
            const video = videoRef.current;
            video.onloadedmetadata = () => {
                setDimensions({ width: video.videoWidth, height: video.videoHeight });
            };
            const objectURL = URL.createObjectURL(file);
            video.src = objectURL;
            video.play();
            return () => {
                URL.revokeObjectURL(objectURL);
            };
        }
    }, [file]);

    useEffect(() => {
        if (!videoRef.current || !canvasRef.current) {
            return;
        }

        const video = videoRef.current;
        const canvas = canvasRef.current;
        const context = canvas.getContext('2d');

        const drawCanvas = () => {
            context.clearRect(0, 0, canvas.width, canvas.height);
            context.drawImage(video, 0, 0, canvas.width, canvas.height);
            if (currentLine) {
                context.beginPath();
                context.moveTo(currentLine.start.x, currentLine.start.y);
                context.lineTo(currentLine.end.x, currentLine.end.y);
                context.strokeStyle = 'red';
                context.lineWidth = 2;
                context.stroke();
            }
            for (const line of lines) {
                context.beginPath();
                context.moveTo(line.start.x, line.start.y);
                context.lineTo(line.end.x, line.end.y);
                context.strokeStyle = 'red';
                context.lineWidth = 5;
                context.stroke();
            }
        };

        if (lines.length === 2) {
            onLineDrawing(lines);
            const url = buildURL();
            handleUrl(url);
            handleFileReset();
            navigate(url);
        }

        const intervalId = setInterval(drawCanvas, 1000 / 30);
        return () => clearInterval(intervalId);
    }, [lines, currentLine, onLineDrawing, handleFileReset, navigate]);

    const handleMouseDown = (e) => {
        if (lines.length >= 2) {
            return;
        }
        const rect = canvasRef.current.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        setStartPoint({ x, y });
        setCurrentLine({ start: { x, y }, end: { x, y } });
    };

    const handleMouseUp = (e) => {
        if (lines.length >= 2) {
            return;
        }
        const rect = canvasRef.current.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        if (currentLine) {
            setLines([...lines, { start: currentLine.start, end: { x, y } }]);
            setCurrentLine(null);
        }
    };

    const handleMouseMove = (e) => {
        if (lines.length >= 2) {
            return;
        }
        if (!currentLine) {
            return;
        }
        const rect = canvasRef.current.getBoundingClientRect();
        const x = e.clientX - rect.left;
        const y = e.clientY - rect.top;
        setCurrentLine({ ...currentLine, end: { x, y } });
    };

    return (
        <div>
            {(file || isVideoLoaded) && (
                <div style={{ position: 'relative' }}>
                    {file && (
                        <video ref={videoRef} style={{ display: 'none' }} autoPlay muted loop />
                    )}
                    {isVideoLoaded && (
                        <ReactPlayer
                            ref={videoRef}
                            width="100%"
                            height="100%"
                            playing
                            controls
                        />
                    )}
                    <canvas
                        ref={canvasRef}
                        width={dimensions.width}
                        height={dimensions.height}
                        style={{ border: '1px solid black' }}
                        onMouseDown={handleMouseDown}
                        onMouseUp={handleMouseUp}
                        onMouseMove={handleMouseMove}
                    />
                    <button onClick={() => setLines([])}>Clear</button>
                </div>
            )}
        </div>
    );
}

