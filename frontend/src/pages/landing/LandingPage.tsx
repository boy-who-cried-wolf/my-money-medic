import React from 'react';
import Navbar from '../../components/layout/Navbar';
import HeroSection from '../../components/landing/HeroSection';
import FeaturesSection from '../../components/landing/FeaturesSection';
import TestimonialsSection from '../../components/landing/TestimonialsSection';
import PricingSection from '../../components/landing/PricingSection';
import CTASection from '../../components/landing/CTASection';
import Footer from '../../components/layout/Footer';
import { motion } from 'framer-motion';
import BlogSection from '../../components/landing/BlogSection';
import PulseCheckSection from '../../components/landing/PulseCheckSection';

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
          <PulseCheckSection />
        </motion.section>
        <motion.section id="features" initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={sectionVariants}>
          <FeaturesSection />
        </motion.section>
        <motion.section id="blog" initial="hidden" whileInView="visible" viewport={{ once: true, amount: 0.3 }} variants={sectionVariants}>
          <BlogSection />
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