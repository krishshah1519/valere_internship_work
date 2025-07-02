import React, { useEffect, useState } from 'react';
import { Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  ArcElement,
  Tooltip,
  Legend,
  Title,
} from 'chart.js';
import api from '../utils/axios';

ChartJS.register(ArcElement, Tooltip, Legend, Title);

const COLORS = ['#3b82f6', '#10b981', '#facc15', '#f97316', '#8b5cf6', '#ef4444'];

const ExpensePieChart = () => {
  const [data, setData] = useState([]);
  const [selectedMonth, setSelectedMonth] = useState(() => {
    const now = new Date();
    return `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}`;
  });

  useEffect(() => {
    if (!selectedMonth) return;

    api
      .get(`/expenses/chart/?month=${selectedMonth}`, { withCredentials: true })
      .then((res) => {
        const categorySummary = res.data.category_summary || [];
        setData(categorySummary);
      })
      .catch((err) => {
        console.error('Failed to load chart data:', err);
      });
  }, [selectedMonth]);

  const chartData = {
    labels: data.map((item) => item.category),
    datasets: [
      {
        label: 'Expenses',
        data: data.map((item) => parseFloat(item.total)),
        backgroundColor: data.map((_, index) => COLORS[index % COLORS.length]),
        borderWidth: 1,
      },
    ],
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          color: '#374151', // gray-700
        },
      },
      title: {
        display: true,
        text: `Expense Distribution for ${selectedMonth}`,
        color: '#111827', // gray-900
        font: {
          size: 18,
        },
      },
      tooltip: {
        callbacks: {
          label: (context) => {
            const label = context.label || '';
            const value = context.raw || 0;
            return `${label}: ₹${value}`;
          },
        },
      },
    },
  };

  const handleMonthChange = (e) => {
    setSelectedMonth(e.target.value);
  };

  return (
    <div className="bg-white text-gray-900 rounded-xl shadow-lg p-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4">
        <h3 className="text-xl font-semibold">Expenses by Category</h3>
        <div className="flex items-center gap-2 mt-2 sm:mt-0">
          <label htmlFor="month" className="text-sm font-medium">
            Select Month:
          </label>
          <input
            id="month"
            type="month"
            value={selectedMonth}
            onChange={handleMonthChange}
            className="px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800"
          />
        </div>
      </div>

      <div className="relative" style={{ height: '350px' }}>
        {data.length > 0 ? (
          <Pie data={chartData} options={chartOptions} />
        ) : (
          <div className="h-full flex items-center justify-center text-gray-500">
            No expense data available for this month.
          </div>
        )}
      </div>
    </div>
  );
};

export default ExpensePieChart;
