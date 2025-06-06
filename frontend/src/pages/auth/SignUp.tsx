import { useState, useCallback } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import Particles from 'react-tsparticles';
import type { Engine } from 'tsparticles-engine';
import { loadSlim } from 'tsparticles-slim';
import MetaTags from '../../components/MetaTags';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import { useAuthContext } from '../../context/AuthContext';

interface FormErrors {
  firstName?: string;
  lastName?: string;
  email?: string;
  password?: string;
  confirmPassword?: string;
  phone?: string;
}

const SignUp = () => {
  const [formData, setFormData] = useState({
    firstName: '',
    lastName: '',
    email: '',
    password: '',
    confirmPassword: '',
    phone: '',
  });

  const [errors, setErrors] = useState<FormErrors>({});
  const { register, isLoading, error: authError } = useAuthContext();

  const particlesInit = useCallback(async (engine: Engine) => {
    await loadSlim(engine);
  }, []);

  const validateForm = (): boolean => {
    const newErrors: FormErrors = {};
    
    // First name validation
    if (!formData.firstName.trim()) {
      newErrors.firstName = 'First name is required';
    }

    // Last name validation
    if (!formData.lastName.trim()) {
      newErrors.lastName = 'Last name is required';
    }

    // Email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!formData.email.trim()) {
      newErrors.email = 'Email is required';
    } else if (!emailRegex.test(formData.email)) {
      newErrors.email = 'Please enter a valid email address';
    }

    // Password validation
    const passwordRegex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$/;
    if (!formData.password) {
      newErrors.password = 'Password is required';
    } else if (!passwordRegex.test(formData.password)) {
      newErrors.password = 'Password must be at least 8 characters long and include uppercase, lowercase, number and special character';
    }

    // Confirm password validation
    if (!formData.confirmPassword) {
      newErrors.confirmPassword = 'Please confirm your password';
    } else if (formData.password !== formData.confirmPassword) {
      newErrors.confirmPassword = 'Passwords do not match';
    }

    // Phone validation
    const phoneRegex = /^\+?[\d\s-]{10,}$/;
    if (!formData.phone.trim()) {
      newErrors.phone = 'Phone number is required';
    } else if (!phoneRegex.test(formData.phone)) {
      newErrors.phone = 'Please enter a valid phone number';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
    // Clear error when user starts typing
    if (errors[name as keyof FormErrors]) {
      setErrors(prev => ({
        ...prev,
        [name]: undefined
      }));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (validateForm()) {
      await register({
        email: formData.email,
        password: formData.password,
        firstName: formData.firstName,
        lastName: formData.lastName,
        phone: formData.phone,
      });
    }
  };

  const renderError = (error?: string) => {
    if (!error) return null;
    return (
      <p className="mt-1 text-sm text-red-600 dark:text-red-400">
        {error}
      </p>
    );
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
              id="tsparticles-signup"
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

          {/* Sign Up Form */}
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
                    Create your account
                  </h2>
                  <p className="mt-2 text-center text-sm text-light-600 dark:text-dark-300">
                    Already have an account?{' '}
                    <Link to="/sign-in" className="font-medium text-primary-500 hover:text-primary-600">
                      Sign in
                    </Link>
                  </p>
                </div>

                {authError && (
                  <div className="bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 p-4 rounded-lg text-sm">
                    {authError}
                  </div>
                )}

                <form className="space-y-6" onSubmit={handleSubmit}>
                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label htmlFor="firstName" className="block text-sm font-medium text-light-700 dark:text-dark-300 mb-1">
                        First name
                      </label>
                      <input
                        id="firstName"
                        name="firstName"
                        type="text"
                        required
                        className={`appearance-none relative block w-full px-3 py-2 border ${
                          errors.firstName ? 'border-red-500' : 'border-light-300 dark:border-dark-600'
                        } placeholder-light-500 dark:placeholder-dark-400 text-light-900 dark:text-dark-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-dark-700`}
                        placeholder="First name"
                        value={formData.firstName}
                        onChange={handleChange}
                      />
                      {renderError(errors.firstName)}
                    </div>
                    <div>
                      <label htmlFor="lastName" className="block text-sm font-medium text-light-700 dark:text-dark-300 mb-1">
                        Last name
                      </label>
                      <input
                        id="lastName"
                        name="lastName"
                        type="text"
                        required
                        className={`appearance-none relative block w-full px-3 py-2 border ${
                          errors.lastName ? 'border-red-500' : 'border-light-300 dark:border-dark-600'
                        } placeholder-light-500 dark:placeholder-dark-400 text-light-900 dark:text-dark-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-dark-700`}
                        placeholder="Last name"
                        value={formData.lastName}
                        onChange={handleChange}
                      />
                      {renderError(errors.lastName)}
                    </div>
                  </div>

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
                      className={`appearance-none relative block w-full px-3 py-2 border ${
                        errors.email ? 'border-red-500' : 'border-light-300 dark:border-dark-600'
                      } placeholder-light-500 dark:placeholder-dark-400 text-light-900 dark:text-dark-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-dark-700`}
                      placeholder="Email address"
                      value={formData.email}
                      onChange={handleChange}
                    />
                    {renderError(errors.email)}
                  </div>

                  <div>
                    <label htmlFor="phone" className="block text-sm font-medium text-light-700 dark:text-dark-300 mb-1">
                      Phone number
                    </label>
                    <input
                      id="phone"
                      name="phone"
                      type="tel"
                      required
                      className={`appearance-none relative block w-full px-3 py-2 border ${
                        errors.phone ? 'border-red-500' : 'border-light-300 dark:border-dark-600'
                      } placeholder-light-500 dark:placeholder-dark-400 text-light-900 dark:text-dark-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-dark-700`}
                      placeholder="Phone number"
                      value={formData.phone}
                      onChange={handleChange}
                    />
                    {renderError(errors.phone)}
                  </div>

                  <div>
                    <label htmlFor="password" className="block text-sm font-medium text-light-700 dark:text-dark-300 mb-1">
                      Password
                    </label>
                    <input
                      id="password"
                      name="password"
                      type="password"
                      autoComplete="new-password"
                      required
                      className={`appearance-none relative block w-full px-3 py-2 border ${
                        errors.password ? 'border-red-500' : 'border-light-300 dark:border-dark-600'
                      } placeholder-light-500 dark:placeholder-dark-400 text-light-900 dark:text-dark-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-dark-700`}
                      placeholder="Password"
                      value={formData.password}
                      onChange={handleChange}
                    />
                    {renderError(errors.password)}
                  </div>

                  <div>
                    <label htmlFor="confirmPassword" className="block text-sm font-medium text-light-700 dark:text-dark-300 mb-1">
                      Confirm password
                    </label>
                    <input
                      id="confirmPassword"
                      name="confirmPassword"
                      type="password"
                      autoComplete="new-password"
                      required
                      className={`appearance-none relative block w-full px-3 py-2 border ${
                        errors.confirmPassword ? 'border-red-500' : 'border-light-300 dark:border-dark-600'
                      } placeholder-light-500 dark:placeholder-dark-400 text-light-900 dark:text-dark-100 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-dark-700`}
                      placeholder="Confirm password"
                      value={formData.confirmPassword}
                      onChange={handleChange}
                    />
                    {renderError(errors.confirmPassword)}
                  </div>

                  <div>
                    <button
                      type="submit"
                      disabled={isLoading}
                      className="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-lg text-white bg-primary-500 hover:bg-primary-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
                    >
                      {isLoading ? 'Creating account...' : 'Create account'}
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

export default SignUp; 