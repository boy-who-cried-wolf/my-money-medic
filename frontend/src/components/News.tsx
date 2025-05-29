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
    image: 'https://static.wixstatic.com/media/eaa99f_2bbb581667b742c49549f7e1eb8c2549~mv2.jpg/v1/fill/w_456,h_342,fp_0.50_0.50,q_90,enc_avif,quality_auto/eaa99f_2bbb581667b742c49549f7e1eb8c2549~mv2.webp',
  },
  {
    id: 2,
    title: 'The Power of Open Banking',
    excerpt: 'Discover how open banking is revolutionizing personal finance management and security.',
    category: 'Technology',
    date: 'March 12, 2024',
    readTime: '4 min read',
    image: 'https://static.wixstatic.com/media/eaa99f_2c856b8c619c49c48b0a18e4e6197cc3~mv2.jpg/v1/fill/w_457,h_342,fp_0.50_0.50,q_90,enc_avif,quality_auto/eaa99f_2c856b8c619c49c48b0a18e4e6197cc3~mv2.webp',
  },
  {
    id: 3,
    title: 'Building Your Emergency Fund',
    excerpt: 'Essential tips and strategies for creating and maintaining a robust emergency fund.',
    category: 'Savings',
    date: 'March 10, 2024',
    readTime: '6 min read',
    image: 'https://static.wixstatic.com/media/eaa99f_9e1a77114dc24035953d8207e0b01ada~mv2.jpg/v1/fill/w_456,h_342,fp_0.50_0.50,q_90,enc_avif,quality_auto/eaa99f_9e1a77114dc24035953d8207e0b01ada~mv2.webp',
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
              <div className="relative bg-white dark:bg-dark-800 rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-all duration-500 hover:-translate-y-1 flex flex-col h-[600px]">
                <div className="w-full h-[342px] relative flex-shrink-0">
                  <img
                    src={item.image}
                    alt={item.title}
                    className="w-full h-full object-cover"
                  />
                </div>
                <div className="p-6 flex flex-col flex-grow">
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
                  <p className="text-light-600 dark:text-dark-300 mb-4 flex-grow">
                    {item.excerpt}
                  </p>
                  <div className="flex items-center justify-between mt-auto">
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