import React, { useState, useRef, useEffect } from "react";
import './UploadDragAndDropForm.css';
import Axios from "../types/AxiosType";
import { useNavigate } from "react-router-dom";
import { FaCamera, FaFileUpload, FaUpload, FaYoutube, FaTimesCircle } from "react-icons/fa";

export default function UploadDragAndDropForm({ task, onFileSelect, handleUrl }) {

    const navigate = useNavigate();
    const [dragActive, setDragActive] = useState(false);
    const [inputValid, setInputValid] = useState(true);
    const [validationMessage, setValidationMessage] = useState("");

    const inputRef = useRef(null);
    const urlRef = useRef(null);

    useEffect(() => {
        // If task changes, clear the input
        if (urlRef.current) {
            urlRef.current.value = "";
        }
    }, [task]);

    const validateUrl = (url) => {
        if (url !== undefined && url !== '') {
            const youtubeRegExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
            const udpOrRtspRegExp = /^(udp|rtsp):\/\/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$/;
            const videoFileRegExp = /^.*\.(mp4|avi|mkv|flv|wmv)$/;

            const matchYouTube = url.match(youtubeRegExp);
            const matchUdpRtsp = url.match(udpOrRtspRegExp);
            const matchVideoFile = url.match(videoFileRegExp);

            return ((matchYouTube && matchYouTube[2].length === 11) || matchUdpRtsp || matchVideoFile);
        }
        return false;
    }

    const handleFile = (file) => {
        const formData = new FormData();
        formData.append("video", file);
        const newUrl = `/stream?source=${file.name}&task=${task}`;
        Axios.axiosForm.post('/save_video', formData)
            .then((response) => {
                if (response.status === 200) {
                    if (inputRef.current) {
                        inputRef.current.value = "";
                    }
                    console.log("Video uploaded successfully ! ");
                    onFileSelect(file);
                    handleUrl(newUrl);
                    // navigate(newUrl)
                }
            })
            .catch(e => console.log(e));
    };
    const getFileNameFromHeaders = (headers) => {
        const contentDispositionHeader = headers['content-disposition'];
        if (contentDispositionHeader) {
            const filenameMatch = contentDispositionHeader.match(/filename="(.+)"/);
            if (filenameMatch && filenameMatch.length > 1) {
                return filenameMatch[1];
            }
        }
        return 'youtube_video.mp4'; // Default filename if extraction fails
    };
    const handleYouTubeDownload = () => {
        const youtubeUrl = urlRef.current.value;
        if (youtubeUrl) {
            Axios.axiosInstance.get('/download', {
                params: {
                    url: youtubeUrl
                },
                responseType: 'blob'
            })
                .then(response => {
                    const file = new File([response.data], getFileNameFromHeaders(response.headers), { type: 'video/mp4' });
                    console.log(file);
                    onFileSelect(file);
                    const url = `/stream?source=${youtubeUrl}&task=${task}`;
                    handleUrl(url);
                })
                .catch(error => {
                    console.log(error);
                });
        }
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
        const inputURL = e.target.value;
        if (!validateUrl(inputURL)) {
            setInputValid(false);
            setValidationMessage("Input is not a valid URL or YouTube link.");


        } else {
            console.log('Valid YouTube URL');
            setInputValid(true);
            setValidationMessage("");
            const udpOrRtspRegExp = /^(udp|rtsp):\/\/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$/;
            const matchUdpRtsp = inputURL.match(udpOrRtspRegExp);
            const processedUrl = `/stream?source=${encodeURI(inputURL)}&task=${task}`
            handleUrl(processedUrl);
            if (matchUdpRtsp) {
                // for udp and rtsp, navigate to a new page

            } else {
                // for youtube url, download the video
                handleYouTubeDownload(inputURL);

            }
        }

    };

    // triggers the input when the button is clicked
    const onButtonClick = (e) => {
        e.preventDefault();
        if (inputRef.current) {
            inputRef.current.click();
        }
    };

    const onWebcamButtonClick = (e) => {
        e.preventDefault();
        const url = `/stream?source=${0}&task=${task}`;
        handleUrl(url);
    };

    const clearUrlInput = (event) => {
        event.preventDefault();
        urlRef.current.value = '';
    };
    return (
        <form id="form-file-upload" onDragEnter={handleDrag} >
            <input ref={inputRef} type="file" id="input-file-upload" multiple={false} onChange={handleChange} />
            <label id="label-file-upload" htmlFor="input-file-upload" className={dragActive ? "drag-active" : ""}>
                <div>
                    <p><FaUpload /> Drag and drop Image / Video File </p>
                    <p>OR</p>
                    <p><FaYoutube /> Paste Youtube / Image URL</p>
                    <div id="source-url-container">
                        <div id="input-group">
                            <input
                                ref={urlRef}
                                type="url"
                                id="source-url"
                                onChange={handleUrlChange}
                                placeholder="Paste a link.."
                                style={inputValid ? { borderColor: "green" } : { borderColor: "red" }}
                            />
                            <button id="clear-button" onClick={clearUrlInput}><FaTimesCircle /></button>
                        </div>
                    </div>

                    {!inputValid && <p className="validation-message" style={{ color: "red" }}>{validationMessage}</p>}

                    <div id="buttons-area">
                        <button className="upload-button" onClick={onButtonClick}>
                            <FaFileUpload className="icon" /> Upload a file
                        </button>
                        <button id="webcam-button" onClick={onWebcamButtonClick}>
                            <FaCamera className="icon" /> Webcam
                        </button>
                    </div>

                </div>
            </label>
            {dragActive && <div id="drag-file-element" onDragEnter={handleDrag} onDragLeave={handleDrag} onDragOver={handleDrag} onDrop={handleDrop}></div>}
        </form>
    );

};