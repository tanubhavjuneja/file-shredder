// src/pages/CommunityPage.jsx
import React, { useState } from "react";
import AuthModal from "../components/AuthModal";

const CommunityPage = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false); // Replace with real auth later
  const [showAuth, setShowAuth] = useState(false);
  const [authMode, setAuthMode] = useState("login"); // "login" or "register"

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100">
      <div className="bg-white shadow-lg rounded-2xl p-8 max-w-lg w-full text-center">
        <h1 className="text-3xl font-bold text-gray-800 mb-4">
          Welcome to the Community
        </h1>
        <p className="text-gray-600 mb-6">
          Connect, share ideas, and start discussions with other members of the project.
        </p>

        {/* Start Discussion Button */}
        <button
          disabled={!isLoggedIn}
          className={`w-full py-3 rounded-xl font-semibold mb-6 transition ${
            isLoggedIn
              ? "bg-blue-600 text-white hover:bg-blue-700"
              : "bg-gray-300 text-gray-500 cursor-not-allowed"
          }`}
        >
          Start Discussion
        </button>

        {/* Auth Buttons */}
        {!isLoggedIn ? (
          <div className="flex justify-center gap-4">
            <button
              onClick={() => {
                setAuthMode("login");
                setShowAuth(true);
              }}
              className="px-4 py-2 bg-blue-500 text-white rounded-xl hover:bg-blue-600 transition"
            >
              Login
            </button>
            <button
              onClick={() => {
                setAuthMode("register");
                setShowAuth(true);
              }}
              className="px-4 py-2 bg-green-500 text-white rounded-xl hover:bg-green-600 transition"
            >
              Register
            </button>
          </div>
        ) : (
          <p className="text-green-600 font-medium">You’re logged in! 🎉</p>
        )}
      </div>

      {/* Auth Popup */}
      {showAuth && (
        <AuthModal
          mode={authMode}
          setMode={setAuthMode}
          onClose={() => setShowAuth(false)}
        />
      )}
    </div>
  );
};

export default CommunityPage;
