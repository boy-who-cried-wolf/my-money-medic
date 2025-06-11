import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';
import MetaTags from '../../components/MetaTags';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import ProtectedRoute from '../../components/ProtectedRoute';
import { useState } from 'react';

// SVG Icons
const Icons = {
  Savings: (
    <svg className="w-8 h-8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20Z" fill="currentColor"/>
      <path d="M12 6C8.69 6 6 8.69 6 12C6 15.31 8.69 18 12 18C15.31 18 18 15.31 18 12C18 8.69 15.31 6 12 6ZM12 16C9.79 16 8 14.21 8 12C8 9.79 9.79 8 12 8C14.21 8 16 9.79 16 12C16 14.21 14.21 16 12 16Z" fill="currentColor"/>
      <path d="M12 10C10.9 10 10 10.9 10 12C10 13.1 10.9 14 12 14C13.1 14 14 13.1 14 12C14 10.9 13.1 10 12 10Z" fill="currentColor"/>
    </svg>
  ),
  Investment: (
    <svg className="w-8 h-8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M3.5 18.5L9.5 12.5L13.5 16.5L22 6.92L20.59 5.51L13.5 13.5L9.5 9.5L2 17L3.5 18.5Z" fill="currentColor"/>
      <path d="M21 2H3C2.45 2 2 2.45 2 3V21C2 21.55 2.45 22 3 22H21C21.55 22 22 21.55 22 21V3C22 2.45 21.55 2 21 2ZM20 20H4V4H20V20Z" fill="currentColor"/>
    </svg>
  ),
  DebtManagement: (
    <svg className="w-8 h-8" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M11.8 10.9C9.53 10.31 8.8 9.7 8.8 8.75C8.8 7.66 9.81 6.9 11.5 6.9C13.28 6.9 13.94 7.75 14 9H16.21C16.14 7.28 15.09 5.7 13 5.19V3H10V5.16C8.06 5.58 6.5 6.84 6.5 8.77C6.5 10.08 7.23 11.23 8.5 11.84C10.79 12.53 11.2 13.47 11.2 14.1C11.2 14.95 10.39 15.6 8.5 15.6C6.5 15.6 5.79 14.75 5.7 13.6H3.5C3.59 15.5 4.5 16.97 6.5 17.47V19.5H9.5V17.43C11.39 17.03 12.8 15.84 12.8 14.1C12.8 12.5 11.8 10.9 11.8 10.9Z" fill="currentColor"/>
    </svg>
  )
};

// Large Watermark Icons
const WatermarkIcons = {
  Savings: (
    <svg className="w-32 h-32 opacity-10" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M12 2C6.48 2 2 6.48 2 12C2 17.52 6.48 22 12 22C17.52 22 22 17.52 22 12C22 6.48 17.52 2 12 2ZM12 20C7.59 20 4 16.41 4 12C4 7.59 7.59 4 12 4C16.41 4 20 7.59 20 12C20 16.41 16.41 20 12 20Z" fill="currentColor"/>
      <path d="M12 6C8.69 6 6 8.69 6 12C6 15.31 8.69 18 12 18C15.31 18 18 15.31 18 12C18 8.69 15.31 6 12 6ZM12 16C9.79 16 8 14.21 8 12C8 9.79 9.79 8 12 8C14.21 8 16 9.79 16 12C16 14.21 14.21 16 12 16Z" fill="currentColor"/>
      <path d="M12 10C10.9 10 10 10.9 10 12C10 13.1 10.9 14 12 14C13.1 14 14 13.1 14 12C14 10.9 13.1 10 12 10Z" fill="currentColor"/>
    </svg>
  ),
  Investment: (
    <svg className="w-32 h-32 opacity-10" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M3.5 18.5L9.5 12.5L13.5 16.5L22 6.92L20.59 5.51L13.5 13.5L9.5 9.5L2 17L3.5 18.5Z" fill="currentColor"/>
      <path d="M21 2H3C2.45 2 2 2.45 2 3V21C2 21.55 2.45 22 3 22H21C21.55 22 22 21.55 22 21V3C22 2.45 21.55 2 21 2ZM20 20H4V4H20V20Z" fill="currentColor"/>
    </svg>
  ),
  DebtManagement: (
    <svg className="w-32 h-32 opacity-10" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
      <path d="M11.8 10.9C9.53 10.31 8.8 9.7 8.8 8.75C8.8 7.66 9.81 6.9 11.5 6.9C13.28 6.9 13.94 7.75 14 9H16.21C16.14 7.28 15.09 5.7 13 5.19V3H10V5.16C8.06 5.58 6.5 6.84 6.5 8.77C6.5 10.08 7.23 11.23 8.5 11.84C10.79 12.53 11.2 13.47 11.2 14.1C11.2 14.95 10.39 15.6 8.5 15.6C6.5 15.6 5.79 14.75 5.7 13.6H3.5C3.59 15.5 4.5 16.97 6.5 17.47V19.5H9.5V17.43C11.39 17.03 12.8 15.84 12.8 14.1C12.8 12.5 11.8 10.9 11.8 10.9Z" fill="currentColor"/>
    </svg>
  )
};

// Mock data for recommended products - replace with real data from API
const recommendedProducts = [
  {
    id: 1,
    name: 'High-Yield Savings Account',
    provider: 'Digital Bank',
    description: 'Earn 4.5% APY on your savings with no minimum balance requirement.',
    features: [
      'No monthly maintenance fees',
      'FDIC insured up to $250,000',
      '24/7 mobile banking access',
      'Free ATM withdrawals'
    ],
    matchScore: 95,
    category: 'Savings',
    monthlyFee: 0,
    interestRate: '4.5%',
    minimumDeposit: 0,
    icon: Icons.Savings,
    watermarkIcon: WatermarkIcons.Savings,
    color: 'text-blue-500'
  },
  {
    id: 2,
    name: 'Investment Portfolio',
    provider: 'Robo Advisor',
    description: 'Automated investment portfolio tailored to your risk tolerance and goals.',
    features: [
      'Diversified portfolio',
      'Automatic rebalancing',
      'Tax-loss harvesting',
      'Low management fees'
    ],
    matchScore: 88,
    category: 'Investment',
    monthlyFee: 0.25,
    interestRate: '7-10% (historical)',
    minimumDeposit: 1000,
    icon: Icons.Investment,
    watermarkIcon: WatermarkIcons.Investment,
    color: 'text-green-500'
  },
  {
    id: 3,
    name: 'Debt Consolidation Loan',
    provider: 'Credit Union',
    description: 'Consolidate high-interest debt into one manageable payment.',
    features: [
      'Fixed interest rate',
      'No prepayment penalties',
      'Flexible terms',
      'Quick approval process'
    ],
    matchScore: 82,
    category: 'Debt Management',
    monthlyFee: 0,
    interestRate: '5.99%',
    minimumDeposit: 5000,
    icon: Icons.DebtManagement,
    watermarkIcon: WatermarkIcons.DebtManagement,
    color: 'text-purple-500'
  }
];

const categoryColors = {
  'Savings': 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200',
  'Investment': 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200',
  'Debt Management': 'bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200'
};

const Recommendations = () => {
  const [selectedProduct, setSelectedProduct] = useState<number | null>(null);

  return (
    <ProtectedRoute>
      <MetaTags />
      <div className="min-h-screen flex flex-col bg-light-50 dark:bg-dark-900">
        <Navbar />
        <main className="flex-grow container-custom py-8 mt-16">
          {/* Header Section */}
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mb-8"
          >
            <h1 className="text-3xl font-bold text-light-900 dark:text-dark-100">
              Your Personalized Recommendations
            </h1>
            <p className="mt-2 text-light-600 dark:text-dark-300">
              Based on your financial profile and goals, we've selected these products for you
            </p>
          </motion.div>

          {/* Filter Section */}
          <div className="mb-8 flex flex-wrap gap-4">
            <button className="px-4 py-2 rounded-full bg-primary-500 text-white hover:bg-primary-600 transition-colors">
              All Products
            </button>
            <button className="px-4 py-2 rounded-full bg-light-100 dark:bg-dark-800 text-light-900 dark:text-dark-100 hover:bg-light-200 dark:hover:bg-dark-700 transition-colors">
              Savings
            </button>
            <button className="px-4 py-2 rounded-full bg-light-100 dark:bg-dark-800 text-light-900 dark:text-dark-100 hover:bg-light-200 dark:hover:bg-dark-700 transition-colors">
              Investments
            </button>
            <button className="px-4 py-2 rounded-full bg-light-100 dark:bg-dark-800 text-light-900 dark:text-dark-100 hover:bg-light-200 dark:hover:bg-dark-700 transition-colors">
              Debt Management
            </button>
          </div>

          {/* Recommendations Grid */}
          <div className="grid grid-cols-1 gap-8">
            {recommendedProducts.map((product, index) => (
              <motion.div
                key={product.id}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5, delay: index * 0.1 }}
                className="bg-white dark:bg-dark-800 rounded-3xl shadow-lg overflow-hidden hover:shadow-xl transition-shadow relative"
              >
                {/* Watermark Icon */}
                <div className={`absolute bottom-4 right-4 ${product.color}`}>
                  {product.watermarkIcon}
                </div>

                {/* Main Content */}
                <div className="p-6">
                  <div className="flex flex-col md:flex-row justify-between gap-6">
                    {/* Product Info */}
                    <div className="flex-grow">
                      <div className="flex items-center justify-between mb-4">
                        <div>
                          <h2 className="text-2xl font-semibold text-light-900 dark:text-dark-100">
                            {product.name}
                          </h2>
                          <p className="text-sm text-light-600 dark:text-dark-300">
                            {product.provider}
                          </p>
                        </div>
                        <div className="flex items-center">
                          <span className="text-sm font-medium text-primary-500 bg-primary-500/10 px-4 py-2 rounded-full">
                            {product.matchScore}% Match
                          </span>
                        </div>
                      </div>
                      <p className="text-light-600 dark:text-dark-300 mb-6 text-lg">
                        {product.description}
                      </p>
                      <div className="grid grid-cols-2 md:grid-cols-4 gap-6 mb-6">
                        <div className="bg-light-50 dark:bg-dark-700 p-4 rounded-xl">
                          <p className="text-sm text-light-600 dark:text-dark-300 mb-1">Category</p>
                          <p className="font-medium text-light-900 dark:text-dark-100">{product.category}</p>
                        </div>
                        <div className="bg-light-50 dark:bg-dark-700 p-4 rounded-xl">
                          <p className="text-sm text-light-600 dark:text-dark-300 mb-1">Monthly Fee</p>
                          <p className="font-medium text-light-900 dark:text-dark-100">
                            {product.monthlyFee === 0 ? 'Free' : `$${product.monthlyFee}`}
                          </p>
                        </div>
                        <div className="bg-light-50 dark:bg-dark-700 p-4 rounded-xl">
                          <p className="text-sm text-light-600 dark:text-dark-300 mb-1">Interest Rate</p>
                          <p className="font-medium text-light-900 dark:text-dark-100">{product.interestRate}</p>
                        </div>
                        <div className="bg-light-50 dark:bg-dark-700 p-4 rounded-xl">
                          <p className="text-sm text-light-600 dark:text-dark-300 mb-1">Minimum Deposit</p>
                          <p className="font-medium text-light-900 dark:text-dark-100">
                            {product.minimumDeposit === 0 ? 'None' : `$${product.minimumDeposit}`}
                          </p>
                        </div>
                      </div>
                      <div className="mb-6">
                        <h3 className="text-sm font-medium text-light-900 dark:text-dark-100 mb-4">
                          Key Features
                        </h3>
                        <ul className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {product.features.map((feature, idx) => (
                            <li key={idx} className="flex items-center text-light-600 dark:text-dark-300 bg-light-50 dark:bg-dark-700 p-3 rounded-lg">
                              <svg
                                className="w-5 h-5 mr-3 text-primary-500"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                              >
                                <path
                                  strokeLinecap="round"
                                  strokeLinejoin="round"
                                  strokeWidth={2}
                                  d="M5 13l4 4L19 7"
                                />
                              </svg>
                              {feature}
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>

                    {/* Action Buttons */}
                    <div className="flex flex-col gap-3 md:w-48">
                      <button 
                        className="w-full bg-primary-500 text-white px-6 py-3 rounded-xl hover:bg-primary-600 transition-colors font-medium"
                        onClick={() => setSelectedProduct(product.id)}
                      >
                        Learn More
                      </button>
                      <button className="w-full border-2 border-primary-500 text-primary-500 px-6 py-3 rounded-xl hover:bg-primary-50 dark:hover:bg-primary-500/10 transition-colors font-medium">
                        Compare
                      </button>
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </main>
        <Footer />
      </div>
    </ProtectedRoute>
  );
};

export default Recommendations; 