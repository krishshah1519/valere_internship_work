import { useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import SearchBar from "../components/Search";


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

          <div className="flex-1 max-w-xxl">
            <SearchBar />
          </div>




        </div>
      </div>
    </div>
  );
}
