import React from 'react';
import { Link } from 'react-router-dom';

const CallToAction = () => (
  <section className="section bg-primary-500 text-white text-center">
    <div className="container-custom">
      <h2 className="text-3xl md:text-4xl font-bold mb-4">Ready to Take Control of Your Financial Health?</h2>
      <p className="text-lg mb-8">Start your journey with PulseCheck and get your personalized action plan today.</p>
      <Link to="/sign-up" className="btn-primary bg-white text-primary-500 hover:bg-light-100 font-bold px-8 py-4 rounded-lg text-lg shadow transition-colors duration-200 inline-block">
        Start Your PulseCheck
      </Link>
    </div>
  </section>
);

export default CallToAction; 