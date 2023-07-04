import React from "react";

export default function ContentItemSection({ children }){
    
    return(<>
        <div className="content-item">
           {children}
        </div>
    </>
    );
}