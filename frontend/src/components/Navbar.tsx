import { motion } from 'framer-motion';
import { useState, useEffect, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import logo from '../assets/images/logo.png';
import { useNotification } from '../context/NotificationContext';
import { useAuthContext } from '../context/AuthContext';
import ProfileSettingsModal from './ProfileSettingsModal';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const [isProfileSettingsOpen, setIsProfileSettingsOpen] = useState(false);
  const { showNotification } = useNotification();
  const { isAuthenticated, logout } = useAuthContext();
  const navigate = useNavigate();
  const location = useLocation();
  const currentPath = location.pathname.split('/')[1] || 'dashboard';
  const profileMenuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target as Node)) {
        setIsProfileOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Navigation links for non-authenticated users (landing page sections)
  const landingNavigation = [
    { name: 'How it Works', href: '#how-it-works' },
    { name: 'Benefits', href: '#benefits' },
    { name: 'Features', href: '#features' },
    { name: 'Health Score', href: '#health-score' },
    { name: 'Open Banking', href: '#open-banking' },
    { name: 'Testimonials', href: '#testimonials' },
    { name: 'FAQ', href: '#faq' },
  ];

  // Navigation links for authenticated users
  const dashboardNavigation = [
    { name: 'Overview', path: '/dashboard' },
    { name: 'Insights', path: '/insights' },
    { name: 'Spending', path: '/spending' },
    { name: 'Savings', path: '/savings' },
    { name: 'Investments', path: '/investments' },
    { name: 'Budget', path: '/budget' },
    { name: 'Recommendations', path: '/recommendations' },
  ];

  const handleLandingLinkClick = (href: string) => {
    // If we're not on the landing page, navigate to it first
    if (location.pathname !== '/') {
      navigate('/');
      // Store the hash to scroll to after navigation
      setTimeout(() => {
        const element = document.querySelector(href);
        if (element) {
          element.scrollIntoView({ behavior: 'smooth' });
        }
      }, 100);
    } else {
      // If we're already on the landing page, just scroll
      const element = document.querySelector(href);
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
    setIsOpen(false);
  };

  return (
    <nav className="fixed w-full bg-dark-800/20 backdrop-blur-md z-50">
      <div className="container-custom py-4">
        <div className="flex items-center justify-between">
          <button
            className="flex items-center"
            onClick={() => navigate('/')}
          >
            <img
              className="h-8 w-auto"
              src={logo}
              alt="MyMoneyMedic"
            />
          </button>
          
          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              // Dashboard Navigation
              <>
                {dashboardNavigation.map((item) => (
                  <button
                    key={item.name}
                    onClick={() => navigate(item.path)}
                    className={`relative px-3 py-2 text-sm font-medium transition-colors ${
                      currentPath === item.path.split('/')[1]
                        ? 'text-primary-500'
                        : 'text-dark-200 hover:text-white'
                    }`}
                  >
                    {item.name}
                    {currentPath === item.path.split('/')[1] && (
                      <motion.div
                        layoutId="activeTab"
                        className="absolute bottom-0 left-0 right-0 h-0.5 bg-primary-500"
                        initial={false}
                        transition={{ type: "spring", stiffness: 500, damping: 30 }}
                      />
                    )}
                  </button>
                ))}
              </>
            ) : (
              // Landing Page Navigation
              <>
                {landingNavigation.map((item) => (
                  <button
                    key={item.name}
                    onClick={() => handleLandingLinkClick(item.href)}
                    className="px-3 py-2 text-sm text-dark-200 hover:text-white transition-colors"
                  >
                    {item.name}
                  </button>
                ))}
              </>
            )}
            
            {/* Profile Menu */}
            {isAuthenticated && (
              <div className="relative" ref={profileMenuRef}>
                <button
                  onClick={() => setIsProfileOpen(!isProfileOpen)}
                  className="flex items-center space-x-2 text-dark-200 hover:text-white"
                >
                  <svg
                    className="w-6 h-6"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth={2}
                      d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                    />
                  </svg>
                </button>
                
                {/* Profile Dropdown */}
                {isProfileOpen && (
                  <motion.div
                    initial={{ opacity: 0, y: -10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="absolute right-0 mt-2 w-48 bg-dark-800 rounded-md shadow-lg py-1"
                  >
                    <button
                      onClick={() => {
                        setIsProfileSettingsOpen(true);
                        setIsProfileOpen(false);
                      }}
                      className="block w-full text-left px-4 py-2 text-sm text-dark-200 hover:bg-dark-700"
                    >
                      Profile Settings
                    </button>
                    <button
                      onClick={() => {
                        logout();
                        setIsProfileOpen(false);
                      }}
                      className="block w-full text-left px-4 py-2 text-sm text-dark-200 hover:bg-dark-700"
                    >
                      Logout
                    </button>
                  </motion.div>
                )}
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <button
            className="md:hidden text-dark-200"
            onClick={() => setIsOpen(!isOpen)}
          >
            <svg
              className="w-6 h-6"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              {isOpen ? (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M6 18L18 6M6 6l12 12"
                />
              ) : (
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M4 6h16M4 12h16M4 18h16"
                />
              )}
            </svg>
          </button>
        </div>

        {/* Mobile Navigation */}
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="md:hidden mt-4 space-y-4"
          >
            {isAuthenticated ? (
              // Mobile Dashboard Navigation
              <>
                {dashboardNavigation.map((item) => (
                  <button
                    key={item.name}
                    onClick={() => {
                      navigate(item.path);
                      setIsOpen(false);
                    }}
                    className={`block w-full text-left px-4 py-2 rounded-md ${
                      currentPath === item.path.split('/')[1]
                        ? 'text-primary-500 bg-dark-700'
                        : 'text-dark-200 hover:bg-dark-700'
                    }`}
                  >
                    {item.name}
                  </button>
                ))}
                <button
                  onClick={() => {
                    logout();
                    setIsOpen(false);
                  }}
                  className="block w-full text-left px-4 py-2 text-dark-200 hover:bg-dark-700 rounded-md"
                >
                  Logout
                </button>
              </>
            ) : (
              // Mobile Landing Page Navigation
              <>
                {landingNavigation.map((item) => (
                  <button
                    key={item.name}
                    onClick={() => {
                      handleLandingLinkClick(item.href);
                      setIsOpen(false);
                    }}
                    className="block w-full text-left px-4 py-2 text-dark-200 hover:bg-dark-700 rounded-md"
                  >
                    {item.name}
                  </button>
                ))}
              </>
            )}
          </motion.div>
        )}
      </div>
      <ProfileSettingsModal
        isOpen={isProfileSettingsOpen}
        onClose={() => setIsProfileSettingsOpen(false)}
      />
    </nav>
  );
};

export default Navbar; 