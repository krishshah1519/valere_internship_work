import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../utils/axios';

const Navbar = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {

      const res = await api.post('/logout/', {}, { withCredentials: true });
      if (res.status === 200 && res.data.status) {
        navigate('/login/');
      }
    } catch (err) {
      console.error('Logout failed:', err.response?.data || err);
    }
  };

  return (
    <nav className="bg-gradient-to-r from-purple-900 via-indigo-800 to-blue-700 shadow-2xl px-6 py-4 flex justify-between items-center z-50">
      <div className="flex items-center gap-4">
        <Link
          to="/home/"
          className="text-2xl font-extrabold text-white hover:text-gray-200 transition"
        >
          Smart Expense
        </Link>
      </div>

      <ul className="flex space-x-8">
        {['Home', 'About', 'Contact'].map((page) => (
          <li key={page}>
            <Link
              to={`/${page.toLowerCase()}/`}
              className="text-white hover:text-gray-200 font-medium transition"
            >
              {page}
            </Link>
          </li>
        ))}
        <li>
          <button
            onClick={handleLogout}
            className="px-4 py-1 bg-white bg-opacity-20 hover:bg-opacity-30 text-black rounded-md font-medium transition"
          >
            Logout
          </button>
        </li>
      </ul>
    </nav>
  );
};

export default Navbar;
