import React from 'react';
import Navbar from './components/Navbar';
import HeroSection from './components/HeroSection';
import PulseCheckSection from './components/PulseCheckSection';
import BlogSection from './components/BlogSection';
import FeaturesSection from './components/FeaturesSection';
import CTASection from './components/CTASection';
import TestimonialsSection from './components/TestimonialsSection';
import Footer from './components/Footer';

function App() {
  return (
    <div className="bg-dark min-h-screen">
      <Navbar />
      <HeroSection />
      <PulseCheckSection />
      <BlogSection />
      <FeaturesSection />
      <CTASection />
      <TestimonialsSection />
      <Footer />
    </div>
  );
}

export default App;
