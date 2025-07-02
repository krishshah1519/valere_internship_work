import { useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";
import ExpensePieChart from "../components/ExpensePieChart";
import ExpenseLineChart from "../components/ExpenseLineChart";
// import SummaryCard from "../components/SummaryCard";

export default function DashboardPage() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const handleToggleSidebar = () => {
    setSidebarOpen((prev) => !prev);
  };

  return (
    <div className="min-h-screen bg-gray-100 text-gray-900 transition-colors duration-300">
      <Navbar onToggleSidebar={handleToggleSidebar} />
      <div className="flex min-h-screen">
        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          onNavigate={() => setSidebarOpen(false)}
        />
        <main className="flex-1 p-6">
          {/* <SummaryCard /> */}

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mt-6">
            <ExpenseLineChart />
            <ExpensePieChart />
          </div>
        </main>
      </div>
    </div>
  );
}
