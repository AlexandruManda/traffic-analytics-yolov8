import React from "react";
import {Link} from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
    const navLinks = [
        {
            "text" : "Home",
            "path" : "/"
        },
        {
            "text" : "Stream",
            "path" : "/stream"
        }
    ];

    return (
        <>
            <nav className="navbar">
                <ul className="nav-list">
                    {navLinks.map((link, index) => (
                        <li key={index} className="nav-item">
                            <Link style={{textDecoration:"none"}} to={link.path}>{link.text}</Link>
                        </li>
                    ))}
                </ul>
            </nav>
        </>
    );
}





