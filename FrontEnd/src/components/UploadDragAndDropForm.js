import React, { useState, useRef } from "react";
import './UploadDragAndDropForm.css';
import axiosForm from "../types/AxiosType";
import { useNavigate } from "react-router-dom";

export default function UploadDragAndDropForm({ onFileSelect }) {
    
    const navigate = useNavigate();
    const [dragActive, setDragActive] = useState(false);
    const inputRef = useRef(null);
    const urlRef = useRef(null);
    
    const handleFile = (file) => {
        const formData = new FormData();
        formData.append("video", file);
        onFileSelect(file);
        axiosForm.post('/save_video', formData)
        .then((response)=>{
            if(response.status === 200){
                // navigate(`/stream?source=${file.name}`);
                console.log("File uploaded successfully");
            }
        })
        .catch(e=>console.log(e));
        
    };
    
    const handleDrag = function (e) {
        e.preventDefault();
        e.stopPropagation();
        if (e.type === "dragenter" || e.type === "dragover") {
            setDragActive(true);
        } else if (e.type === "dragleave") {
            setDragActive(false);
        }
    };

    const handleDrop = function (e) {
        e.preventDefault();
        e.stopPropagation();
        setDragActive(false);
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
            
        }
    };

    // triggers when file is selected with click
    const handleChange = function (e) {
        e.preventDefault();
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    };

    const handleUrlChange = function (e) {
        console.log(e.target.value);
    }

    // triggers the input when the button is clicked
    const onButtonClick = (e) => {
        e.preventDefault();
        inputRef.current.click();

    };

    const onWebcamButtonClick = (e) => {
        e.preventDefault();
    };





    return (
        <form id="form-file-upload" onDragEnter={handleDrag} >
            <input ref={inputRef} type="file" id="input-file-upload" multiple={false} onChange={handleChange} />
            <label id="label-file-upload" htmlFor="input-file-upload" className={dragActive ? "drag-active" : ""}>
                <div>
                    <p>Drag and drop Image / Video File </p>
                    <p>OR</p>
                    <p>Paste Youtube / Image URL</p>
                    <input ref={urlRef} type="url" id="source-url" onChange={handleUrlChange} placeholder="Paste a link.." />
                    <div id="buttons-area">
                        <button className="upload-button" onClick={onButtonClick}>Upload a file</button>
                        <button id="webcam-button" onClick={onWebcamButtonClick}>Webcam</button>
                    </div>
                    
                </div>
            </label>
            {dragActive && <div id="drag-file-element" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}></div>}
        </form>
    );

};