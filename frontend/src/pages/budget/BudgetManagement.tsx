import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import MetaTags from '../../components/MetaTags';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import ProtectedRoute from '../../components/ProtectedRoute';
import FinancialNav from '../../components/FinancialNav';
import { Bar, Doughnut } from 'react-chartjs-2';

// Mock data - replace with real data from API
const budgetCategories = [
  {
    id: 1,
    name: 'Housing',
    budget: 1200,
    spent: 1200,
    remaining: 0,
    percentage: 100,
    trend: 'stable',
  },
  {
    id: 2,
    name: 'Food & Dining',
    budget: 600,
    spent: 450,
    remaining: 150,
    percentage: 75,
    trend: 'down',
  },
  {
    id: 3,
    name: 'Transportation',
    budget: 300,
    spent: 280,
    remaining: 20,
    percentage: 93,
    trend: 'up',
  },
  {
    id: 4,
    name: 'Entertainment',
    budget: 200,
    spent: 150,
    remaining: 50,
    percentage: 75,
    trend: 'stable',
  },
  {
    id: 5,
    name: 'Utilities',
    budget: 250,
    spent: 230,
    remaining: 20,
    percentage: 92,
    trend: 'stable',
  },
  {
    id: 6,
    name: 'Shopping',
    budget: 300,
    spent: 180,
    remaining: 120,
    percentage: 60,
    trend: 'down',
  },
];

const monthlyBudgetData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Budget',
      data: [2850, 2850, 2850, 2850, 2850, 2850],
      backgroundColor: 'rgba(99, 102, 241, 0.2)',
      borderColor: 'rgb(99, 102, 241)',
      borderWidth: 2,
    },
    {
      label: 'Spent',
      data: [2700, 2800, 2600, 2750, 2680, 2490],
      backgroundColor: 'rgba(16, 185, 129, 0.2)',
      borderColor: 'rgb(16, 185, 129)',
      borderWidth: 2,
    },
  ],
};

const budgetAllocationData = {
  labels: budgetCategories.map(cat => cat.name),
  datasets: [
    {
      data: budgetCategories.map(cat => cat.budget),
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

const BudgetManagement = () => {
  const [selectedMonth, setSelectedMonth] = useState('current');
  const [selectedCategory, setSelectedCategory] = useState<number | null>(null);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: 'GBP',
    }).format(amount);
  };

  const getTrendColor = (trend: string) => {
    switch (trend) {
      case 'up':
        return 'text-red-500';
      case 'down':
        return 'text-green-500';
      case 'stable':
        return 'text-light-600 dark:text-dark-300';
      default:
        return 'text-light-600 dark:text-dark-300';
    }
  };

  const totalBudget = budgetCategories.reduce((sum, cat) => sum + cat.budget, 0);
  const totalSpent = budgetCategories.reduce((sum, cat) => sum + cat.spent, 0);
  const totalRemaining = totalBudget - totalSpent;
  const overallProgress = (totalSpent / totalBudget) * 100;

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
                  Budget Management
                </h1>
                <p className="mt-2 text-light-600 dark:text-dark-300">
                  Track and manage your monthly budget
                </p>
              </div>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="px-6 py-3 bg-primary-500 text-white rounded-xl hover:bg-primary-600 transition-colors"
              >
                Create Budget
              </motion.button>
            </div>
          </motion.div>

          {/* Financial Navigation */}
          <FinancialNav />

          {/* Month Selector */}
          <div className="mb-8">
            <div className="flex space-x-4">
              {['previous', 'current', 'next'].map((month) => (
                <button
                  key={month}
                  onClick={() => setSelectedMonth(month)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    selectedMonth === month
                      ? 'bg-primary-500 text-white'
                      : 'text-light-600 dark:text-dark-300 hover:bg-light-100 dark:hover:bg-dark-800'
                  }`}
                >
                  {month.charAt(0).toUpperCase() + month.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Budget Overview */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
          >
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-sm font-medium text-light-600 dark:text-dark-300 mb-2">
                Total Budget
              </h3>
              <p className="text-2xl font-bold text-light-900 dark:text-dark-100">
                {formatCurrency(totalBudget)}
              </p>
            </div>
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-sm font-medium text-light-600 dark:text-dark-300 mb-2">
                Total Spent
              </h3>
              <p className="text-2xl font-bold text-light-900 dark:text-dark-100">
                {formatCurrency(totalSpent)}
              </p>
            </div>
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-sm font-medium text-light-600 dark:text-dark-300 mb-2">
                Remaining
              </h3>
              <p className="text-2xl font-bold text-green-500">
                {formatCurrency(totalRemaining)}
              </p>
            </div>
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-sm font-medium text-light-600 dark:text-dark-300 mb-2">
                Overall Progress
              </h3>
              <p className="text-2xl font-bold text-light-900 dark:text-dark-100">
                {Math.round(overallProgress)}%
              </p>
            </div>
          </motion.div>

          {/* Budget Charts */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8"
          >
            <div className="lg:col-span-2 bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Monthly Budget vs Spent
              </h2>
              <div className="h-80">
                <Bar
                  data={monthlyBudgetData}
                  options={{
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                      legend: {
                        position: 'top',
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
            </div>

            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Budget Allocation
              </h2>
              <div className="h-80">
                <Doughnut
                  data={budgetAllocationData}
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
            </div>
          </motion.div>

          {/* Budget Categories */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
          >
            <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
              Budget Categories
            </h2>
            <div className="space-y-4">
              {budgetCategories.map((category) => (
                <div
                  key={category.id}
                  className="p-6 bg-light-50 dark:bg-dark-700 rounded-xl"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-medium text-light-900 dark:text-dark-100">
                        {category.name}
                      </h3>
                      <p className="text-sm text-light-600 dark:text-dark-300">
                        Budget: {formatCurrency(category.budget)}
                      </p>
                    </div>
                    <span className={`text-sm font-medium ${getTrendColor(category.trend)}`}>
                      {category.trend === 'up' ? '↑' : category.trend === 'down' ? '↓' : '→'}
                    </span>
                  </div>
                  <div className="mb-4">
                    <div className="flex justify-between text-sm text-light-600 dark:text-dark-300 mb-2">
                      <span>Progress</span>
                      <span>{category.percentage}%</span>
                    </div>
                    <div className="w-full bg-light-200 dark:bg-dark-600 rounded-full h-2">
                      <div
                        className={`h-2 rounded-full ${
                          category.percentage > 90
                            ? 'bg-red-500'
                            : category.percentage > 75
                            ? 'bg-yellow-500'
                            : 'bg-green-500'
                        }`}
                        style={{ width: `${category.percentage}%` }}
                      />
                    </div>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <p className="text-sm text-light-600 dark:text-dark-300 mb-1">
                        Spent
                      </p>
                      <p className="text-lg font-bold text-light-900 dark:text-dark-100">
                        {formatCurrency(category.spent)}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-light-600 dark:text-dark-300 mb-1">
                        Remaining
                      </p>
                      <p className="text-lg font-bold text-green-500">
                        {formatCurrency(category.remaining)}
                      </p>
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

export default BudgetManagement; 