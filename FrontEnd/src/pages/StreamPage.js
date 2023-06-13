import React, { useState } from "react";
import useQuery from "../hooks/useQuery";
import StreamPageVideoPlayer from "../components/StreamPageVideoPlayer";
import VideoPreview from "../components/VideoPreview";
import UploadDragAndDropForm from "../components/UploadDragAndDropForm";
import Axios from "../types/AxiosType";
export default function StreamPage() {
    const query = useQuery();
    const [selectedFile, setSelectedFile] = useState(null);
    const [lines, setLines] = useState([]);
    const [isStreamStopped, setIsStreamStopped] = useState(true);
    const [url,setUrl] = useState("");
    
    const source = query.get('source');
    const line_1 = query.get('line1');
    const line_2 = query.get('line2');
    const task = query.get('task');
    
    const tasks = ["traffic", "person"];
    const [selectedTask, setSelectedTask] = useState(task || tasks[0]);

    const isValidLink =  /^https?:\/\/\w+(\.\w+)*(:\d+)?(\/\S*)?$/i.test(source) ||  /^(udp):\/\/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$/i.test(source);;


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

    const handleIsStreamStopped = (value)=>{
        console.log(value);
        setIsStreamStopped(value);
    };

    const handleUrl = (url) =>{
        setUrl(url);
        setIsStreamStopped(false);
    };

    const handleSelectChange = (e)=>{
        setSelectedTask(e.target.value);
        
        setUrl('/stream');
    };
    const stateStr = isStreamStopped ? "True" : "False";
    return (
        <div style={containerStyles}>
           <div>
            <UploadDragAndDropForm  
                onFileSelect={handleFileSelect} 
                task={selectedTask} 
                handleUrl={handleUrl} 
                handleIsStreamStopped={handleIsStreamStopped} 
            />
               
                <br></br>
                <br/> <br/> <br/> <br/>
                <select value={selectedTask} onChange={handleSelectChange}>
                    {tasks.map(taskOption => <option key={taskOption} value={taskOption}>{taskOption}</option>)}
                </select>
          
            </div>
               
                {(isValidLink || isValidFilename) && !isStreamStopped && (
                    <StreamPageVideoPlayer
                        key={source} // Ensure the component updates when the source changes
                        filename={source}
                        line1={line_1}
                        line2={line_2}
                        task={selectedTask}
                        url={url}
                        isStreamStopped={isStreamStopped}
                        handleIsStreamStopped={handleIsStreamStopped}
                    />
                )}
           
                
            {selectedFile && selectedTask ===tasks[0] && (
                <VideoPreview 
                    key={selectedFile.name} 
                    file={selectedFile} 
                    task={selectedTask}
                    handleUrl={handleUrl}
                    handleFileReset={handleFileReset} 
                    onLineDrawing={handleLineDrawing} 
                />
            )}
            

        </div>
    );
};