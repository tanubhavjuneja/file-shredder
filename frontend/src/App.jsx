// src/App.jsx
import { BrowserRouter as Router, Routes, Route, Navigate } from "react-router-dom";
import LoginPage from "./pages/LoginPage";
import CommunityPage from "./pages/CommunityPage";

function App() {
  // Check if the user is logged in by checking localStorage token
  const isLoggedIn = !!localStorage.getItem("accessToken");

  return (
    <Router>
      <Routes>
        {/* Redirect root "/" based on login status */}
        <Route
          path="/"
          element={isLoggedIn ? <Navigate to="/community" /> : <LoginPage />}
        />
        {/* Community page route */}
        <Route
          path="/community"
          element={isLoggedIn ? <CommunityPage /> : <Navigate to="/" />}
        />
      </Routes>
    </Router>
  );
}

export default App;
