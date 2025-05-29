import React from 'react';
import { motion } from 'framer-motion';

const HealthScore = () => {
  const score = 82;
  const circumference = 2 * Math.PI * 70; // radius = 70
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <section className="relative py-24 overflow-hidden">
      {/* Background gradient */}
      <div className="absolute inset-0 bg-gradient-to-b from-light-50/50 to-light-100/50 dark:from-dark-900/50 dark:to-dark-800/50" />
      
      <div className="container-custom relative z-10">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="text-center mb-16"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-light-900 dark:text-dark-100 mb-6">
            Your Financial Health
            <span className="block text-primary-500 mt-2">Score & Insights</span>
          </h2>
          <p className="text-xl text-light-600 dark:text-dark-300 max-w-3xl mx-auto">
            Get a clear understanding of your financial health with our comprehensive scoring system.
            Track your progress and receive personalized recommendations to improve your score.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-16 items-center">
          <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            whileInView={{ opacity: 1, scale: 1 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="relative"
          >
            <div className="absolute inset-0 bg-gradient-to-br from-primary-500/10 to-primary-600/10 rounded-2xl blur-xl" />
            <div className="relative bg-white dark:bg-dark-800 rounded-2xl p-8 shadow-xl">
              <div className="relative w-64 h-64 mx-auto">
                <svg className="w-full h-full transform -rotate-90">
                  {/* Background circle */}
                  <circle
                    cx="128"
                    cy="128"
                    r="70"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="8"
                    className="text-light-200 dark:text-dark-700"
                  />
                  {/* Progress circle */}
                  <circle
                    cx="128"
                    cy="128"
                    r="70"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="8"
                    strokeDasharray={circumference}
                    strokeDashoffset={strokeDashoffset}
                    strokeLinecap="round"
                    className="text-primary-500 transition-all duration-1000 ease-in-out"
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <span className="text-6xl font-bold text-primary-500">{score}</span>
                    <span className="block text-sm text-light-600 dark:text-dark-300 mt-1">Health Score</span>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 20 }}
            whileInView={{ opacity: 1, x: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.8 }}
            className="space-y-8"
          >
            <div className="space-y-6">
              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-primary-500/10 flex items-center justify-center text-primary-500">
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-2">
                    Personalized Scoring
                  </h3>
                  <p className="text-light-600 dark:text-dark-300">
                    Your score is calculated based on your unique financial situation, goals, and habits.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-primary-500/10 flex items-center justify-center text-primary-500">
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-2">
                    Real-Time Updates
                  </h3>
                  <p className="text-light-600 dark:text-dark-300">
                    Your score updates automatically as your financial situation changes.
                  </p>
                </div>
              </div>

              <div className="flex items-start gap-4">
                <div className="flex-shrink-0 w-12 h-12 rounded-xl bg-primary-500/10 flex items-center justify-center text-primary-500">
                  <svg className="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
                  </svg>
                </div>
                <div>
                  <h3 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-2">
                    Actionable Insights
                  </h3>
                  <p className="text-light-600 dark:text-dark-300">
                    Receive personalized recommendations to improve your financial health score.
                  </p>
                </div>
              </div>
            </div>
          </motion.div>
      </div>
    </div>
  </section>
);
};

export default HealthScore; 