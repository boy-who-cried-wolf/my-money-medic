import { Helmet } from 'react-helmet';

interface MetaTagsProps {
  title?: string;
  description?: string;
  keywords?: string;
  ogTitle?: string;
  ogDescription?: string;
  ogImage?: string;
  ogUrl?: string;
}

const MetaTags = ({
  title = 'MyMoneyMedic - Integrated Financial Health Check Platform',
  description = 'MyMoneyMedic is your integrated financial health check platform. Start with PulseCheck, an interactive quiz to discover your goals and status. Get AI-powered suggestions, open banking integration, personalized insights, health score, and a tailored action plan for better financial well-being.',
  keywords = 'financial health, PulseCheck, MyMoneyMedic, AI financial advice, open banking, personalized insights, health score, action plan, financial wellness',
  ogTitle,
  ogDescription,
  ogImage = '/logo.svg',
  ogUrl = window.location.href,
}: MetaTagsProps) => {
  return (
    <Helmet>
      {/* Basic Meta Tags */}
      <title>{title}</title>
      <meta name="description" content={description} />
      <meta name="keywords" content={keywords} />
      
      {/* Open Graph Meta Tags */}
      <meta property="og:title" content={ogTitle || title} />
      <meta property="og:description" content={ogDescription || description} />
      <meta property="og:image" content={ogImage} />
      <meta property="og:url" content={ogUrl} />
      <meta property="og:type" content="website" />
      
      {/* Twitter Card Meta Tags */}
      <meta name="twitter:card" content="summary_large_image" />
      <meta name="twitter:title" content={ogTitle || title} />
      <meta name="twitter:description" content={ogDescription || description} />
      <meta name="twitter:image" content={ogImage} />
      
      {/* Additional Meta Tags */}
      <meta name="viewport" content="width=device-width, initial-scale=1" />
      <meta charSet="utf-8" />
      <meta name="theme-color" content="#00E575" />
    </Helmet>
  );
};

export default MetaTags; 