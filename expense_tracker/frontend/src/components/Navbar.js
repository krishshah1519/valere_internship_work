import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import api from '../utils/axios';

const Navbar = ({ onToggleSidebar }) => {
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const res = await api.post('/logout/', {}, { withCredentials: true });

      if (res.status === 200 && res.data.status) {
        console.log('Logout successful');
        navigate('/login/');
      } else {
        console.warn('Unexpected logout response', res.data);
      }
    } catch (err) {
      console.error('Logout failed:', err.response?.data || err.message);
    }
  };

  const toggleMobileMenu = () => {
    setIsMobileMenuOpen((prev) => !prev);
  };

  return (
    <nav className="bg-white shadow-md px-6 py-4 flex justify-between items-center z-50 relative">
      <div className="flex items-center gap-4">
        {/* Toggle button for mobile */}
        <button
          className="lg:hidden p-2 rounded hover:bg-gray-100"
          onClick={toggleMobileMenu}
        >
          {isMobileMenuOpen ? (
            <X className="h-6 w-6 text-gray-800" />
          ) : (
            <Menu className="h-6 w-6 text-gray-800" />
          )}
        </button>

        <Link
          to="/home/"
          className="text-2xl font-bold text-gray-800 hover:text-blue-600 transition-colors"
        >
          Smart Expense Tracker
        </Link>
      </div>

      {/* Desktop links */}
      <ul className="hidden lg:flex space-x-6">
        <li>
          <Link to="/home/" className="text-gray-700 hover:text-blue-600 font-medium">
            Home
          </Link>
        </li>
        <li>
          <Link to="/about" className="text-gray-700 hover:text-blue-600 font-medium">
            About
          </Link>
        </li>
        <li>
          <Link to="/contact" className="text-gray-700 hover:text-blue-600 font-medium">
            Contact
          </Link>
        </li>
        <li>
          <button
            onClick={handleLogout}
            className="text-red-500 hover:text-red-700 font-medium"
          >
            Logout
          </button>
        </li>
      </ul>

      {/* Mobile menu dropdown */}
      {isMobileMenuOpen && (
        <div className="absolute top-full left-0 w-full bg-white shadow-md border-t z-40 lg:hidden">
          <ul className="flex flex-col px-6 py-4 space-y-4">
            <li>
              <Link
                to="/home/"
                className="text-gray-700 font-medium hover:text-blue-600"
                onClick={toggleMobileMenu}
              >
                Home
              </Link>
            </li>
            <li>
              <Link
                to="/about"
                className="text-gray-700 font-medium hover:text-blue-600"
                onClick={toggleMobileMenu}
              >
                About
              </Link>
            </li>
            <li>
              <Link
                to="/contact"
                className="text-gray-700 font-medium hover:text-blue-600"
                onClick={toggleMobileMenu}
              >
                Contact
              </Link>
            </li>
            <li>
              <button
                onClick={() => {
                  toggleMobileMenu();
                  handleLogout();
                }}
                className="text-left text-red-500 font-medium hover:text-red-700"
              >
                Logout
              </button>
            </li>
          </ul>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
