import React, { useRef, useState, useEffect } from 'react';
import { useNavigate } from "react-router-dom";

export default function VideoPreview({ file }) {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [startPoint, setStartPoint] = useState(null);
    const [lines, setLines] = useState([]);
    const [dimensions, setDimensions] = useState({ width: 0, height: 0 });
    const [currentLine, setCurrentLine] = useState(null);

    const navigate = useNavigate();
    // URL Building function
    const buildURL = () => {
        let url = `/stream?source=${file.name}`;
        lines.forEach((line, index) => {
            url += `&line${index + 1}=(${line.start.x},${line.start.y})(${line.end.x},${line.end.y})`;
        });
        return url;
    };
    

    useEffect(() => {
        if (!file) {
            return;
        }

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
            // replace '/path-to-navigate' with the path you want to navigate to when two lines are drawn
            console.log('hello')
            // console.log(lines);
            const url = buildURL();
            console.log(url);
            navigate(url);
        }

        const intervalId = setInterval(drawCanvas, 1000 / 30);
        return () => clearInterval(intervalId);
    }, [lines]);

    //% gets triggered when the mouse click button is pressed
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

    //? gets triggered when the mouse click button is released
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

    //? gets triggered when the mouse is moved
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
            <video ref={videoRef} style={{ display: 'none' }} autoPlay muted loop />
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
    );
}
