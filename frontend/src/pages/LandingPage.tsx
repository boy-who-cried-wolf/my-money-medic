import React from 'react';
import Navbar from '../components/Navbar';
import HeroSection from '../components/HeroSection';
import FeaturesSection from '../components/FeaturesSection';
import TestimonialsSection from '../components/TestimonialsSection';
import PricingSection from '../components/PricingSection';
import CTASection from '../components/CTASection';
import Footer from '../components/Footer';
import { motion } from 'framer-motion';

const sectionVariants = {
  hidden: { opacity: 0, y: 40 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.7, ease: 'easeOut' } },
};

const LandingPage: React.FC = () => {
  return (
    <div className="min-h-screen bg-dark">
      <Navbar />
      <main>
        <motion.section id="home" initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={sectionVariants}>
          <HeroSection />
        </motion.section>
        <motion.section id="pulsecheck" initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={sectionVariants}>
          <FeaturesSection />
        </motion.section>
        <motion.section id="testimonials" initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={sectionVariants}>
          <TestimonialsSection />
        </motion.section>
        <motion.section id="pricing" initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={sectionVariants}>
          <PricingSection />
        </motion.section>
        <motion.section id="about" initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={sectionVariants}>
          <CTASection />
        </motion.section>
      </main>
      <Footer />
    </div>
  );
};

export default LandingPage; 