import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { useNotification } from '../context/NotificationContext';

const Newsletter = () => {
  const [email, setEmail] = useState('');
  const { showNotification } = useNotification();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    showNotification('Thank you for subscribing! The newsletter feature will be available soon.');
    setEmail('');
  };

  return (
    <section className="section bg-primary-500/10 dark:bg-primary-500/5">
      <div className="container-custom">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8 }}
          className="max-w-2xl mx-auto text-center"
        >
          <h2 className="text-3xl md:text-4xl font-bold text-light-900 dark:text-dark-100 mb-4">
            Stay Updated
          </h2>
          <p className="text-lg text-light-600 dark:text-dark-300 mb-8">
            Subscribe to our newsletter for the latest financial wellness tips and updates.
          </p>
          <form onSubmit={handleSubmit} className="flex flex-col sm:flex-row gap-4">
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="Enter your email"
              className="flex-1 px-6 py-3 rounded-lg bg-light-50 dark:bg-dark-700 text-light-900 dark:text-dark-100 focus:outline-none focus:ring-2 focus:ring-primary-500"
              required
            />
            <button
              type="submit"
              className="px-6 py-3 bg-primary-500 text-dark-900 font-medium rounded-lg hover:bg-primary-600 transition-colors"
            >
              Subscribe
            </button>
          </form>
        </motion.div>
      </div>
    </section>
  );
};

export default Newsletter; 