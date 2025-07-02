import React, { useEffect, useState } from "react";
import api from "../utils/axios";

const AdminDashboard = () => {
  const [users, setUsers]                 = useState([]);    // table data
  const [categories, setCategories]       = useState([]);    // category dropdown
  const [filterUser, setFilterUser]       = useState("");
  const [filterStartDate, setFilterStartDate] = useState("");
  const [filterEndDate, setFilterEndDate]     = useState("");
  const [filterCategory, setFilterCategory] = useState("");
  const [error, setError]                 = useState("");

  // load categories once
  useEffect(() => {
    api.get("/admin/categories/")
      .then(res => setCategories(res.data.categories))
      .catch(() => setError("Not authorized"));
  }, []);

  // whenever any filter changes, re‑fetch the summary
  useEffect(() => {
    const fetchSummary = async () => {
      try {
        const res = await api.get("/admin/summary/", {
          params: {
            user_id:    filterUser    || undefined,
            start_date: filterStartDate || undefined,
            end_date:   filterEndDate   || undefined,
            category:   filterCategory || undefined,
          }
        });
        setUsers(res.data);
      } catch {
        setError("Failed to load summary.");
      }
    };

    fetchSummary();
  }, [filterUser, filterStartDate, filterEndDate, filterCategory]);

  // export with same filters
  const handleExport = async () => {
    try {
      const res = await api.post(
        "/export/",
        {
          user_id:    filterUser,
          start_date: filterStartDate,
          end_date:   filterEndDate,
          category:   filterCategory,
        },
        { responseType: "blob" }
      );
      const url  = window.URL.createObjectURL(new Blob([res.data]));
      const link = document.createElement("a");
      link.href     = url;
      link.download = "expenses.xlsx";
      document.body.appendChild(link);
      link.click();
    } catch {
      alert("Export failed. Check backend logs.");
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-6">📊 Admin Dashboard</h1>
      {error && <p className="text-red-500 mb-4">{error}</p>}

      {/* Dynamic Filters */}
      <div className="grid grid-cols-1 sm:grid-cols-5 gap-4 mb-6">
        {/* User */}
        <div>
          <label className="block text-sm mb-1">User</label>
          <select
            className="w-full border rounded p-2"
            value={filterUser}
            onChange={e => setFilterUser(e.target.value)}
          >
            <option value="">All</option>
            {users.map(u => (
              <option key={u.id} value={u.id}>{u.username}</option>
            ))}
          </select>
        </div>

        {/* Start Date */}
        <div>
          <label className="block text-sm mb-1">Start Date</label>
          <input
            type="date"
            className="w-full border rounded p-2"
            value={filterStartDate}
            onChange={e => setFilterStartDate(e.target.value)}
          />
        </div>

        {/* End Date */}
        <div>
          <label className="block text-sm mb-1">End Date</label>
          <input
            type="date"
            className="w-full border rounded p-2"
            value={filterEndDate}
            onChange={e => setFilterEndDate(e.target.value)}
          />
        </div>

        {/* Category */}
        <div>
          <label className="block text-sm mb-1">Category</label>
          <select
            className="w-full border rounded p-2"
            value={filterCategory}
            onChange={e => setFilterCategory(e.target.value)}
          >
            <option value="">All</option>
            {categories.map((c,i) => (
              <option key={i} value={c}>{c}</option>
            ))}
          </select>
        </div>

        {/* Export Button */}
        <div className="flex items-end">
          <button
            onClick={handleExport}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 w-full"
          >
            Export Data
          </button>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-x-auto">
        <table className="min-w-full bg-white border border-gray-300">
          <thead>
            <tr className="bg-gray-100">
              <th className="py-2 px-4 border">Username</th>
              <th className="py-2 px-4 border">Email</th>
              <th className="py-2 px-4 border">Total Spent (₹)</th>
            </tr>
          </thead>
          <tbody>
            {users.map(user => (
              <tr key={user.id} className="text-center">
                <td className="py-2 px-4 border">{user.username}</td>
                <td className="py-2 px-4 border">{user.email}</td>
                <td className="py-2 px-4 border">₹{user.total_spent}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default AdminDashboard;
