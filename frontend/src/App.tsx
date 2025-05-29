import { BrowserRouter as Router } from 'react-router-dom';
import Benefits from './components/Benefits';
import CallToAction from './components/CallToAction';
import FAQ from './components/FAQ';
import Features from './components/Features';
import Footer from './components/Footer';
import HealthScore from './components/HealthScore';
import Hero from './components/Hero';
import HowItWorks from './components/HowItWorks';
import MetaTags from './components/MetaTags';
import Navbar from './components/Navbar';
import News from './components/News';
import Newsletter from './components/Newsletter';
import OpenBanking from './components/OpenBanking';
import Testimonials from './components/Testimonials';
import { NotificationProvider } from './context/NotificationContext';
import { ThemeProvider } from './context/ThemeContext';

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
