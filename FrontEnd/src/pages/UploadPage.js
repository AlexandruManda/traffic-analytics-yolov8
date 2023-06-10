import React, {useState} from "react";
import UploadDragAndDropForm from "../components/UploadDragAndDropForm";
import VideoPreview from "../components/VideoPreview";

export default function UploadPage(){
    const [selectedFile, setSelectedFile] = useState(null);

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

    return(
        <div style={containerStyles}>
            <UploadDragAndDropForm onFileSelect={setSelectedFile} />
            {selectedFile && <VideoPreview file={selectedFile} />}
        </div>
    );
};