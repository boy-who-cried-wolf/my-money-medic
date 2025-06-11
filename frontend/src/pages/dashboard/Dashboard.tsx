import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import { useState, useEffect } from 'react';
import Footer from '../../components/Footer';
import MetaTags from '../../components/MetaTags';
import Navbar from '../../components/Navbar';
import ProtectedRoute from '../../components/ProtectedRoute';
import { Line, Doughnut, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  BarElement,
} from 'chart.js';

// Register ChartJS components
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
  ArcElement
);

// Mock data - replace with real data from API
const metrics = [
  {
    title: 'Financial Health Score',
    value: '78',
    change: '+5%',
    trend: 'up',
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
      </svg>
    ),
  },
  {
    title: 'Monthly Savings',
    value: '£850',
    change: '+12%',
    trend: 'up',
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
  {
    title: 'Investment Returns',
    value: '£2,450',
    change: '+8.3%',
    trend: 'up',
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    ),
  },
  {
    title: 'Debt Reduction',
    value: '£1,200',
    change: '-15%',
    trend: 'down',
    icon: (
      <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0V9m0 8l-8-8-4 4-6-6" />
      </svg>
    ),
  },
];

const recentTransactions = [
  {
    id: 1,
    description: 'Grocery Shopping',
    amount: '-£85.50',
    date: '2024-03-15',
    category: 'Food & Dining',
  },
  {
    id: 2,
    description: 'Salary Deposit',
    amount: '+£2,800.00',
    date: '2024-03-14',
    category: 'Income',
  },
  {
    id: 3,
    description: 'Electric Bill',
    amount: '-£65.00',
    date: '2024-03-13',
    category: 'Utilities',
  },
  {
    id: 4,
    description: 'Investment Dividend',
    amount: '+£120.00',
    date: '2024-03-12',
    category: 'Investment',
  },
];

// Chart data
const financialHealthData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Financial Health Score',
      data: [65, 68, 72, 70, 75, 78],
      borderColor: 'rgb(99, 102, 241)',
      backgroundColor: 'rgba(99, 102, 241, 0.1)',
      tension: 0.4,
      fill: true,
    },
  ],
};

const spendingByCategoryData = {
  labels: ['Housing', 'Food', 'Transport', 'Entertainment', 'Utilities', 'Other'],
  datasets: [
    {
      data: [35, 25, 15, 10, 10, 5],
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

const savingsGoalsData = {
  labels: ['Emergency Fund', 'House Deposit', 'Retirement', 'Vacation'],
  datasets: [
    {
      label: 'Progress',
      data: [75, 45, 30, 60],
      backgroundColor: 'rgba(99, 102, 241, 0.8)',
    },
  ],
};

const Dashboard = () => {
  return (
    <ProtectedRoute>
      <MetaTags />
      <div className="min-h-screen flex flex-col bg-light-50 dark:bg-dark-900">
        <Navbar />
        <main className="flex-grow container-custom py-8 mt-16">
          {/* Welcome Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-8"
          >
            <h1 className="text-3xl font-bold text-light-900 dark:text-dark-100">
              Welcome back, <span className="text-primary-500">John</span>
            </h1>
            <p className="mt-2 text-light-600 dark:text-dark-300">
              Here's an overview of your financial health
            </p>
          </motion.div>

          {/* Metrics Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {metrics.map((metric, index) => (
              <motion.div
                key={metric.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
              >
                <div className="flex items-center justify-between mb-4">
                  <div className="p-2 bg-primary-500/10 rounded-lg text-primary-500">
                    {metric.icon}
                  </div>
                  <span className={`text-sm font-medium ${
                    metric.trend === 'up' ? 'text-green-500' : 'text-red-500'
                  }`}>
                    {metric.change}
                  </span>
                </div>
                <h3 className="text-sm font-medium text-light-600 dark:text-dark-300 mb-1">
                  {metric.title}
                </h3>
                <p className="text-2xl font-bold text-light-900 dark:text-dark-100">
                  {metric.value}
                </p>
              </motion.div>
            ))}
          </div>

          {/* Main Content Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
            {/* Financial Health Chart */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.4 }}
              className="lg:col-span-2 bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
            >
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Financial Health Overview
              </h2>
              <div className="h-80">
                <Line
                  data={financialHealthData}
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
                        max: 100,
                      },
                    },
                  }}
                />
              </div>
            </motion.div>

            {/* Recent Transactions */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.5 }}
              className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100">
                  Recent Transactions
                </h2>
                <Link to="/transactions" className="text-sm font-medium text-primary-500 hover:text-primary-600">
                  View all
                </Link>
              </div>
              <div className="space-y-4">
                {recentTransactions.map((transaction) => (
                  <div
                    key={transaction.id}
                    className="flex items-center justify-between p-4 bg-light-50 dark:bg-dark-700 rounded-lg"
                  >
                    <div>
                      <p className="font-medium text-light-900 dark:text-dark-100">
                        {transaction.description}
                      </p>
                      <p className="text-sm text-light-600 dark:text-dark-300">
                        {transaction.category}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className={`font-medium ${
                        transaction.amount.startsWith('+') ? 'text-green-500' : 'text-red-500'
                      }`}>
                        {transaction.amount}
                      </p>
                      <p className="text-sm text-light-600 dark:text-dark-300">
                        {transaction.date}
                      </p>
                    </div>
                  </div>
                ))}
              </div>
            </motion.div>

            {/* Spending Analysis */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.6 }}
              className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
            >
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Spending by Category
              </h2>
              <div className="h-80">
                <Doughnut
                  data={spendingByCategoryData}
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

            {/* Savings Goals */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.7 }}
              className="lg:col-span-2 bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
            >
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100">
                  Savings Goals Progress
                </h2>
                <Link to="/goals" className="text-sm font-medium text-primary-500 hover:text-primary-600">
                  Manage Goals
                </Link>
              </div>
              <div className="h-80">
                <Bar
                  data={savingsGoalsData}
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
                        max: 100,
                        title: {
                          display: true,
                          text: 'Progress (%)',
                        },
                      },
                    },
                  }}
                />
              </div>
            </motion.div>
          </div>
        </main>
        <Footer />
      </div>
    </ProtectedRoute>
  );
};

export default Dashboard; 