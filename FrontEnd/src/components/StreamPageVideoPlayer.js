import React,{useRef,useEffect} from 'react';

function StreamPageVideoPlayer({ filename, line1,line2 }) {
    const videoURL = `http://localhost:5000/api/stream?source=${filename}&line1=${line1}&line2=${line2}`;
    const imgRef = useRef(null);

    useEffect(()=>{
        const imgDisplay = imgRef.current;
        if (imgDisplay){
            imgDisplay.src=videoURL;
        } 

        return(()=>{
            imgDisplay.src="";
        });
    },[imgRef]);

    return (
        <div>
            <img ref={imgRef} alt="Wait for detection .." />
        </div>
    );
};

export default StreamPageVideoPlayer;