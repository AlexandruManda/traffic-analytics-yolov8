import React from "react";
import "./HomePage.css";

export default function HomePage() {
  return (
    <div className="homepage">
      <nav className="navbar">
        <ul className="nav-list">
          <li className="nav-item">
            <a href="#">Home</a>
          </li>
          <li className="nav-item">
            <a href="#">About</a>
          </li>
          <li className="nav-item">
            <a href="#">Services</a>
          </li>
          <li className="nav-item">
            <a href="#">Contact</a>
          </li>
        </ul>
      </nav>

      <section className="hero-section">
        <img
          className="hero-image"
          src="path/to/hero-image.jpg"
          alt="Hero"
        />
      </section>

      <section className="content-section">
        <div className="container">
          <div className="content-item">
            <img
              className="content-image"
              src="path/to/image1.jpg"
              alt="Image 1"
            />
            <p>
              Lorem ipsum dolor sit amet, consectetur adipiscing elit. Integer
              commodo eros sit amet turpis interdum, id efficitur neque eleifend.
              In vitae mi a arcu ullamcorper euismod. Fusce hendrerit magna id
              lacus facilisis, sit amet scelerisque elit scelerisque.
            </p>
          </div>
          <div className="content-item">
            <p>
              Nullam varius ipsum a dolor tempus aliquam. Suspendisse potenti.
              Proin luctus odio id urna ultrices tristique. Sed mattis, mi non
              mattis efficitur, est sem pharetra lacus, id efficitur turpis ante
              sit amet felis. Quisque nec libero ut diam bibendum faucibus.
            </p>
            <img
              className="content-image"
              src="path/to/image2.jpg"
              alt="Image 2"
            />
          </div>
        </div>
      </section>
    </div>
  );
}
