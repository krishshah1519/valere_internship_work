import React, { useEffect, useState } from 'react';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import api from '../utils/axios';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];

const ExpenseLineChart = () => {
  const [year, setYear] = useState(() => {
    const now = new Date();
    return String(now.getFullYear());
  });
  const [monthlyData, setMonthlyData] = useState(Array(12).fill(0));

  useEffect(() => {
    api
      .get(`/expenses/yearly-chart/?year=${year}`, { withCredentials: true })
      .then((res) => {
        const summary = res.data.monthly_summary || [];
        const monthMap = {};
        summary.forEach((item) => {
          monthMap[item.month] = parseFloat(item.total);
        });
        const updatedData = MONTHS.map((month) => monthMap[month] || 0);
        setMonthlyData(updatedData);
      })
      .catch((err) => {
        console.error('Failed to fetch monthly summary', err);
      });
  }, [year]);

  const data = {
    labels: MONTHS,
    datasets: [
      {
        label: `Monthly Expenses (${year})`,
        data: monthlyData,
        fill: false,
        borderColor: '#3b82f6', // Tailwind blue-500
        backgroundColor: '#3b82f6',
        tension: 0.4,
        pointRadius: 4,
        pointHoverRadius: 6,
      },
    ],
  };

  const options = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        position: 'top',
        labels: {
          color: '#374151',
        },
      },
      title: {
        display: true,
        text: `Expense Trends for ${year}`,
        color: '#111827',
        font: {
          size: 18,
        },
      },
      tooltip: {
        callbacks: {
          label: (context) => `₹${context.parsed.y}`,
        },
      },
    },
    scales: {
      x: {
        ticks: {
          color: '#374151', // gray-700
        },
        grid: {
          color: '#e5e7eb', // gray-200
        },
      },
      y: {
        ticks: {
          color: '#374151', // gray-700
        },
        grid: {
          color: '#e5e7eb',
        },
      },
    },
  };

  return (
    <div className="bg-white text-gray-900 rounded-xl shadow-lg p-6">
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between mb-4">
        <h3 className="text-xl font-semibold">Expense Trends</h3>
        <div className="flex items-center gap-2 mt-2 sm:mt-0">
          <label htmlFor="year" className="text-sm font-medium">
            Select Year:
          </label>
          <input
            id="year"
            type="number"
            min="2000"
            max="2100"
            value={year}
            onChange={(e) => setYear(e.target.value)}
            className="px-2 py-1 w-28 rounded border border-gray-300 focus:outline-none focus:ring-2 focus:ring-blue-500 text-gray-800"
          />
        </div>
      </div>

      <div className="relative" style={{ height: '350px' }}>
        <Line data={data} options={options} />
      </div>
    </div>
  );
};

export default ExpenseLineChart;
