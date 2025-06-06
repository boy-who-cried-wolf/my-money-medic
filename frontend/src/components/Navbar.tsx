import { motion } from 'framer-motion';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import logo from '../assets/images/logo.png';
import { useNotification } from '../context/NotificationContext';
import { useAuthContext } from '../context/AuthContext';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [isProfileOpen, setIsProfileOpen] = useState(false);
  const { showNotification } = useNotification();
  const { isAuthenticated, logout } = useAuthContext();
  const navigate = useNavigate();

  const navigation = [
    { name: 'PulseCheck', href: '/pulsecheck' },
    { name: 'How it Works', href: '/how-it-works' },
    { name: 'News & Media', href: '/news' },
    { name: 'Partners Area', href: '/partners' },
    { name: 'MyMoneyMedic', href: '/mymoneymedic' },
  ];

  const handleLinkClick = (name: string) => {
    showNotification(`The ${name} feature is coming soon! Stay tuned for updates.`);
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
          <div className="hidden md:flex items-center space-x-8">
            {navigation.map((item) => (
              <button
                key={item.name}
                onClick={() => handleLinkClick(item.name)}
                className="nav-link"
              >
                {item.name}
              </button>
            ))}
            
            {/* Profile Menu */}
            {isAuthenticated && (
              <div className="relative">
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
                        handleLinkClick('Profile Settings');
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
            {navigation.map((item) => (
              <button
                key={item.name}
                onClick={() => {
                  handleLinkClick(item.name);
                  setIsOpen(false);
                }}
                className="block text-dark-200 hover:bg-dark-700 px-4 py-2 rounded-md w-full text-left"
              >
                {item.name}
              </button>
            ))}
            
            {/* Mobile Profile Menu */}
            {isAuthenticated && (
              <>
                <button
                  onClick={() => {
                    handleLinkClick('Profile Settings');
                    setIsOpen(false);
                  }}
                  className="block text-dark-200 hover:bg-dark-700 px-4 py-2 rounded-md w-full text-left"
                >
                  Profile Settings
                </button>
                <button
                  onClick={() => {
                    logout();
                    setIsOpen(false);
                  }}
                  className="block text-dark-200 hover:bg-dark-700 px-4 py-2 rounded-md w-full text-left"
                >
                  Logout
                </button>
              </>
            )}
          </motion.div>
        )}
      </div>
    </nav>
  );
};

export default Navbar; 