import React from "react";
import useQuery from "../hooks/useQuery";
import StreamPageVideoPlayer from "../components/StreamPageVideoPlayer";


export default function StreamPage(){
    const query = useQuery();

    const source = query.get('source');
    const line_1 = query.get('line1');
    const line_2 = query.get('line2');
    const isValidLink = /^https?:\/\/\w+(\.\w+)*(:\d+)?(\/\S*)?$/i.test(source);
    const isValidFilename = /\.(mp4|avi|jpg|jpeg|png)$/i.test(source);
     
    return(
        <>
            <p>Stream Page</p>
            {isValidLink && <StreamPageVideoPlayer filename={source} line1={line_1} line2={line_2}/>}
            {isValidFilename && <StreamPageVideoPlayer filename={source} line1={line_1} line2={line_2}/>}
        </>
    );
};