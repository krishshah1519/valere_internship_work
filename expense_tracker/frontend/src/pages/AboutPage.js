import { useState } from "react";
import Navbar from "../components/Navbar";
import Sidebar from "../components/Sidebar";

export default function AboutPage() {
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
        <main className="flex-1 p-6 space-y-4">
          <h1 className="text-2xl font-bold mb-4">Assignment : Smart Expense Tracker</h1>

          <section>
            <h2 className="text-xl font-semibold mb-2">Objective</h2>
            <p>
              Develop a Django-based expense tracker where users can log, manage, and visualize their personal
              expenses through a clean interface with charts, export options, and weekly summaries.
            </p>
          </section>

          <section>
            <h2 className="text-xl font-semibold mb-2">Core Features</h2>
            <ol className="list-decimal list-inside space-y-2">
              <li>
                <strong>User Authentication</strong>
                <ul className="list-disc list-inside ml-4">
                  <li>Register: New users can sign up</li>
                  <li>Login/Logout: Session-based authentication</li>
                  <li>Users can only access and manage their own expenses</li>
                </ul>
              </li>
              <li>
                <strong>Expense Management</strong>
                <ul className="list-disc list-inside ml-4">
                  <li>Add/Edit/Delete expenses (amount, description, category, date)</li>
                  <li>Filter expenses by date or category</li>
                </ul>
              </li>
              <li>
                <strong>Category-wise Monthly Summary (Chart.js)</strong>
                <ul className="list-disc list-inside ml-4">
                  <li>Pie chart for current month's category distribution</li>
                  <li>Line/bar chart for expenses over time</li>
                </ul>
              </li>
              <li>
                <strong>Export to Excel</strong>
                <ul className="list-disc list-inside ml-4">
                  <li>Download expenses as `.xlsx` file using pandas/openpyxl</li>
                  <li>Filter by month or category</li>
                </ul>
              </li>
              <li>
                <strong>REST API (Django REST Framework)</strong>
                <ul className="list-disc list-inside ml-4">
                  <li>GET/POST/PUT/DELETE for expenses with token/session auth</li>
                </ul>
              </li>
            </ol>
          </section>

          <section>
            <h2 className="text-xl font-semibold mb-2">Advanced Features</h2>
            <ol className="list-decimal list-inside space-y-2">
              <li>
                <strong>Weekly Email Reports (Celery + Redis)</strong>
                <ul className="list-disc list-inside ml-4">
                  <li>Background task to generate weekly expense summaries</li>
                  <li>Email report with totals and category breakdown</li>
                </ul>
              </li>
              <li>
                <strong>Custom Admin Dashboard</strong>
                <ul className="list-disc list-inside ml-4">
                  <li>Filters by date, user, and category</li>
                  <li>Total spent by each user</li>
                  <li>User activity logs and export options</li>
                </ul>
              </li>
            </ol>
          </section>
        </main>
      </div>
    </div>
  );
}
