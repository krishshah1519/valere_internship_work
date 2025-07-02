import { useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import SearchBar from "../components/Search";
import ExportToExcel from "../components/Export";   // 👈 import the form

export default function ExpensesPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const handleToggleSidebar = () => setSidebarOpen((prev) => !prev);

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900">
      <Navbar onToggleSidebar={handleToggleSidebar} />

      <div className="flex">
        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          onNavigate={() => setSidebarOpen(false)}
        />


        <div className="flex-1 p-4 flex items-start space-x-6">
          {/* 1) Search bar takes up flexible space */}
          <div className="flex-1 max-w-xxl">
            <SearchBar />
          </div>

          {/* 2) Export form on the right, fixed width */}


        </div>
      </div>
    </div>
  );
}
