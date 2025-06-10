import { useEffect, useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import MetaTags from '../../components/MetaTags';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import { motion } from 'framer-motion';

// Yodlee FastLink configuration
const YODLEE_CONFIG = {
  fastLinkURL: process.env.REACT_APP_YODLEE_FASTLINK_URL || 'https://fl4.sandbox.yodlee.com.au/authenticate/anzdevexsandbox/fastlink/',
  clientId: process.env.REACT_APP_YODLEE_CLIENT_ID || '3vb7NjZIL8ATwADYxK914RSnW9QCtQeFcrurD6tHEnOeX87J',
  clientSecret: process.env.REACT_APP_YODLEE_CLIENT_SECRET || 'lhwvb3zCL3Tk2kMyIy4EL8MGjVehCSKyDzSlqteGRM9qRYpweHCx6bZgjOA20Xod',
  environment: process.env.REACT_APP_YODLEE_ENVIRONMENT || 'sandbox',
};

const YodleeConnect = () => {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(true);
  const [showFastLink, setShowFastLink] = useState(false);
  const [fastLinkToken, setFastLinkToken] = useState('');
  const [error, setError] = useState<string | null>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);

  useEffect(() => {
    // Log configuration for debugging
    console.log('Yodlee Configuration:', {
      fastLinkURL: YODLEE_CONFIG.fastLinkURL,
      environment: YODLEE_CONFIG.environment,
      hasClientId: !!YODLEE_CONFIG.clientId,
      hasClientSecret: !!YODLEE_CONFIG.clientSecret,
    });

    const initializeFastLink = async () => {
      try {
        // For testing, we'll use a mock token
        // In production, this should be replaced with an actual API call
        const mockToken = 'mock-token-' + Date.now();
        console.log('Using mock token:', mockToken);
        setFastLinkToken(mockToken);
        setIsLoading(false);
      } catch (error) {
        console.error('Error initializing FastLink:', error);
        setError('Failed to initialize FastLink. Please try again later.');
        setIsLoading(false);
      }
    };

    initializeFastLink();
  }, []);

  const handleFastLinkMessage = (event: MessageEvent) => {
    // Ignore MetaMask messages
    if (event.data?.target === 'metamask-inpage') {
      return;
    }

    // Log Yodlee messages for debugging
    if (event.origin === YODLEE_CONFIG.fastLinkURL) {
      console.log('Received Yodlee message:', event.data);
    }

    // Handle messages from FastLink iframe
    if (event.origin === YODLEE_CONFIG.fastLinkURL) {
      try {
        const { type, data } = event.data;
        
        switch (type) {
          case 'FASTLINK_ACCOUNTS_ADDED':
            // Handle successful account addition
            console.log('Accounts added:', data);
            navigate('/dashboard');
            break;
          case 'FASTLINK_ERROR':
            // Handle error
            console.error('FastLink error:', data);
            setError(data.message || 'An error occurred while connecting your bank account.');
            setShowFastLink(false);
            break;
          case 'FASTLINK_CLOSE':
            // Handle FastLink close
            console.log('FastLink closed by user');
            setShowFastLink(false);
            break;
          default:
            // Only log if it's a Yodlee message
            if (event.origin === YODLEE_CONFIG.fastLinkURL) {
              console.log('Unhandled Yodlee message type:', type);
            }
        }
      } catch (error) {
        console.error('Error processing FastLink message:', error);
      }
    }
  };

  useEffect(() => {
    if (showFastLink) {
      window.addEventListener('message', handleFastLinkMessage);
      return () => window.removeEventListener('message', handleFastLinkMessage);
    }
  }, [showFastLink]);

  const handleStartFastLink = () => {
    setError(null);
    setShowFastLink(true);
  };

  const handleRetry = () => {
    setError(null);
    setIsLoading(true);
    // Re-initialize FastLink
    const mockToken = 'mock-token-' + Date.now();
    setFastLinkToken(mockToken);
    setIsLoading(false);
  };

  // Construct FastLink URL with all necessary parameters
  const getFastLinkUrl = () => {
    const params = new URLSearchParams({
      token: fastLinkToken,
      clientId: YODLEE_CONFIG.clientId,
      environment: YODLEE_CONFIG.environment,
    });
    return `${YODLEE_CONFIG.fastLinkURL}?${params.toString()}`;
  };

  return (
    <div className="min-h-screen flex flex-col bg-gradient-to-br from-light-50/50 to-light-100/50 dark:from-dark-900/50 dark:to-dark-800/50">
      <MetaTags />
      <Navbar />
      <main className="flex-grow container-custom py-12 mt-16">
        <div className="max-w-3xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="bg-white dark:bg-dark-800 rounded-2xl shadow-xl p-8 relative overflow-hidden"
          >
            {/* Decorative Elements */}
            <div className="absolute top-0 right-0 w-32 h-32 bg-primary-500/5 rounded-full blur-2xl -translate-y-1/2 translate-x-1/2" />
            <div className="absolute bottom-0 left-0 w-32 h-32 bg-primary-500/5 rounded-full blur-2xl translate-y-1/2 -translate-x-1/2" />

            <div className="relative">
              <h1 className="text-3xl font-bold text-light-900 dark:text-dark-100 mb-6">
                Connect Your Bank Account
              </h1>

              {error ? (
                <div className="space-y-6">
                  <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-xl p-6">
                    <div className="flex items-center">
                      <svg className="w-6 h-6 text-red-500 mr-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                      </svg>
                      <h3 className="text-lg font-medium text-red-800 dark:text-red-200">Error</h3>
                    </div>
                    <p className="mt-2 text-red-700 dark:text-red-300">{error}</p>
                  </div>
                  <div className="flex justify-center">
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={handleRetry}
                      className="px-6 py-3 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-xl hover:from-primary-600 hover:to-primary-700 transition-all duration-200 shadow-sm hover:shadow-md"
                    >
                      Try Again
                    </motion.button>
                  </div>
                </div>
              ) : isLoading ? (
                <div className="flex flex-col items-center justify-center py-12">
                  <div className="w-16 h-16 border-4 border-primary-500 border-t-transparent rounded-full animate-spin mb-4" />
                  <p className="text-light-600 dark:text-dark-300">
                    Preparing secure connection...
                  </p>
                </div>
              ) : showFastLink ? (
                <div className="w-full h-[600px] rounded-xl overflow-hidden border border-light-300 dark:border-dark-600">
                  <iframe
                    ref={iframeRef}
                    src={getFastLinkUrl()}
                    className="w-full h-full"
                    title="Yodlee FastLink"
                    allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture"
                  />
                </div>
              ) : (
                <div className="space-y-6">
                  <p className="text-light-600 dark:text-dark-300">
                    We're about to connect you to Yodlee's secure banking platform. This will allow us to:
                  </p>
                  <ul className="space-y-3">
                    <li className="flex items-start">
                      <svg className="w-6 h-6 text-primary-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="text-light-700 dark:text-dark-200">Securely access your bank accounts</span>
                    </li>
                    <li className="flex items-start">
                      <svg className="w-6 h-6 text-primary-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="text-light-700 dark:text-dark-200">Analyze your spending patterns</span>
                    </li>
                    <li className="flex items-start">
                      <svg className="w-6 h-6 text-primary-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                      </svg>
                      <span className="text-light-700 dark:text-dark-200">Provide personalized financial insights</span>
                    </li>
                  </ul>

                  <div className="flex flex-col sm:flex-row gap-4 mt-8">
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={handleStartFastLink}
                      className="flex-1 px-6 py-3 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-xl hover:from-primary-600 hover:to-primary-700 transition-all duration-200 shadow-sm hover:shadow-md"
                    >
                      Continue to Bank Selection
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={() => navigate('/dashboard')}
                      className="flex-1 px-6 py-3 border border-light-300 dark:border-dark-600 rounded-xl text-light-700 dark:text-dark-300 hover:bg-light-50 dark:hover:bg-dark-700 transition-all duration-200"
                    >
                      Skip for Now
                    </motion.button>
                  </div>
                </div>
              )}
            </div>
          </motion.div>
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default YodleeConnect; 