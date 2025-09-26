// src/pages/CommunityPage.jsx
import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles.css";

const CommunityPage = () => {
  const [discussions, setDiscussions] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [user, setUser] = useState(null);
  const [profileOpen, setProfileOpen] = useState(false);

  const token = localStorage.getItem("accessToken");

  // Fetch logged-in user info
  const fetchUser = async () => {
    if (!token) return;

    try {
      const res = await axios.get("http://127.0.0.1:8000/api/user/", {
        headers: { Authorization: `Bearer ${token}` },
      });
      setUser(res.data);
    } catch (err) {
      console.error("Failed to fetch user:", err);
      localStorage.removeItem("accessToken"); // token might be invalid
      setUser(null);
    }
  };

  // Fetch previous discussions
  const fetchDiscussions = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/api/discussions/list");
      setDiscussions(res.data);
    } catch (err) {
      console.error("Failed to fetch discussions:", err);
      setError("Failed to load discussions.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUser();
    fetchDiscussions();
  }, []);

  // Logout user
  const handleLogout = () => {
    localStorage.removeItem("accessToken");
    setUser(null);
    window.location.reload(); // redirect to login page
  };

  // Start a new discussion
  const handleStartDiscussion = async () => {
    const title = prompt("Enter discussion title:");
    if (!title) return;
    if (!token) {
      alert("You must be logged in to start a discussion.");
      return;
    }

    try {
      const res = await axios.post(
        "http://127.0.0.1:8000/api/discussions/create",
        { title },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setDiscussions([res.data, ...discussions]);
    } catch (err) {
      console.error("Failed to start discussion:", err);
      alert("Failed to start discussion.");
    }
  };

  return (
    <div className="community-container">
      {/* Header */}
      <div className="community-header">
        <h1>Community</h1>
        {user && (
          <div className="user-profile-wrapper">
            {/* Avatar */}
            <div
              className="user-avatar"
              onClick={() => setProfileOpen(!profileOpen)}
            >
              {user.username.charAt(0).toUpperCase()}
            </div>

            {/* Profile Popup */}
            {profileOpen && (
              <div className="profile-popup">
                <p>
                  <strong>Username:</strong> {user.username}
                </p>
                <p>
                  <strong>Email:</strong> {user.email}
                </p>
                {user.phone && (
                  <p>
                    <strong>Phone:</strong> {user.phone}
                  </p>
                )}
                <button onClick={handleLogout} className="logout-btn">
                  Logout
                </button>
              </div>
            )}
          </div>
        )}
      </div>

      {/* Start Discussion Button */}
      <button
        className="community-btn community-btn-blue"
        onClick={handleStartDiscussion}
        disabled={!user}
        title={!user ? "Login to start a discussion" : ""}
      >
        Start Discussion
      </button>

      {/* Discussions List */}
      <div className="discussions-list">
        {loading ? (
          <p>Loading discussions...</p>
        ) : error ? (
          <p style={{ color: "red" }}>{error}</p>
        ) : discussions.length === 0 ? (
          <p>No discussions yet. Start one!</p>
        ) : (
          discussions.map((d) => (
            <div key={d.id} className="discussion-card">
              <h3>{d.title}</h3>
              <p>Started by: {d.user.username}</p>
            </div>
          ))
        )}
      </div>
    </div>
  );
};

export default CommunityPage;
