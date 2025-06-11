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
          <section id="hero">
            <Hero />
          </section>
          <section id="how-it-works">
            <HowItWorks />
          </section>
          <section id="benefits">
            <Benefits />
          </section>
          <section id="features">
            <Features />
          </section>
          <section id="health-score">
            <HealthScore />
          </section>
          <section id="open-banking">
            <OpenBanking />
          </section>
          <section id="testimonials">
            <Testimonials />
          </section>
          <section id="faq">
            <FAQ />
          </section>
          <section id="news">
            <News />
          </section>
          <section id="newsletter">
            <Newsletter />
          </section>
        </main>
        <Footer />
      </div>
    </>
  );
};

export default LandingPage; 