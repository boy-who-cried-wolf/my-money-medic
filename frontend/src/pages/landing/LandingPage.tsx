import Benefits from '../../components/Benefits';
import FAQ from '../../components/FAQ';
import Features from '../../components/Features';
import Footer from '../../components/Footer';
import HealthScore from '../../components/HealthScore';
import Hero from '../../components/Hero';
import HowItWorks from '../../components/HowItWorks';
import MetaTags from '../../components/MetaTags';
import Navbar from '../../components/Navbar';
import News from '../../components/News';
import Newsletter from '../../components/Newsletter';
import OpenBanking from '../../components/OpenBanking';
import Testimonials from '../../components/Testimonials';

const LandingPage = () => {
  return (
    <>
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
          <News />
          <Newsletter />
        </main>
        <Footer />
      </div>
    </>
  );
};

export default LandingPage; 