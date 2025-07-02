import React, { useState, useEffect } from 'react';
import api from '../utils/axios';

function ExportToExcel() {
  const [filterType, setFilterType] = useState('');
  const [month, setMonth] = useState('');
  const [category, setCategory] = useState('');
  const [categories, setCategories] = useState([]); // fetched from API
  const [startDate, setStartDate] = useState('');
  const [endDate, setEndDate] = useState('');

  useEffect(() => {
    const fetchCategories = async () => {
      try {
        const res = await api.get('/categories/', { withCredentials: true });
        setCategories(res.data.categories || []);
      } catch (error) {
        console.error('Failed to fetch categories:', error);
      }
    };
    fetchCategories();
  }, []);

  const handleExport = async () => {
    try {
      let payload = {};

      if (filterType === 'all') {
        // no filters, export all
      } else if (filterType === 'month') {
        if (!month) return alert("Please select a month.");
        payload.month = month;
      } else if (filterType === 'category') {
        if (!category) return alert("Please select a category.");
        payload.category = category;
      } else if (filterType === 'date_range') {
        if (!startDate || !endDate) return alert("Please select both start and end dates.");
        payload.start_date = startDate;
        payload.end_date = endDate;
      } else if (filterType === 'month_category') {
        if (!month || !category) return alert("Please select both month and category.");
        payload.month = month;
        payload.category = category;
      } else {
        return alert('Please select a filter type.');
      }

      const response = await api.post('/export/', payload, {
        responseType: 'blob',
        withCredentials: true,
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', 'expenses.xlsx');
      document.body.appendChild(link);
      link.click();
      link.remove();
    } catch (error) {
      console.error('Export failed:', error);
      alert('Failed to export data.');
    }
  };

  return (
    <div className="container mt-5">
      <div className="card shadow p-4">
        <div className="mb-3">
          <label className="form-label">Filter By</label>
          <select
            className="form-select"
            value={filterType}
            onChange={(e) => setFilterType(e.target.value)}
          >
            <option value="">-- Select Filter --</option>
            <option value="all">All Expenses</option>
            <option value="month">Month</option>
            <option value="category">Category</option>
            <option value="date_range">Start & End Date</option>
            <option value="month_category">Month + Category</option>
          </select>
        </div>

        {filterType === 'month' && (
          <div className="mb-3">
            <label className="form-label">Month (YYYY-MM)</label>
            <input
              type="month"
              className="form-control"
              value={month}
              onChange={(e) => setMonth(e.target.value)}
            />
          </div>
        )}

        {filterType === 'category' && (
          <div className="mb-3">
            <label className="form-label">Category</label>
            <select
              className="form-select"
              value={category}
              onChange={(e) => setCategory(e.target.value)}
            >
              <option value="">-- Select Category --</option>
              {categories.map((cat, index) => (
                <option key={index} value={cat}>{cat}</option>
              ))}
            </select>
          </div>
        )}

        {filterType === 'date_range' && (
          <div className="row mb-3">
            <div className="col-md-6">
              <label className="form-label">Start Date</label>
              <input
                type="date"
                className="form-control"
                value={startDate}
                onChange={(e) => setStartDate(e.target.value)}
              />
            </div>
            <div className="col-md-6">
              <label className="form-label">End Date</label>
              <input
                type="date"
                className="form-control"
                value={endDate}
                onChange={(e) => setEndDate(e.target.value)}
              />
            </div>
          </div>
        )}

        {filterType === 'month_category' && (
          <div className="row mb-3">
            <div className="col-md-6">
              <label className="form-label">Month (YYYY-MM)</label>
              <input
                type="month"
                className="form-control"
                value={month}
                onChange={(e) => setMonth(e.target.value)}
              />
            </div>
            <div className="col-md-6">
              <label className="form-label">Category</label>
              <select
                className="form-select"
                value={category}
                onChange={(e) => setCategory(e.target.value)}
              >
                <option value="">-- Select Category --</option>
                {categories.map((cat, index) => (
                  <option key={index} value={cat}>{cat}</option>
                ))}
              </select>
            </div>
          </div>
        )}

        <div className="text-center">
          <button className="btn btn-success px-4 py-2" onClick={handleExport}>
            ⬇️ Export to Excel
          </button>
        </div>
      </div>
    </div>
  );
}

export default ExportToExcel;
