import React, { useState } from "react";
import { DollarSign, Home, Mail, Settings, User, X } from "lucide-react";
import { useNavigate } from "react-router-dom";

const Sidebar = ({ isOpen, onClose, onNavigate }) => {
  const [activeItem, setActiveItem] = useState('/');
  const navigate = useNavigate(); // ✅ Move inside the component

  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: Home, path: '/home/' },
    { id: 'expenses', label: 'Manage Expenses', icon: DollarSign, path: '/expenses/' },
    // { id: 'profile', label: 'Profile', icon: User, path: '/profile/' },
    // { id: 'settings', label: 'Settings', icon: Settings, path: '/settings/' },
    { id: 'contact', label: 'Contact Us', icon: Mail, path: '/contact/' },
  ];

  const handleNavigation = (path) => {
    setActiveItem(path);
    if (onNavigate) onNavigate(path);
    navigate(path);
    onClose();
  };

  return (
    <>
      {isOpen && (
        <div
          className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
          onClick={onClose}
        />
      )}

      <aside
        className={`z-50 bg-white text-gray-800 shadow-lg lg:shadow-none
          fixed top-0 left-0 w-64 h-screen transform transition-transform duration-300
          ${isOpen ? 'translate-x-0' : '-translate-x-full'}
          lg:translate-x-0 lg:static lg:h-auto
        `}
      >
        <div className="p-4 border-b border-gray-300 lg:hidden">
          <button
            onClick={onClose}
            className="p-2 rounded-md hover:bg-gray-200"
          >
            <X className="h-5 w-5 text-gray-800" />
          </button>
        </div>

        <nav className="p-4 space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeItem === item.path;

            return (
              <button
                key={item.id}
                onClick={() => handleNavigation(item.path)}
                className={`w-full flex items-center space-x-3 px-3 py-2 rounded-lg text-left transition-colors
                  ${isActive ? 'bg-blue-100 font-semibold text-blue-700' : 'hover:bg-gray-100'}
                `}
              >
                <Icon className="h-5 w-5" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>
      </aside>
    </>
  );
};

export default Sidebar;
