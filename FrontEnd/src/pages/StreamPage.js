// import React, { useEffect, useState } from "react";
// import useQuery from "../hooks/useQuery";
// import StreamPageVideoPlayer from "../components/StreamPageVideoPlayer";
// import VideoPreview from "../components/VideoPreview";
// import UploadDragAndDropForm from "../components/UploadDragAndDropForm";
// import './StreamPage.css';
// import { useNavigate } from "react-router-dom";

// export default function StreamPage() {
//     const query = useQuery();
//     const [selectedFile, setSelectedFile] = useState(null);
//     const [lines, setLines] = useState([]);
//     const [isStreamStopped, setIsStreamStopped] = useState(false);
//     const [url,setUrl] = useState("");
    
//     const source = query.get('source');
//     const line_1 = query.get('line1');
//     const line_2 = query.get('line2');
//     const task = query.get('task');
    
//     const tasks = ["traffic", "person"];
//     const [selectedTask, setSelectedTask] = useState(task || tasks[0]);

//     const isValidLink =  /^https?:\/\/\w+(\.\w+)*(:\d+)?(\/\S*)?$/i.test(source) ||  /^(udp):\/\/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$/i.test(source);;

//     const linesPresent = line_1 && line_2 ;
//     const isValidFilename = /\.(mp4|avi|jpg|jpeg|png)$/i.test(source);
//     const navigate = useNavigate();
//     const buildURL = () => {
//         let builtUrl = `/stream?source=${selectedFile?.name }`;
//         lines.forEach((line, index) => {
//             builtUrl += `&line${index + 1}=(${line.start.x},${line.start.y})(${line.end.x},${line.end.y})`;
//         });
//         builtUrl +=`&task=${selectedTask}`
//         return builtUrl;
//     };
//     // useEffect(()=>{
//     //     if(lines.length >=2){
//     //         const url = buildURL();
//     //         // setUrl(url);
//     //         navigate(url);
//     //     }
//     // },[lines]);
    
//     // useEffect(()=>{
//     //     const url = buildURL();
//     //     // setUrl(url);
//     // },[selectedTask,isStreamStopped]);

//     // useEffect(()=>{
//     //     if(task == task[0]){
//     //         setIsStreamStopped(true);
//     //     }
//     //     else if (task==task[1]){
//     //         setIsStreamStopped(false);
//     //     }
//     // },[selectedFile,selectedTask]);
//     const handleFileReset = () => {
//         setSelectedFile(null);
//         setIsStreamStopped(true);
//     }
    
//       const handleLineDrawing = (lines) => {
//         setLines(lines);
//         // setIsStreamStopped(true);
//         if(lines.length >= 2){
//             setIsStreamStopped(false);
//         }
//       };
    
//       const handleUrl = (url) =>{
//         setUrl(url);
//         navigate(url);
//         if (selectedTask === task[1]){
//             setIsStreamStopped(false);
//         }
        
//       };
    
//     const handleFileSelect = (file) => {

//         setIsStreamStopped(true);
//         setSelectedFile(file);
//     };

//     const handleSelectChange = (e)=>{
//         setSelectedTask(e.target.value);
//         // handleFileReset();
//     };

//     return (
//         <div className="stream-page-container">
//             <div>
//                 <UploadDragAndDropForm  
//                     onFileSelect={handleFileSelect} 
//                     task={selectedTask} 
//                     handleUrl={handleUrl} 
//                 />

//                 <br></br>
//                 <h3>Select the tracker type </h3>
//                 <select className="task-select" value={selectedTask} onChange={handleSelectChange}>
//                     {tasks.map(taskOption => 
//                         <option key={taskOption} value={taskOption}>
//                            {taskOption === 'person' ? '👤 Person' : '🚗 Traffic'}
//                         </option>)
//                     }
//                 </select>
//             </div>
//             {isStreamStopped?"True":"False"}
    
//             {selectedTask}
//             {/* Only render VideoPreview if task is 'traffic' */}
//             {selectedTask === tasks[0] && !linesPresent &&  
//                 <VideoPreview 
//                     key={selectedTask}
//                     file={selectedFile}
//                     task={selectedTask}
//                     onLineDrawing={handleLineDrawing}
                
//                 />
//             }
//              {!isStreamStopped && 
//                 <StreamPageVideoPlayer
//                 url={url} 
//                 isStreamStopped={isStreamStopped} 
//                 />
//             }
//     </div>
//     );
// };

import React, { useEffect, useState } from "react";
import useQuery from "../hooks/useQuery";
import StreamPageVideoPlayer from "../components/StreamPageVideoPlayer";
import VideoPreview from "../components/VideoPreview";
import UploadDragAndDropForm from "../components/UploadDragAndDropForm";
import './StreamPage.css';
import { useNavigate } from "react-router-dom";

export default function StreamPage() {
    const query = useQuery();
    const [selectedFile, setSelectedFile] = useState(null);
    const [lines, setLines] = useState([]);
    const [isStreamStopped, setIsStreamStopped] = useState(false);
    const [url,setUrl] = useState("");
    
    const source = query.get('source');
    const line_1 = query.get('line1');
    const line_2 = query.get('line2');
    const task = query.get('task');
    
    const tasks = ["traffic", "person"];
    const [selectedTask, setSelectedTask] = useState(task || tasks[0]);

    const isValidLink =  /^https?:\/\/\w+(\.\w+)*(:\d+)?(\/\S*)?$/i.test(source) ||  /^(udp):\/\/(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):(\d{1,5})$/i.test(source);;

    const linesPresent = line_1 && line_2 ;
    const isValidFilename = /\.(mp4|avi|jpg|jpeg|png)$/i.test(source);
    const navigate = useNavigate();

    const buildURL = () => {
        let builtUrl = `/stream?source=${selectedFile?.name }`;
        lines.forEach((line, index) => {
            builtUrl += `&line${index + 1}=(${line.start.x},${line.start.y})(${line.end.x},${line.end.y})`;
        });
        builtUrl +=`&task=${selectedTask}`
        return builtUrl;
    };

    useEffect(()=>{
        console.log('selectedTask:', selectedTask);
    console.log('selectedFile:', selectedFile);
        if (selectedTask && selectedFile) {
            const url = buildURL();
            setUrl(url);
            navigate(url);
        }

    },[lines]);

    useEffect(()=>{
        if (selectedTask === tasks[1]){
            setIsStreamStopped(false);
        }
        if(lines.length >=2){
            setIsStreamStopped(false);
        //     setLines([]);
        }
    },[url]);

    useEffect(()=>{
        if(selectedFile && selectedTask==tasks[1]){
            setIsStreamStopped(true);
        }
    },[selectedFile]);

    const handleFileReset = () => {
        setSelectedFile(null);
        // setIsStreamStopped(true);
    }
    
    const handleLineDrawing = (drawnLines) => {
        setLines(drawnLines);
    };
    
    const handleUrl = (url) =>{
        setUrl(url);
        navigate(url);
    };
    
    const handleFileSelect = (file) => {
        setIsStreamStopped(true);
        setSelectedFile(file);
    };

    const handleSelectChange = (e)=>{
        setSelectedTask(e.target.value);
        handleFileReset();
    };

    return (
        <div className="stream-page-container">
            <div>
                <UploadDragAndDropForm  
                    onFileSelect={handleFileSelect} 
                    task={selectedTask} 
                    handleUrl={handleUrl} 
                />

                <br></br>
                <h3>Select the tracker type </h3>
                <select className="task-select" value={selectedTask} onChange={handleSelectChange}>
                    {tasks.map(taskOption => 
                        <option key={taskOption} value={taskOption}>
                           {taskOption === 'person' ? '👤 Person' : '🚗 Traffic'}
                        </option>)
                    }
                </select>
            </div>
            {/* {isStreamStopped ? "True" : "False"} */}
    
            {/* {selectedTask} */}
            {/* Only render VideoPreview if task is 'traffic' */}
            {selectedTask === tasks[0] && !linesPresent && isStreamStopped &&  
                <VideoPreview 
                    key={selectedTask}
                    file={selectedFile}
                    task={selectedTask}
                    onLineDrawing={handleLineDrawing}
                
                />
            }
             {!isStreamStopped && 
                <StreamPageVideoPlayer
                url={url} 
                isStreamStopped={isStreamStopped} 
                />
            }
    </div>
    );
};
