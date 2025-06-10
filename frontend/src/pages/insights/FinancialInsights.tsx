import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import MetaTags from '../../components/MetaTags';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import ProtectedRoute from '../../components/ProtectedRoute';
import FinancialNav from '../../components/FinancialNav';
import { Line } from 'react-chartjs-2';

// Mock data - replace with real data from API
const insights = [
  {
    id: 1,
    title: 'High Spending in Food & Dining',
    description: 'Your spending in the Food & Dining category is 25% higher than your budget. Consider meal planning to reduce costs.',
    category: 'spending',
    priority: 'high',
    impact: 'medium',
    action: 'Review your food delivery subscriptions and dining out habits.',
  },
  {
    id: 2,
    title: 'Emergency Fund Below Target',
    description: 'Your emergency fund is at 75% of the recommended 6-month expenses. Consider increasing your monthly savings.',
    category: 'savings',
    priority: 'high',
    impact: 'high',
    action: 'Set up automatic transfers to your emergency fund.',
  },
  {
    id: 3,
    title: 'Investment Portfolio Rebalancing',
    description: 'Your portfolio allocation has drifted from your target. Consider rebalancing to maintain your risk profile.',
    category: 'investments',
    priority: 'medium',
    impact: 'high',
    action: 'Review your asset allocation and make necessary adjustments.',
  },
  {
    id: 4,
    title: 'Credit Card Interest Rate',
    description: 'You\'re paying high interest on your credit card balance. Consider transferring to a lower-rate card.',
    category: 'debt',
    priority: 'medium',
    impact: 'medium',
    action: 'Research balance transfer offers and create a debt payoff plan.',
  },
];

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

const FinancialInsights = () => {
  const [selectedInsight, setSelectedInsight] = useState<number | null>(null);

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

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high':
        return 'bg-red-500/10 text-red-500';
      case 'medium':
        return 'bg-yellow-500/10 text-yellow-500';
      case 'low':
        return 'bg-green-500/10 text-green-500';
      default:
        return 'bg-light-200 dark:bg-dark-700 text-light-600 dark:text-dark-300';
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
            <h1 className="text-3xl font-bold text-light-900 dark:text-dark-100">
              Financial Insights
            </h1>
            <p className="mt-2 text-light-600 dark:text-dark-300">
              Personalized recommendations and insights
            </p>
          </motion.div>

          {/* Financial Navigation */}
          <FinancialNav />

          {/* Financial Health Score */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8"
          >
            <div className="lg:col-span-2 bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Financial Health Score
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
                        title: {
                          display: true,
                          text: 'Score',
                        },
                      },
                    },
                  }}
                />
              </div>
            </div>
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Key Metrics
              </h2>
              <div className="space-y-4">
                <div className="p-4 bg-light-50 dark:bg-dark-700 rounded-xl">
                  <h3 className="font-medium text-light-900 dark:text-dark-100 mb-2">
                    Overall Score
                  </h3>
                  <p className="text-2xl font-bold text-primary-500">78/100</p>
                  <p className="text-sm text-light-600 dark:text-dark-300 mt-1">
                    +5% from last month
                  </p>
                </div>
                <div className="p-4 bg-light-50 dark:bg-dark-700 rounded-xl">
                  <h3 className="font-medium text-light-900 dark:text-dark-100 mb-2">
                    Areas of Focus
                  </h3>
                  <ul className="text-sm text-light-600 dark:text-dark-300 space-y-2">
                    <li>• Emergency Fund</li>
                    <li>• Investment Diversification</li>
                    <li>• Debt Management</li>
                  </ul>
                </div>
              </div>
            </div>
          </motion.div>

          {/* Insights Grid */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8"
          >
            {insights
              .filter(
                (insight) =>
                  !selectedInsight || insight.id === selectedInsight
              )
              .map((insight) => (
                <motion.div
                  key={insight.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.5, delay: 0.1 * insight.id }}
                  className="lg:col-span-1 bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
                >
                  <div className="flex items-center justify-between mb-4">
                    <h3 className="text-lg font-medium text-light-900 dark:text-dark-100">
                      {insight.title}
                    </h3>
                    <span className={`text-sm font-medium ${getPriorityColor(insight.priority)}`}>
                      {insight.priority.toUpperCase()}
                    </span>
                  </div>
                  <p className="text-light-600 dark:text-dark-300 mb-4">
                    {insight.description}
                  </p>
                  <div className="flex items-center justify-between">
                    <span
                      className={`px-3 py-1 rounded-full text-sm font-medium ${getImpactColor(
                        insight.impact
                      )}`}
                    >
                      {insight.impact.toUpperCase()} IMPACT
                    </span>
                    <button
                      onClick={() => setSelectedInsight(insight.id)}
                      className="text-primary-500 hover:text-primary-600 text-sm font-medium"
                    >
                      View Details
                    </button>
                  </div>
                </motion.div>
              ))}
          </motion.div>

          {/* Recommended Actions */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
          >
            <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
              Recommended Actions
            </h2>
            <div className="space-y-4">
              {insights.map((insight) => (
                <div
                  key={insight.id}
                  className="p-4 bg-light-50 dark:bg-dark-700 rounded-xl"
                >
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-medium text-light-900 dark:text-dark-100 mb-2">
                        {insight.title}
                      </h3>
                      <p className="text-sm text-light-600 dark:text-dark-300">
                        {insight.action}
                      </p>
                    </div>
                    <button className="px-4 py-2 bg-primary-500 text-white rounded-lg hover:bg-primary-600 transition-colors">
                      Take Action
                    </button>
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

export default FinancialInsights; 