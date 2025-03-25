import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Home from "./pages/Home";
import Detect from "./pages/Detect";
import Footer from "./components/Footer";

function App() {
  return (
    <Router>
      <Navbar />
      <div className="pt-20"> {/* Add padding to prevent overlap with fixed navbar */}
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/detect" element={<Detect />} />
        </Routes>
      </div>
      <Footer />
    </Router>
  );
}

export default App;
