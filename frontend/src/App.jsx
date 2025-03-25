import { BrowserRouter as Router, Route, Routes, Link } from "react-router-dom";
import Home from "/src/pages/Home.jsx";
import Detect from "/src/pages/Detect.jsx";
import "/src/App.css";

function App() {
  return (
    <Router>
      <div className="fullscreen-bg"></div>
      <div className="navbar">
        <Link to="/" className="nav-link">HOME</Link>
        <Link to="/detect" className="nav-link">DETECT</Link>
      </div>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/detect" element={<Detect />} />
      </Routes>
    </Router>
  );
}

export default App;
