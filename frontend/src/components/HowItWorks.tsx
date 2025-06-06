import React from 'react';
import { motion } from 'framer-motion';
import { Link } from 'react-router-dom';

const steps = [
  {
    number: '01',
    title: 'Take the PulseCheck',
    description: 'Start with a quick, interactive quiz to discover your financial goals and current status.',
    icon: (
      <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
      </svg>
    ),
  },
  {
    number: '02',
    title: 'AI-Powered Analysis',
    description: 'Our AI analyzes your answers and, with your permission, your financial data via Open Banking.',
    icon: (
      <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
      </svg>
    ),
  },
  {
    number: '03',
    title: 'Get Your Action Plan',
    description: 'Receive a personalized health score, insights, and a step-by-step action plan to improve your financial well-being.',
    icon: (
      <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
      </svg>
    ),
  },
];

const HowItWorks = () => {
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
            How MyMoneyMedic
            <span className="block text-primary-500 mt-2">Works for You</span>
          </h2>
          <p className="text-xl text-light-600 dark:text-dark-300 max-w-3xl mx-auto">
            Your journey to better financial health starts here. Follow these simple steps to get personalized insights
            and a clear path to financial success.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {steps.map((step, index) => (
            <motion.div
              key={step.number}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: index * 0.2 }}
              className="group relative"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-primary-500/10 to-primary-600/10 rounded-2xl blur-xl group-hover:opacity-100 opacity-0 transition-opacity duration-500" />
              <div className="relative bg-white dark:bg-dark-800 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-500 hover:-translate-y-1">
                <div className="flex flex-col items-center text-center">
                  <div className="relative mb-6">
                    <div className="absolute inset-0 bg-primary-500/10 rounded-full blur-lg" />
                    <div className="relative w-16 h-16 rounded-full bg-primary-500/10 flex items-center justify-center text-primary-500 group-hover:bg-primary-500 group-hover:text-white transition-all duration-500">
                      {step.icon}
                    </div>
                  </div>
                  <span className="text-4xl font-bold text-primary-500/20 mb-4">{step.number}</span>
                  <h3 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-4 group-hover:text-primary-500 transition-colors duration-300">
                    {step.title}
                  </h3>
                  <p className="text-light-600 dark:text-dark-300">
                    {step.description}
                  </p>
                </div>
              </div>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="mt-16 text-center"
        >
          <Link to="/sign-up" className="btn-primary group relative overflow-hidden inline-block">
            <span className="relative z-10">Start Your Journey</span>
            <motion.div
              className="absolute inset-0 bg-primary-600"
              initial={{ x: '-100%' }}
              whileHover={{ x: 0 }}
              transition={{ duration: 0.3 }}
            />
          </Link>
        </motion.div>
      </div>
    </section>
  );
};

export default HowItWorks; 