import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import MetaTags from '../../components/MetaTags';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import ProtectedRoute from '../../components/ProtectedRoute';
import FinancialNav from '../../components/FinancialNav';
import { Bar, Doughnut, Line } from 'react-chartjs-2';

// Mock data - replace with real data from API
const spendingCategories = [
  { name: 'Housing', amount: 1200, percentage: 35, trend: 'stable' },
  { name: 'Food', amount: 850, percentage: 25, trend: 'up' },
  { name: 'Transport', amount: 510, percentage: 15, trend: 'down' },
  { name: 'Entertainment', amount: 340, percentage: 10, trend: 'up' },
  { name: 'Utilities', amount: 340, percentage: 10, trend: 'stable' },
  { name: 'Other', amount: 170, percentage: 5, trend: 'stable' },
];

const monthlySpendingData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Total Spending',
      data: [3200, 3400, 3300, 3500, 3400, 3410],
      borderColor: 'rgb(99, 102, 241)',
      backgroundColor: 'rgba(99, 102, 241, 0.1)',
      tension: 0.4,
      fill: true,
    },
  ],
};

const categorySpendingData = {
  labels: spendingCategories.map(cat => cat.name),
  datasets: [
    {
      data: spendingCategories.map(cat => cat.amount),
      backgroundColor: [
        'rgba(99, 102, 241, 0.8)',
        'rgba(16, 185, 129, 0.8)',
        'rgba(245, 158, 11, 0.8)',
        'rgba(239, 68, 68, 0.8)',
        'rgba(139, 92, 246, 0.8)',
        'rgba(107, 114, 128, 0.8)',
      ],
    },
  ],
};

const SpendingAnalysis = () => {
  const [timeRange, setTimeRange] = useState('month');
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  return (
    <ProtectedRoute>
      <MetaTags />
      <div className="min-h-screen flex flex-col bg-light-50 dark:bg-dark-900">
        <Navbar />
        <main className="flex-grow container-custom py-8 mt-16">
          {/* Header */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-8"
          >
            <h1 className="text-3xl font-bold text-light-900 dark:text-dark-100">
              Spending Analysis
            </h1>
            <p className="mt-2 text-light-600 dark:text-dark-300">
              Track and analyze your spending patterns
            </p>
          </motion.div>

          {/* Financial Navigation */}
          <FinancialNav />

          {/* Time Range Selector */}
          <div className="mb-8">
            <div className="flex space-x-4">
              {['week', 'month', 'quarter', 'year'].map((range) => (
                <button
                  key={range}
                  onClick={() => setTimeRange(range)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    timeRange === range
                      ? 'bg-primary-500 text-white'
                      : 'text-light-600 dark:text-dark-300 hover:bg-light-100 dark:hover:bg-dark-800'
                  }`}
                >
                  {range.charAt(0).toUpperCase() + range.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Monthly Spending Trend */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="lg:col-span-2 bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
            >
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Monthly Spending Trend
              </h2>
              <div className="h-80">
                <Line
                  data={monthlySpendingData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        display: false,
                      },
                    },
                    scales: {
                      y: {
                        beginAtZero: true,
                        title: {
                          display: true,
                          text: 'Amount (£)',
                        },
                      },
                    },
                  }}
                />
              </div>
            </motion.div>

            {/* Spending by Category */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.3 }}
              className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
            >
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Spending by Category
              </h2>
              <div className="h-80">
                <Doughnut
                  data={categorySpendingData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'bottom',
                      },
                    },
                  }}
                />
              </div>
            </motion.div>

            {/* Category Breakdown */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
              className="lg:col-span-3 bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
            >
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Category Breakdown
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                {spendingCategories.map((category) => (
                  <div
                    key={category.name}
                    className="p-4 bg-light-50 dark:bg-dark-700 rounded-xl"
                  >
                    <div className="flex items-center justify-between mb-2">
                      <h3 className="font-medium text-light-900 dark:text-dark-100">
                        {category.name}
                      </h3>
                      <span className={`text-sm font-medium ${
                        category.trend === 'up'
                          ? 'text-red-500'
                          : category.trend === 'down'
                          ? 'text-green-500'
                          : 'text-light-600 dark:text-dark-300'
                      }`}>
                        {category.trend === 'up' ? '↑' : category.trend === 'down' ? '↓' : '→'}
                      </span>
                    </div>
                    <p className="text-2xl font-bold text-light-900 dark:text-dark-100 mb-1">
                      £{category.amount}
                    </p>
                    <div className="w-full bg-light-200 dark:bg-dark-600 rounded-full h-2">
                      <div
                        className="bg-primary-500 h-2 rounded-full"
                        style={{ width: `${category.percentage}%` }}
                      />
                    </div>
                    <p className="text-sm text-light-600 dark:text-dark-300 mt-1">
                      {category.percentage}% of total spending
                    </p>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Spending Insights */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.5 }}
              className="lg:col-span-3 bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
            >
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Spending Insights
              </h2>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="p-6 bg-light-50 dark:bg-dark-700 rounded-xl">
                  <h3 className="font-medium text-light-900 dark:text-dark-100 mb-2">
                    Top Spending Category
                  </h3>
                  <p className="text-2xl font-bold text-primary-500 mb-1">
                    Housing
                  </p>
                  <p className="text-sm text-light-600 dark:text-dark-300">
                    35% of your total spending
                  </p>
                </div>
                <div className="p-6 bg-light-50 dark:bg-dark-700 rounded-xl">
                  <h3 className="font-medium text-light-900 dark:text-dark-100 mb-2">
                    Fastest Growing Category
                  </h3>
                  <p className="text-2xl font-bold text-red-500 mb-1">
                    Food & Dining
                  </p>
                  <p className="text-sm text-light-600 dark:text-dark-300">
                    Increased by 15% this month
                  </p>
                </div>
                <div className="p-6 bg-light-50 dark:bg-dark-700 rounded-xl">
                  <h3 className="font-medium text-light-900 dark:text-dark-100 mb-2">
                    Potential Savings
                  </h3>
                  <p className="text-2xl font-bold text-green-500 mb-1">
                    £340
                  </p>
                  <p className="text-sm text-light-600 dark:text-dark-300">
                    Based on your spending patterns
                  </p>
                </div>
              </div>
            </motion.div>
          </div>
        </main>
        <Footer />
      </div>
    </ProtectedRoute>
  );
};

export default SpendingAnalysis; 