import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { NotificationProvider } from './context/NotificationContext';
import Navbar from './components/Navbar';
import Hero from './components/Hero';
import Features from './components/Features';
import News from './components/News';
import Newsletter from './components/Newsletter';
import Footer from './components/Footer';
import MetaTags from './components/MetaTags';
import HowItWorks from './components/HowItWorks';
import Benefits from './components/Benefits';
import Testimonials from './components/Testimonials';
import HealthScore from './components/HealthScore';
import OpenBanking from './components/OpenBanking';
import FAQ from './components/FAQ';
import CallToAction from './components/CallToAction';

const App = () => {
  return (
    <ThemeProvider>
      <NotificationProvider>
        <Router>
          <MetaTags />
          <div className="min-h-screen flex flex-col">
            <Navbar />
            <main className="flex-grow">
              <Hero />
              <HowItWorks />
              <Benefits />
              <Features />
              <HealthScore />
              <OpenBanking />
              <Testimonials />
              <FAQ />
              <CallToAction />
              <News />
              <Newsletter />
            </main>
            <Footer />
          </div>
        </Router>
      </NotificationProvider>
    </ThemeProvider>
  );
};

export default App;
