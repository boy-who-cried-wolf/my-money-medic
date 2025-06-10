import { useLocation, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';

const FinancialNav = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const currentPath = location.pathname.split('/')[1] || 'dashboard';

  const tabs = [
    { id: 'dashboard', label: 'Overview', path: '/dashboard' },
    { id: 'insights', label: 'Insights', path: '/insights' },
    { id: 'spending', label: 'Spending', path: '/spending' },
    { id: 'savings', label: 'Savings', path: '/savings' },
    { id: 'investments', label: 'Investments', path: '/investments' },
    { id: 'budget', label: 'Budget', path: '/budget' },
  ];

  return (
    <div className="border-b border-light-200 dark:border-dark-700 mb-8">
      <nav className="flex space-x-1">
        {tabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => navigate(tab.path)}
            className={`relative px-4 py-3 text-sm font-medium transition-colors ${
              currentPath === tab.id
                ? 'text-primary-500'
                : 'text-light-600 dark:text-dark-300 hover:text-light-900 dark:hover:text-dark-100'
            }`}
          >
            {tab.label}
            {currentPath === tab.id && (
              <motion.div
                layoutId="activeTab"
                className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-500"
                initial={false}
                transition={{ type: "spring", stiffness: 500, damping: 30 }}
              />
            )}
          </button>
        ))}
      </nav>
    </div>
  );
};

export default FinancialNav; 