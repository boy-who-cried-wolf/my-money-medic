import { useState, useCallback } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { motion } from 'framer-motion';
import Particles from 'react-tsparticles';
import type { Engine } from 'tsparticles-engine';
import { loadSlim } from 'tsparticles-slim';
import MetaTags from '../../components/MetaTags';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import { useAuthContext } from '../../context/AuthContext';

const SignIn = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const { login, isLoading, error } = useAuthContext();
  const navigate = useNavigate();

  const particlesInit = useCallback(async (engine: Engine) => {
    await loadSlim(engine);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate('/onboarding');
    } catch (error) {
      // Error is already handled by the AuthContext
    }
  };

  return (
    <>
      <MetaTags />
      <div className="min-h-screen flex flex-col">
        <Navbar />
        <main className="flex-grow relative bg-gradient-to-br from-light-50/50 to-light-100/50 dark:from-dark-900/50 dark:to-dark-800/50 overflow-hidden">
          {/* Particles Background */}
          <div className="absolute inset-0 -z-10">
            <Particles
              id="tsparticles-signin"
              init={particlesInit}
              options={{
                background: {
                  color: {
                    value: "transparent",
                  },
                },
                fpsLimit: 120,
                interactivity: {
                  events: {
                    onClick: {
                      enable: true,
                      mode: "push",
                    },
                    onHover: {
                      enable: true,
                      mode: "repulse",
                    },
                    resize: true,
                  },
                  modes: {
                    push: {
                      quantity: 4,
                    },
                    repulse: {
                      distance: 100,
                      duration: 0.4,
                    },
                  },
                },
                particles: {
                  color: {
                    value: "#00AFFF",
                  },
                  links: {
                    color: "#00AFFF",
                    distance: 100,
                    enable: true,
                    opacity: 0.3,
                    width: 1,
                  },
                  move: {
                    direction: "none",
                    enable: true,
                    outModes: {
                      default: "bounce",
                    },
                    random: false,
                    speed: 1,
                    straight: false,
                  },
                  number: {
                    density: {
                      enable: true,
                      area: 400,
                    },
                    value: 40,
                  },
                  opacity: {
                    value: 0.3,
                  },
                  shape: {
                    type: "circle",
                  },
                  size: {
                    value: { min: 1, max: 3 },
                  },
                },
                detectRetina: true,
              }}
              className="absolute inset-0"
            />
          </div>

          {/* Decorative elements */}
          <motion.div
            className="absolute top-0 right-0 w-64 h-64 bg-primary-500 rounded-full opacity-5 blur-xl -translate-y-1/2 translate-x-1/2"
            animate={{
              scale: [1, 1.1, 1],
              opacity: [0.05, 0.1, 0.05],
            }}
            transition={{
              duration: 5,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />
          <motion.div
            className="absolute bottom-0 left-0 w-48 h-48 bg-light-200 dark:bg-dark-700 rounded-full opacity-30 blur-xl translate-y-1/2 -translate-x-1/2"
            animate={{
              scale: [1, 1.1, 1],
              opacity: [0.3, 0.4, 0.3],
            }}
            transition={{
              duration: 4,
              repeat: Infinity,
              ease: "easeInOut",
            }}
          />

          {/* Sign In Form */}
          <div className="container-custom py-12 px-4 sm:px-6 lg:px-8 mt-16">
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8 }}
              className="max-w-md mx-auto"
            >
              <div className="bg-white dark:bg-dark-800 rounded-2xl shadow-xl p-8 space-y-8">
                <div>
                  <h2 className="text-3xl font-bold text-center text-light-900 dark:text-dark-100">
                    Sign in to your account
                  </h2>
                  <p className="mt-2 text-center text-sm text-light-600 dark:text-dark-300">
                    Or{' '}
                    <Link to="/sign-up" className="font-medium text-primary-500 hover:text-primary-600">
                      create a new account
                    </Link>
                  </p>
                </div>

                {error && (
                  <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-lg text-sm">
                    {error}
                  </div>
                )}

                <form className="space-y-6" onSubmit={handleSubmit}>
                  <div>
                    <label htmlFor="email-address" className="block text-sm font-medium text-light-700 dark:text-dark-300 mb-1">
                      Email address
                    </label>
                    <input
                      id="email-address"
                      name="email"
                      type="email"
                      autoComplete="email"
                      required
                      className="appearance-none relative block w-full px-3 py-2 border border-light-300 dark:border-dark-600 placeholder-light-500 dark:placeholder-dark-400 text-light-900 dark:text-dark-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-dark-700"
                      placeholder="Email address"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                    />
                  </div>

                  <div>
                    <label htmlFor="password" className="block text-sm font-medium text-light-700 dark:text-dark-300 mb-1">
                      Password
                    </label>
                    <input
                      id="password"
                      name="password"
                      type="password"
                      autoComplete="current-password"
                      required
                      className="appearance-none relative block w-full px-3 py-2 border border-light-300 dark:border-dark-600 placeholder-light-500 dark:placeholder-dark-400 text-light-900 dark:text-dark-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-dark-700"
                      placeholder="Password"
                      value={password}
                      onChange={(e) => setPassword(e.target.value)}
                    />
                  </div>

                  <div className="flex items-center justify-between">
                    <div className="flex items-center">
                      <input
                        id="remember-me"
                        name="remember-me"
                        type="checkbox"
                        className="h-4 w-4 text-primary-500 focus:ring-primary-500 border-light-300 dark:border-dark-600 rounded"
                      />
                      <label htmlFor="remember-me" className="ml-2 block text-sm text-light-700 dark:text-dark-300">
                        Remember me
                      </label>
                    </div>

                    <div className="text-sm">
                      <Link to="/forgot-password" className="font-medium text-primary-500 hover:text-primary-600">
                        Forgot your password?
                      </Link>
                    </div>
                  </div>

                  <div>
                    <button
                      type="submit"
                      disabled={isLoading}
                      className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-primary-500 hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isLoading ? 'Signing in...' : 'Sign in'}
                    </button>
                  </div>
                </form>
              </div>
            </motion.div>
          </div>
        </main>
        <Footer />
      </div>
    </>
  );
};

export default SignIn; 