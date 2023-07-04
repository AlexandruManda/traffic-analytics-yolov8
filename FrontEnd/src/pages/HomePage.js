import React from "react";
import "./HomePage.css";
import ContentItemSection from "../components/ContentItemSection";
import heroImage from './../assets/hero.jpg';

export default function HomePage() {
  return (
    <div className="homepage">

      <section className="hero-section">
        <img
          className="hero-image"
          src={heroImage}
          alt="Hero"
        />
      </section>

      <section className="content-section">
        <div className="container">
            <ContentItemSection>
            <p>
              Revolutionizing traffic management through AI-powered real-time analysis and advanced computer vision techniques.
            </p>
            </ContentItemSection>
        </div>
      </section>
    </div>
  );
}
