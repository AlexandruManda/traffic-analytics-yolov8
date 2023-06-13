import React, { useState, useRef, useEffect } from "react";
import './UploadDragAndDropForm.css';
import Axios from "../types/AxiosType";
import { useNavigate } from "react-router-dom";
import { FaCamera, FaFileUpload, FaUpload, FaYoutube  } from "react-icons/fa";

export default function UploadDragAndDropForm({task, onFileSelect,handleIsStreamStopped,handleUrl }) {
    
    const navigate = useNavigate();
    const [dragActive, setDragActive] = useState(false);
    const [inputValid, setInputValid] = useState(true);
    const [validationMessage, setValidationMessage] = useState("");
    const [selectedUrl,setSelectedUrl]=useState("");

    const inputRef = useRef(null);
    const urlRef = useRef(null);
    
    // useEffect(()=>{

    //     if (selectedUrl =="")
    //         return;
    //     navigate(selectedUrl);
    // },[selectedUrl]);

    useEffect(() => {
        // If task changes, clear the input
        if (urlRef.current) {
          urlRef.current.value = "";
          setSelectedUrl("");
        }
      }, [task]);

    const validateUrl = (url) => {
        if (url !== undefined || url !== '') {        
            const youtubeRegExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
            const udpOrRtspRegExp = /^(udp|rtsp):\/\/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$/;
            
            const matchYouTube = url.match(youtubeRegExp);
            const matchUdpRtsp = url.match(udpOrRtspRegExp);
            
            return ((matchYouTube && matchYouTube[2].length === 11) || matchUdpRtsp);
        }
        return false;
    }

    const handleFile = (file) => {
        const formData = new FormData();
        formData.append("video", file);
        handleIsStreamStopped(false);
        onFileSelect(file);
        Axios.axiosForm.post('/save_video', formData)
        .then((response)=>{
            if(response.status === 200){
                // navigate(`/stream`);
                // After successful upload, you can build your new URL here
                const newUrl = `/stream?source=${response.data.filename}&task=${task}`;
                handleUrl(newUrl);
                navigate(newUrl);
                if (inputRef.current) {
                    inputRef.current.value = "";
                }
                console.log("File uploaded successfully");
                console.log(response.data);
                onFileSelect(file);
                setSelectedUrl(newUrl);
                handleIsStreamStopped(true);
                

            }
        })
        .catch(e=>console.log(e));
        
    };
    const getFileNameFromHeaders = (headers) => {
        const contentDispositionHeader = headers['content-disposition'];
        const filenameMatch = contentDispositionHeader.match(/filename="(.+)"/);
        if (filenameMatch && filenameMatch.length > 1) {
          return filenameMatch[1];
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
                    console.log(response);
                    const file = new File([response.data], getFileNameFromHeaders(response.headers), { type: 'video/mp4' });
                    console.log(file);
                    onFileSelect(file);
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
            console.log(e.target.files[0]);
        }
    };

    const handleUrlChange = function (e) {
        const inputURL = e.target.value;
        if (inputURL === '') {
            setInputValid(false);
            setValidationMessage("Input field can't be empty.");
            handleUrl('/stream');
            setSelectedUrl('/stream')
        } else if (!validateUrl(inputURL)) {
            setInputValid(false);
            setValidationMessage("Input is not a valid URL or YouTube link.");
            handleUrl('/stream');
            setSelectedUrl('/stream')
        } else {
            console.log('Valid YouTube URL');
            setInputValid(true);
            setValidationMessage("");
            // isStreamStopped();
           
            const udpOrRtspRegExp = /^(udp|rtsp):\/\/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$/;
            const matchUdpRtsp = inputURL.match(udpOrRtspRegExp);
            if (matchUdpRtsp) {
                // for udp and rtsp, navigate to a new page
                const processedUrl = `/stream?source=${encodeURI(inputURL)}&task=${task}`
                console.log(processedUrl);
                handleUrl(processedUrl);
                setSelectedUrl(processedUrl);

            } else {
                // for youtube url, download the video
                handleYouTubeDownload(inputURL);
                const url = `/stream?source=${inputURL}&task=${task}`;
                handleUrl(url);
                setSelectedUrl(url);
                
            }
            // handleYouTubeDownload(url);
        }
      
    };

    // triggers the input when the button is clicked
    const onButtonClick = (e) => {
        e.preventDefault();
        if(inputRef.current){
            inputRef.current.click();
        }
    };

    const onWebcamButtonClick = (e) => {
        e.preventDefault();
    };


    return (
        <form id="form-file-upload" onDragEnter={handleDrag} >
            <input ref={inputRef} type="file" id="input-file-upload" multiple={false} onChange={handleChange} />
            <label id="label-file-upload" htmlFor="input-file-upload" className={dragActive ? "drag-active" : ""}>
                <div>
                    <p><FaUpload /> Drag and drop Image / Video File </p>
                    <p>OR</p>
                    <p><FaYoutube /> Paste Youtube / Image URL</p>
                    <input 
                        ref={urlRef} 
                        type="url" 
                        id="source-url" 
                        onChange={handleUrlChange} 
                        placeholder="Paste a link.."
                        style={inputValid ? { borderColor: "green" } : { borderColor: "red" }} 
                    />
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