// src/pages/CommunityPage.jsx
import React, { useState, useEffect } from "react";
import "../styles.css";
import AuthModal from "../components/AuthModal";

const CommunityPage = () => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [authMode, setAuthMode] = useState("login"); // "login" or "register"
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  // Check localStorage token on page load
  useEffect(() => {
    const token = localStorage.getItem("accessToken");
    if (token) setIsLoggedIn(true);
  }, []);

  // Callback when login succeeds
  const handleLoginSuccess = (token) => {
    setIsLoggedIn(true);
    localStorage.setItem("accessToken", token); // make sure token is saved
    setIsModalOpen(false); // close modal
  };

  return (
    <div className="community-container">
      <div className="community-card">
        <h1>Welcome to the Community</h1>
        <p>Join discussions, share knowledge, and connect with others.</p>

        {/* Auth Buttons */}
        {!isLoggedIn ? (
          <div className="community-actions">
            <button
              className="community-btn community-btn-blue"
              onClick={() => {
                setAuthMode("login");
                setIsModalOpen(true);
              }}
            >
              Login
            </button>
            <button
              className="community-btn community-btn-green"
              onClick={() => {
                setAuthMode("register");
                setIsModalOpen(true);
              }}
            >
              Register
            </button>
          </div>
        ) : (
          <p className="logged-in-msg">You’re logged in! 🎉</p>
        )}
      </div>

      {/* Auth Modal */}
      {isModalOpen && (
        <AuthModal
          mode={authMode}
          setMode={setAuthMode}
          onClose={() => setIsModalOpen(false)}
          onLoginSuccess={handleLoginSuccess} // pass callback to modal
        />
      )}
    </div>
  );
};

export default CommunityPage;
