import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import MetaTags from '../../components/MetaTags';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import ProtectedRoute from '../../components/ProtectedRoute';
import { Bar } from 'react-chartjs-2';

// Mock data - replace with real data from API
const savingsGoals = [
  {
    id: 1,
    name: 'Emergency Fund',
    target: 10000,
    current: 7500,
    deadline: '2024-12-31',
    priority: 'high',
    category: 'safety',
  },
  {
    id: 2,
    name: 'House Deposit',
    target: 50000,
    current: 22500,
    deadline: '2025-06-30',
    priority: 'high',
    category: 'housing',
  },
  {
    id: 3,
    name: 'Retirement',
    target: 500000,
    current: 150000,
    deadline: '2045-12-31',
    priority: 'medium',
    category: 'retirement',
  },
  {
    id: 4,
    name: 'Vacation Fund',
    target: 5000,
    current: 3000,
    deadline: '2024-08-31',
    priority: 'low',
    category: 'leisure',
  },
];

const goalProgressData = {
  labels: savingsGoals.map(goal => goal.name),
  datasets: [
    {
      label: 'Progress',
      data: savingsGoals.map(goal => (goal.current / goal.target) * 100),
      backgroundColor: 'rgba(99, 102, 241, 0.8)',
    },
  ],
};

const SavingsGoals = () => {
  const [selectedGoal, setSelectedGoal] = useState<number | null>(null);
  const [showAddGoal, setShowAddGoal] = useState(false);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: 'GBP',
    }).format(amount);
  };

  const calculateProgress = (current: number, target: number) => {
    return Math.round((current / target) * 100);
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'text-red-500';
      case 'medium':
        return 'text-yellow-500';
      case 'low':
        return 'text-green-500';
      default:
        return 'text-light-600 dark:text-dark-300';
    }
  };

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
            <div className="flex justify-between items-center">
              <div>
                <h1 className="text-3xl font-bold text-light-900 dark:text-dark-100">
                  Savings Goals
                </h1>
                <p className="mt-2 text-light-600 dark:text-dark-300">
                  Track and manage your financial goals
                </p>
              </div>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                onClick={() => setShowAddGoal(true)}
                className="px-6 py-3 bg-primary-500 text-white rounded-xl hover:bg-primary-600 transition-colors"
              >
                Add New Goal
              </motion.button>
            </div>
          </motion.div>

          {/* Goals Overview */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
          >
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-sm font-medium text-light-600 dark:text-dark-300 mb-2">
                Total Goals
              </h3>
              <p className="text-2xl font-bold text-light-900 dark:text-dark-100">
                {savingsGoals.length}
              </p>
            </div>
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-sm font-medium text-light-600 dark:text-dark-300 mb-2">
                Total Target
              </h3>
              <p className="text-2xl font-bold text-light-900 dark:text-dark-100">
                {formatCurrency(savingsGoals.reduce((sum, goal) => sum + goal.target, 0))}
              </p>
            </div>
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-sm font-medium text-light-600 dark:text-dark-300 mb-2">
                Total Saved
              </h3>
              <p className="text-2xl font-bold text-light-900 dark:text-dark-100">
                {formatCurrency(savingsGoals.reduce((sum, goal) => sum + goal.current, 0))}
              </p>
            </div>
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-sm font-medium text-light-600 dark:text-dark-300 mb-2">
                Average Progress
              </h3>
              <p className="text-2xl font-bold text-light-900 dark:text-dark-100">
                {Math.round(
                  savingsGoals.reduce(
                    (sum, goal) => sum + calculateProgress(goal.current, goal.target),
                    0
                  ) / savingsGoals.length
                )}
                %
              </p>
            </div>
          </motion.div>

          {/* Goals Progress Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8"
          >
            <div className="lg:col-span-2 bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Goals Progress
              </h2>
              <div className="h-80">
                <Bar
                  data={goalProgressData}
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
            </div>
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Goals Summary
              </h2>
              <div className="space-y-4">
                {savingsGoals.map((goal) => (
                  <div key={goal.id} className="p-4 bg-light-50 dark:bg-dark-700 rounded-xl">
                    <div className="flex justify-between items-center mb-2">
                      <h3 className="font-medium text-light-900 dark:text-dark-100">
                        {goal.name}
                      </h3>
                      <span className={`text-sm font-medium ${getPriorityColor(goal.priority)}`}>
                        {goal.priority.toUpperCase()}
                      </span>
                    </div>
                    <div className="text-sm text-light-600 dark:text-dark-300">
                      <p>Target: {formatCurrency(goal.target)}</p>
                      <p>Current: {formatCurrency(goal.current)}</p>
                      <p>Progress: {calculateProgress(goal.current, goal.target)}%</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </motion.div>

          {/* Goals List */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
          >
            <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
              Your Goals
            </h2>
            <div className="space-y-4">
              {savingsGoals.map((goal) => (
                <div
                  key={goal.id}
                  className="p-6 bg-light-50 dark:bg-dark-700 rounded-xl"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-medium text-light-900 dark:text-dark-100">
                        {goal.name}
                      </h3>
                      <p className="text-sm text-light-600 dark:text-dark-300">
                        Target: {formatCurrency(goal.target)}
                      </p>
                    </div>
                    <span className={`text-sm font-medium ${getPriorityColor(goal.priority)}`}>
                      {goal.priority.toUpperCase()}
                    </span>
                  </div>
                  <div className="mb-4">
                    <div className="flex justify-between text-sm text-light-600 dark:text-dark-300 mb-2">
                      <span>Progress</span>
                      <span>{calculateProgress(goal.current, goal.target)}%</span>
                    </div>
                    <div className="w-full bg-light-200 dark:bg-dark-600 rounded-full h-2">
                      <div
                        className="bg-primary-500 h-2 rounded-full"
                        style={{
                          width: `${calculateProgress(goal.current, goal.target)}%`,
                        }}
                      />
                    </div>
                  </div>
                  <div className="flex justify-between items-center">
                    <div className="text-sm text-light-600 dark:text-dark-300">
                      <p>Current: {formatCurrency(goal.current)}</p>
                      <p>Remaining: {formatCurrency(goal.target - goal.current)}</p>
                    </div>
                    <div className="text-sm text-light-600 dark:text-dark-300">
                      <p>Deadline: {new Date(goal.deadline).toLocaleDateString()}</p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </motion.div>
        </main>
        <Footer />
      </div>
    </ProtectedRoute>
  );
};

export default SavingsGoals; 