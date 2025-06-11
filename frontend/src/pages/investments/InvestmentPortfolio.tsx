import { useState } from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import MetaTags from '../../components/MetaTags';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import ProtectedRoute from '../../components/ProtectedRoute';
import { Line, Doughnut } from 'react-chartjs-2';

// Mock data - replace with real data from API
const investments = [
  {
    id: 1,
    name: 'Vanguard S&P 500 ETF',
    type: 'ETF',
    value: 25000,
    allocation: 40,
    return: 12.5,
    risk: 'medium',
    category: 'stocks',
  },
  {
    id: 2,
    name: 'UK Government Bonds',
    type: 'Bond',
    value: 15000,
    allocation: 25,
    return: 4.2,
    risk: 'low',
    category: 'bonds',
  },
  {
    id: 3,
    name: 'Tech Growth Fund',
    type: 'Mutual Fund',
    value: 10000,
    allocation: 15,
    return: 18.7,
    risk: 'high',
    category: 'stocks',
  },
  {
    id: 4,
    name: 'Real Estate Investment Trust',
    type: 'REIT',
    value: 8000,
    allocation: 12,
    return: 8.3,
    risk: 'medium',
    category: 'real_estate',
  },
  {
    id: 5,
    name: 'Gold ETF',
    type: 'ETF',
    value: 5000,
    allocation: 8,
    return: 5.1,
    risk: 'low',
    category: 'commodities',
  },
];

const portfolioValueData = {
  labels: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
  datasets: [
    {
      label: 'Portfolio Value',
      data: [58000, 59500, 61200, 59800, 62500, 63000],
      borderColor: 'rgb(99, 102, 241)',
      backgroundColor: 'rgba(99, 102, 241, 0.1)',
      tension: 0.4,
      fill: true,
    },
  ],
};

const allocationData = {
  labels: investments.map(inv => inv.name),
  datasets: [
    {
      data: investments.map(inv => inv.allocation),
      backgroundColor: [
        'rgba(99, 102, 241, 0.8)',
        'rgba(16, 185, 129, 0.8)',
        'rgba(245, 158, 11, 0.8)',
        'rgba(239, 68, 68, 0.8)',
        'rgba(139, 92, 246, 0.8)',
      ],
    },
  ],
};

const InvestmentPortfolio = () => {
  const [timeRange, setTimeRange] = useState('6m');
  const [selectedInvestment, setSelectedInvestment] = useState<number | null>(null);

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-GB', {
      style: 'currency',
      currency: 'GBP',
    }).format(amount);
  };

  const getRiskColor = (risk: string) => {
    switch (risk) {
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

  const totalValue = investments.reduce((sum, inv) => sum + inv.value, 0);
  const totalReturn = investments.reduce(
    (sum, inv) => sum + (inv.value * inv.return) / 100,
    0
  );

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
                  Investment Portfolio
                </h1>
                <p className="mt-2 text-light-600 dark:text-dark-300">
                  Track and manage your investments
                </p>
              </div>
              <motion.button
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className="px-6 py-3 bg-primary-500 text-white rounded-xl hover:bg-primary-600 transition-colors"
              >
                Add Investment
              </motion.button>
            </div>
          </motion.div>

          {/* Time Range Selector */}
          <div className="mb-8">
            <div className="flex space-x-4">
              {['1m', '3m', '6m', '1y', 'all'].map((range) => (
                <button
                  key={range}
                  onClick={() => setTimeRange(range)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                    timeRange === range
                      ? 'bg-primary-500 text-white'
                      : 'text-light-600 dark:text-dark-300 hover:bg-light-100 dark:hover:bg-dark-800'
                  }`}
                >
                  {range.toUpperCase()}
                </button>
              ))}
            </div>
          </div>

          {/* Portfolio Overview */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8"
          >
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-sm font-medium text-light-600 dark:text-dark-300 mb-2">
                Total Portfolio Value
              </h3>
              <p className="text-2xl font-bold text-light-900 dark:text-dark-100">
                {formatCurrency(totalValue)}
              </p>
            </div>
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-sm font-medium text-light-600 dark:text-dark-300 mb-2">
                Total Return
              </h3>
              <p className="text-2xl font-bold text-green-500">
                {formatCurrency(totalReturn)}
              </p>
            </div>
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-sm font-medium text-light-600 dark:text-dark-300 mb-2">
                Average Return
              </h3>
              <p className="text-2xl font-bold text-light-900 dark:text-dark-100">
                {(
                  investments.reduce(
                    (sum, inv) => sum + (inv.return * inv.allocation) / 100,
                    0
                  )
                ).toFixed(1)}
                %
              </p>
            </div>
            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h3 className="text-sm font-medium text-light-600 dark:text-dark-300 mb-2">
                Number of Investments
              </h3>
              <p className="text-2xl font-bold text-light-900 dark:text-dark-100">
                {investments.length}
              </p>
            </div>
          </motion.div>

          {/* Portfolio Value Chart */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.3 }}
            className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8"
          >
            <div className="lg:col-span-2 bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Portfolio Value Trend
              </h2>
              <div className="h-80">
                <Line
                  data={portfolioValueData}
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
                        beginAtZero: false,
                        title: {
                          display: true,
                          text: 'Value (£)',
                        },
                      },
                    },
                  }}
                />
              </div>
            </div>

            <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6">
              <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
                Asset Allocation
              </h2>
              <div className="h-80">
                <Doughnut
                  data={allocationData}
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

          {/* Investments List */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: 0.4 }}
            className="bg-white dark:bg-dark-800 rounded-2xl shadow-lg p-6"
          >
            <h2 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-6">
              Your Investments
            </h2>
            <div className="space-y-4">
              {investments.map((investment) => (
                <div
                  key={investment.id}
                  className="p-6 bg-light-50 dark:bg-dark-700 rounded-xl"
                >
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <h3 className="text-lg font-medium text-light-900 dark:text-dark-100">
                        {investment.name}
                      </h3>
                      <p className="text-sm text-light-600 dark:text-dark-300">
                        {investment.type}
                      </p>
                    </div>
                    <span className={`text-sm font-medium ${getRiskColor(investment.risk)}`}>
                      {investment.risk.toUpperCase()}
                    </span>
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <p className="text-sm text-light-600 dark:text-dark-300 mb-1">
                        Current Value
                      </p>
                      <p className="text-lg font-bold text-light-900 dark:text-dark-100">
                        {formatCurrency(investment.value)}
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-light-600 dark:text-dark-300 mb-1">
                        Allocation
                      </p>
                      <p className="text-lg font-bold text-light-900 dark:text-dark-100">
                        {investment.allocation}%
                      </p>
                    </div>
                    <div>
                      <p className="text-sm text-light-600 dark:text-dark-300 mb-1">
                        Return
                      </p>
                      <p className={`text-lg font-bold ${
                        investment.return >= 0 ? 'text-green-500' : 'text-red-500'
                      }`}>
                        {investment.return}%
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

export default InvestmentPortfolio; 