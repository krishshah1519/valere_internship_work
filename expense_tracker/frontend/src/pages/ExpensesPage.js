import {useState} from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import SearchBar from "../components/Search";

export default function ExpensesPage() {
    const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleToggleSidebar = () => {
    setSidebarOpen((prev) => !prev);
  };
    return(
        <div className="min-h-screen bg-gray-100 text-gray-900 transition-colors duration-300">
            <Navbar onToggleSidebar={handleToggleSidebar} />
            <div className="flex min-h-screen">
                <Sidebar
                    isOpen={sidebarOpen}
                    onClose={() => setSidebarOpen(false)}
                    onNavigate={() => setSidebarOpen(false)}/>
                <SearchBar />
            </div>
        </div>
    )
}