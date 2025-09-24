import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import CommunityPage from "./pages/CommunityPage";
import "./styles.css";
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<CommunityPage />} />
      </Routes>
    </Router>
  );
}
export default App;