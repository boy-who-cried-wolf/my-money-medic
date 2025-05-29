import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const faqs = [
  {
    question: 'What is PulseCheck?',
    answer: 'PulseCheck is a quick, interactive quiz that helps you discover your financial goals and current status. It\'s the first step in your MyMoneyMedic journey, providing personalized insights and recommendations based on your unique situation.',
  },
  {
    question: 'How does MyMoneyMedic use my data?',
    answer: 'With your permission, we use your answers and (optionally) your bank data to provide personalized insights and action plans. Your privacy and security are our top priorities. We use bank-level encryption and never share your data without your explicit consent.',
  },
  {
    question: 'Is my information secure?',
    answer: 'Absolutely. We use bank-level encryption and security measures to protect your data. Our platform is built with the highest security standards, and we regularly undergo security audits to ensure your information remains safe and private.',
  },
  {
    question: 'Can I get support as my situation changes?',
    answer: 'Yes! MyMoneyMedic offers ongoing support and tips as your financial journey evolves. Our platform adapts to your changing circumstances, providing relevant insights and recommendations to help you stay on track with your financial goals.',
  },
  {
    question: 'How does the financial health score work?',
    answer: 'Your financial health score is calculated based on various factors including your spending habits, savings, investments, and financial goals. The score provides a clear picture of your financial well-being and helps track your progress over time.',
  },
  {
    question: 'What makes MyMoneyMedic different?',
    answer: 'MyMoneyMedic combines AI-powered analysis with personalized insights to provide a comprehensive financial health solution. We focus on your unique situation, offering actionable steps and ongoing support to help you achieve your financial goals.',
  },
];

const FAQ = () => {
  const [openIndex, setOpenIndex] = useState<number | null>(null);

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
            Frequently Asked
            <span className="block text-primary-500 mt-2">Questions</span>
          </h2>
          <p className="text-xl text-light-600 dark:text-dark-300 max-w-3xl mx-auto">
            Find answers to common questions about MyMoneyMedic and how we can help you
            achieve better financial health.
          </p>
        </motion.div>

        <div className="max-w-3xl mx-auto space-y-4">
          {faqs.map((faq, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true }}
              transition={{ duration: 0.8, delay: index * 0.1 }}
              className="group"
            >
              <button
                onClick={() => setOpenIndex(openIndex === index ? null : index)}
                className="w-full text-left bg-white dark:bg-dark-800 rounded-2xl p-6 shadow-lg hover:shadow-xl transition-all duration-500"
              >
                <div className="flex items-center justify-between gap-4">
                  <h3 className="text-xl font-semibold text-light-900 dark:text-dark-100 group-hover:text-primary-500 transition-colors duration-300">
                    {faq.question}
                  </h3>
                  <div className="flex-shrink-0 w-6 h-6">
                    <motion.div
                      animate={{ rotate: openIndex === index ? 180 : 0 }}
                      transition={{ duration: 0.3 }}
                    >
                      <svg className="w-6 h-6 text-primary-500" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                      </svg>
                    </motion.div>
        </div>
        </div>
                <AnimatePresence>
                  {openIndex === index && (
                    <motion.div
                      initial={{ height: 0, opacity: 0 }}
                      animate={{ height: 'auto', opacity: 1 }}
                      exit={{ height: 0, opacity: 0 }}
                      transition={{ duration: 0.3 }}
                      className="overflow-hidden"
                    >
                      <p className="mt-4 text-light-600 dark:text-dark-300">
                        {faq.answer}
                      </p>
                    </motion.div>
                  )}
                </AnimatePresence>
              </button>
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
          <p className="text-light-600 dark:text-dark-300 mb-6">
            Still have questions? We're here to help!
          </p>
          <button className="btn-primary group relative overflow-hidden">
            <span className="relative z-10">Contact Support</span>
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

export default FAQ; 