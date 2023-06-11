import React, { useState } from "react";
import useQuery from "../hooks/useQuery";
import StreamPageVideoPlayer from "../components/StreamPageVideoPlayer";
import VideoPreview from "../components/VideoPreview";
import UploadDragAndDropForm from "../components/UploadDragAndDropForm";

export default function StreamPage() {
    const query = useQuery();
    const [selectedFile, setSelectedFile] = useState(null);
    const [lines, setLines] = useState([]);
    const [isStreamStopped, setIsStreamStopped] = useState(true);
    const [url,setUrl] = useState("");
    const source = query.get('source');
    const line_1 = query.get('line1');
    const line_2 = query.get('line2');
    const isValidLink =  /^https?:\/\/\w+(\.\w+)*(:\d+)?(\/\S*)?$/i.test(source);
    const isValidFilename = /\.(mp4|avi|jpg|jpeg|png)$/i.test(source);


    const containerStyles = {
        display: 'grid',
        gridTemplateColumns: '1fr 2fr',
        gap: '20px',
        justifyContent: 'center',
        alignItems: 'center',
        height: '80vh',
        margin: '0 auto',
        maxWidth: '90%',
    };

    const handleFileSelect = (file) => {
        setIsStreamStopped(true);
        setSelectedFile(file);
    };

    const handleFileReset =()=>{
        setSelectedFile(null);
    }
    const handleLineDrawing = (lines) => {
        setLines(lines);
        if(lines.length===2){
            setIsStreamStopped(false);
        }
    };

    const handleStopStream = ()=>{
        setIsStreamStopped(true);
    };

    const handleUrl = (url) =>{
        setUrl(url);
    };
    return (
        <div style={containerStyles}>
            <UploadDragAndDropForm onFileSelect={handleFileSelect} onUrl={handleUrl} isStreamStopped={handleStopStream} />
          

                {(isValidLink || isValidFilename) && !isStreamStopped && (
                    <StreamPageVideoPlayer
                        key={source} // Ensure the component updates when the source changes
                        filename={source}
                        line1={line_1}
                        line2={line_2}
                        isStreamStopped={isStreamStopped}
                    />
                )}
            
            {selectedFile && (
                <VideoPreview 
                    key={selectedFile.name} 
                    file={selectedFile} 
                    handleFileReset={handleFileReset} 
                    onLineDrawing={handleLineDrawing} 
                />
            )}

        </div>
    );
};