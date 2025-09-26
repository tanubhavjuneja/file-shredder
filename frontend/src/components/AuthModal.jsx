import React, { useState, useEffect } from "react";
import axios from "axios";
import "../styles.css";

const AuthModal = ({ mode, setMode, onClose , onLoginSuccess}) => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    name: "",
    password: "",
    phone: "",
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");

    try {
      if (mode === "login") {
        const res = await axios.post("http://127.0.0.1:8000/api/login/", {
          username: formData.username,
          password: formData.password,
        });
        if (res.data.success) {
          if (onLoginSuccess) onLoginSuccess(res.data.token);
          alert("Login successful!");
          onClose();
        } else {
          setError(res.data.message || "Login failed");
        }
      } else {
        const res = await axios.post("http://127.0.0.1:8000/api/register/", {
          username: formData.username,
          email: formData.email,
          name: formData.name,
          password: formData.password,
          phone: formData.phone,
        });
        if (res.data.success) {
          alert("Registration successful! Please login.");
          setMode("login");
        } else {
          setError(res.data.message || "Registration failed");
        }
      }
    } catch (err) {
      console.error(err);
      setError("Server error. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  // Close modal on Escape key
  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", handleEsc);
    return () => window.removeEventListener("keydown", handleEsc);
  }, [onClose]);

  return (
    <div className="auth-modal">
      <div className="auth-modal-content">
        <h2>{mode === "login" ? "Login" : "Register"}</h2>

        {error && <p style={{ color: "red", marginBottom: "0.5rem" }}>{error}</p>}

        <form onSubmit={handleSubmit}>
          {mode === "login" ? (
            <>
              <input
                type="text"
                name="username"
                placeholder="Username"
                value={formData.username}
                onChange={handleChange}
                required
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                required
              />
            </>
          ) : (
            <>
              <input
                type="text"
                name="username"
                placeholder="Username"
                value={formData.username}
                onChange={handleChange}
                required
              />
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="name"
                placeholder="Full Name"
                value={formData.name}
                onChange={handleChange}
                required
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                required
              />
              <input
                type="text"
                name="phone"
                placeholder="Phone (Optional)"
                value={formData.phone}
                onChange={handleChange}
              />
            </>
          )}

          <button
            type="submit"
            className={mode === "login" ? "login-btn" : "register-btn"}
            disabled={loading}
          >
            {loading ? "Please wait..." : mode === "login" ? "Login" : "Register"}
          </button>
        </form>

        <div className="switch-link">
          {mode === "login" ? (
            <>
              New user?{" "}
              <button type="button" onClick={() => setMode("register")}>
                Register
              </button>
            </>
          ) : (
            <>
              Already a user?{" "}
              <button type="button" onClick={() => setMode("login")}>
                Login
              </button>
            </>
          )}
        </div>

        <button className="cancel-btn" onClick={onClose}>
          Cancel
        </button>
      </div>
    </div>
  );
};

export default AuthModal;
