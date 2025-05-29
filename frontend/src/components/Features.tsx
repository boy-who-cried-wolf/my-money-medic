import React from 'react';
import { motion } from 'framer-motion';
import { useNotification } from '../context/NotificationContext';

const features = [
  {
    id: 1,
    title: 'AI-Powered Analysis',
    description: 'Get personalized financial insights powered by advanced AI algorithms that understand your unique situation.',
    icon: (
      <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
      </svg>
    ),
  },
  {
    id: 2,
    title: 'Real-Time Monitoring',
    description: 'Track your financial health in real-time with automatic updates and instant notifications.',
    icon: (
      <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
      </svg>
    ),
  },
  {
    id: 3,
    title: 'Secure Open Banking',
    description: 'Connect your accounts securely with bank-level encryption and real-time data synchronization.',
    icon: (
      <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
      </svg>
    ),
  },
  {
    id: 4,
    title: 'Personalized Action Plan',
    description: 'Receive a customized roadmap to improve your financial health with actionable steps.',
    icon: (
      <svg className="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
      </svg>
    ),
  },
];

const Features = () => {
  const { showNotification } = useNotification();

  const handleFeatureClick = (title: string) => {
    showNotification(`Learn more about ${title} coming soon!`);
  };

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
            Powerful Features for Your
            <span className="block text-primary-500 mt-2">Financial Success</span>
          </h2>
          <p className="text-xl text-light-600 dark:text-dark-300 max-w-3xl mx-auto">
            Discover how MyMoneyMedic combines cutting-edge technology with personalized insights
            to help you achieve your financial goals.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
          {features.map((feature, index) => (
            <motion.div
              key={feature.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: index * 0.2 }}
              className="group relative"
              onClick={() => handleFeatureClick(feature.title)}
            >
              <div className="absolute inset-0 bg-gradient-to-br from-primary-500/10 to-primary-600/10 rounded-2xl blur-xl group-hover:opacity-100 opacity-0 transition-opacity duration-500" />
              <div className="relative bg-white dark:bg-dark-800 rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-500 hover:-translate-y-1 cursor-pointer">
                <div className="flex items-start gap-6">
                  <div className="flex-shrink-0 w-16 h-16 rounded-xl bg-primary-500/10 flex items-center justify-center text-primary-500 group-hover:bg-primary-500 group-hover:text-white transition-all duration-500">
                    {feature.icon}
                  </div>
                  <div>
                    <h3 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-3 group-hover:text-primary-500 transition-colors duration-300">
                      {feature.title}
                    </h3>
                    <p className="text-light-600 dark:text-dark-300 leading-relaxed">
                      {feature.description}
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features; 