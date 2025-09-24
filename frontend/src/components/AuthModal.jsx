// src/components/AuthModal.jsx
import React, { useState } from "react";
const AuthModal = ({ mode, setMode, onClose }) => {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    name: "",
    password: "",
    phone: "",
  });

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = (e) => {
    e.preventDefault();
    if (mode === "login") {
      console.log("Login Data:", {
        username: formData.username,
        password: formData.password,
      });
      // TODO: POST to Django backend /api/login
    } else {
      console.log("Register Data:", formData);
      // TODO: POST to Django backend /api/register
    }
    onClose();
  };

  return (
    <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-50">
      <div className="bg-white rounded-2xl shadow-lg p-6 w-full max-w-sm animate-fadeIn">
        <h2 className="text-2xl font-bold mb-4 text-center text-gray-800">
          {mode === "login" ? "Login" : "Register"}
        </h2>

        <form onSubmit={handleSubmit} className="space-y-3">
          {/* Login Fields */}
          {mode === "login" ? (
            <>
              <input
                type="text"
                name="username"
                placeholder="Username"
                value={formData.username}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-300"
                required
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-blue-300"
                required
              />
            </>
          ) : (
            /* Register Fields */
            <>
              <input
                type="text"
                name="username"
                placeholder="Username"
                value={formData.username}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-green-300"
                required
              />
              <input
                type="email"
                name="email"
                placeholder="Email"
                value={formData.email}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-green-300"
                required
              />
              <input
                type="text"
                name="name"
                placeholder="Full Name"
                value={formData.name}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-green-300"
                required
              />
              <input
                type="password"
                name="password"
                placeholder="Password"
                value={formData.password}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-green-300"
                required
              />
              <input
                type="text"
                name="phone"
                placeholder="Phone (Optional)"
                value={formData.phone}
                onChange={handleChange}
                className="w-full px-3 py-2 border rounded-lg focus:ring focus:ring-green-300"
              />
            </>
          )}

          {/* Submit */}
          <button
            type="submit"
            className={`w-full py-2 rounded-lg text-white font-semibold transition ${
              mode === "login"
                ? "bg-blue-600 hover:bg-blue-700"
                : "bg-green-600 hover:bg-green-700"
            }`}
          >
            {mode === "login" ? "Login" : "Register"}
          </button>
        </form>

        {/* Switch Option */}
        <div className="mt-4 text-center text-sm text-gray-600">
          {mode === "login" ? (
            <>
              New user?{" "}
              <button
                onClick={() => setMode("register")}
                className="text-green-600 font-medium hover:underline"
              >
                Register
              </button>
            </>
          ) : (
            <>
              Already a user?{" "}
              <button
                onClick={() => setMode("login")}
                className="text-blue-600 font-medium hover:underline"
              >
                Login
              </button>
            </>
          )}
        </div>

        {/* Cancel */}
        <button
          onClick={onClose}
          className="mt-4 text-sm text-gray-500 hover:underline w-full"
        >
          Cancel
        </button>
      </div>
    </div>
  );
};

export default AuthModal;
