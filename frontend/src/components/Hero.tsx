import { motion } from 'framer-motion';
import { useCallback } from 'react';
import { Link } from 'react-router-dom';
import Particles from 'react-tsparticles';
import type { Engine } from 'tsparticles-engine';
import { loadSlim } from 'tsparticles-slim';
import { useNotification } from '../context/NotificationContext';

const Hero = () => {
  const { showNotification } = useNotification();

  const particlesInit = useCallback(async (engine: Engine) => {
    await loadSlim(engine);
  }, []);

  const handleLearnMoreClick = () => {
    showNotification('Learn more about our features coming soon!');
  };

  return (
    <div className="relative bg-gradient-to-br from-light-50/50 to-light-100/50 dark:from-dark-900/50 dark:to-dark-800/50 overflow-hidden">
      <div className="container-custom py-16 md:py-24">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12 items-center">
          <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.8 }}
            className="md:col-span-2 relative"
          >
            <div className="absolute inset-0 -z-10">
              <Particles
                id="tsparticles-hero"
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
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold text-light-900 dark:text-dark-100 leading-tight">
              Welcome to <span className="text-primary-500">MyMoneyMedic</span>
            </h1>
            <p className="mt-6 text-lg text-light-600 dark:text-dark-300">
              MyMoneyMedic is your integrated financial health check platform. Start with <span className="font-semibold text-primary-500">PulseCheck</span> — a quick, interactive quiz to discover your financial goals and current status. <br className="hidden md:block" />
              Receive AI-powered suggestions, personalized tips, and a detailed health score. Connect your accounts securely with Open Banking for in-depth analysis, and get a tailored action plan to improve your financial well-being.
            </p>
            <div className="mt-8 flex flex-col sm:flex-row gap-4">
              <Link to="/sign-up" className="btn-primary">
                Get Your FREE Pulse Check Now
              </Link>
              <button
                onClick={handleLearnMoreClick}
                className="btn-secondary"
              >
                Learn How It Works
              </button>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.2 }}
            className="relative h-[400px] md:h-[500px] rounded-lg overflow-hidden"
          />
        </div>
      </div>

      {/* Decorative elements with animation and fade edges */}
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
    </div>
  );
};

export default Hero; 