import { Link } from "react-router-dom";

const Navbar = () => {
  return (
    <nav className="w-full bg-gray-900 bg-opacity-70 shadow-md fixed top-0 left-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
        <Link to="/" className="text-2xl font-bold text-cyan-400">
          Alethia
        </Link>

        <div className="space-x-6">
          <Link to="/" className="text-white hover:text-cyan-300 transition">
            Home
          </Link>
          <Link to="/detect" className="text-white hover:text-cyan-300 transition">
            Detect
          </Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
