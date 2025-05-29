import React from 'react';
import { motion } from 'framer-motion';

const newsItems = [
  {
    id: 1,
    title: 'Understanding Your Financial Health Score',
    excerpt: 'Learn how your financial health score is calculated and what it means for your financial future.',
    category: 'Financial Education',
    date: 'March 15, 2024',
    readTime: '5 min read',
    image: (
      <div className="w-full h-48 bg-gradient-to-br from-primary-500/20 to-primary-600/20 rounded-xl flex items-center justify-center">
        <svg className="w-16 h-16 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
    ),
  },
  {
    id: 2,
    title: 'The Power of Open Banking',
    excerpt: 'Discover how open banking is revolutionizing personal finance management and security.',
    category: 'Technology',
    date: 'March 12, 2024',
    readTime: '4 min read',
    image: (
      <div className="w-full h-48 bg-gradient-to-br from-primary-500/20 to-primary-600/20 rounded-xl flex items-center justify-center">
        <svg className="w-16 h-16 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
        </svg>
      </div>
    ),
  },
  {
    id: 3,
    title: 'Building Your Emergency Fund',
    excerpt: 'Essential tips and strategies for creating and maintaining a robust emergency fund.',
    category: 'Savings',
    date: 'March 10, 2024',
    readTime: '6 min read',
    image: (
      <div className="w-full h-48 bg-gradient-to-br from-primary-500/20 to-primary-600/20 rounded-xl flex items-center justify-center">
        <svg className="w-16 h-16 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      </div>
    ),
  },
];

const News = () => {
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
            Latest Insights &
            <span className="block text-primary-500 mt-2">Financial Tips</span>
          </h2>
          <p className="text-xl text-light-600 dark:text-dark-300 max-w-3xl mx-auto">
            Stay informed with our latest articles, tips, and insights to help you make better
            financial decisions and achieve your goals.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
          {newsItems.map((item, index) => (
            <motion.article
              key={item.id}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: index * 0.2 }}
              className="group relative"
            >
              <div className="absolute inset-0 bg-gradient-to-br from-primary-500/10 to-primary-600/10 rounded-2xl blur-xl group-hover:opacity-100 opacity-0 transition-opacity duration-500" />
              <div className="relative bg-white dark:bg-dark-800 rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-500 hover:-translate-y-1">
                {item.image}
                <div className="p-6">
                  <div className="flex items-center gap-4 mb-4">
                    <span className="px-3 py-1 text-sm font-medium text-primary-500 bg-primary-500/10 rounded-full">
                      {item.category}
                    </span>
                    <span className="text-sm text-light-500 dark:text-dark-400">
                      {item.date}
                    </span>
                  </div>
                  <h3 className="text-xl font-semibold text-light-900 dark:text-dark-100 mb-3 group-hover:text-primary-500 transition-colors duration-300">
                    {item.title}
                  </h3>
                  <p className="text-light-600 dark:text-dark-300 mb-4">
                    {item.excerpt}
                  </p>
                  <div className="flex items-center justify-between">
                    <span className="text-sm text-light-500 dark:text-dark-400">
                      {item.readTime}
                    </span>
                    <button className="text-primary-500 hover:text-primary-600 transition-colors duration-300">
                      Read More →
                    </button>
                  </div>
                </div>
              </div>
            </motion.article>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="mt-16 text-center"
        >
          <button className="btn-primary group relative overflow-hidden">
            <span className="relative z-10">View All Articles</span>
            <motion.div
              className="absolute inset-0 bg-primary-600"
              initial={{ x: '-100%' }}
              whileHover={{ x: 0 }}
              transition={{ duration: 0.3 }}
            />
          </button>
        </motion.div>
      </div>
    </section>
  );
};

export default News; 