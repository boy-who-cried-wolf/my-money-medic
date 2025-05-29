import React from 'react';

const Testimonials = () => (
  <section className="section bg-white dark:bg-dark-900">
    <div className="container-custom text-center">
      <h2 className="text-3xl md:text-4xl font-bold text-light-900 dark:text-dark-100 mb-6">What Our Users Say</h2>
      <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="p-6 rounded-xl bg-light-50 dark:bg-dark-800 shadow">
          <p className="text-lg text-light-700 dark:text-dark-200 mb-4">“PulseCheck helped me understand my finances and set clear goals. The AI tips are spot on!”</p>
          <span className="block font-semibold text-primary-500">— Alex, 32</span>
        </div>
        <div className="p-6 rounded-xl bg-light-50 dark:bg-dark-800 shadow">
          <p className="text-lg text-light-700 dark:text-dark-200 mb-4">“I love how MyMoneyMedic connects to my bank and gives me a real health score. The action plan is easy to follow.”</p>
          <span className="block font-semibold text-primary-500">— Priya, 28</span>
        </div>
        <div className="p-6 rounded-xl bg-light-50 dark:bg-dark-800 shadow">
          <p className="text-lg text-light-700 dark:text-dark-200 mb-4">“The personalized insights and ongoing support keep me motivated to improve my financial health.”</p>
          <span className="block font-semibold text-primary-500">— Sam, 45</span>
        </div>
      </div>
    </div>
  </section>
);

export default Testimonials; 