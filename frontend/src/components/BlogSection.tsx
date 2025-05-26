import React from 'react';

const BlogSection: React.FC = () => {
  const blogPosts = [
    {
      title: "Understanding Your Financial Health Score",
      excerpt: "Learn how to interpret your PulseCheck results and make meaningful improvements.",
      date: "May 15, 2024",
      readTime: "5 min read",
      image: "https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=400&q=80"
    },
    {
      title: "The Connection Between Mental and Financial Health",
      excerpt: "Discover how your financial wellbeing impacts your overall mental health.",
      date: "May 10, 2024",
      readTime: "7 min read",
      image: "https://images.unsplash.com/photo-1465101046530-73398c7f28ca?auto=format&fit=crop&w=400&q=80"
    },
    {
      title: "Smart Investment Strategies for Beginners",
      excerpt: "Start your investment journey with these proven strategies and tips.",
      date: "May 5, 2024",
      readTime: "6 min read",
      image: "https://images.unsplash.com/photo-1515168833906-d2a3b82b3029?auto=format&fit=crop&w=400&q=80"
    }
  ];

  return (
    <section className="relative py-24 overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-gradient-to-b from-dark-lighter via-dark to-dark-lighter">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_right,_var(--tw-gradient-stops))] from-primary/10 via-transparent to-transparent"></div>
      </div>

      {/* Content */}
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-16">
          <div className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-primary/20 to-primary/10 backdrop-blur-sm border border-white/10 mb-6">
            <span className="flex h-2 w-2 mr-2">
              <span className="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-primary opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
            </span>
            <span className="text-sm font-medium bg-gradient-to-r from-primary to-primary/80 bg-clip-text text-transparent">
              Conor's Corner
            </span>
          </div>
          <h2 className="text-4xl font-bold text-white mb-6">
            Insights & Strategies
            <span className="block bg-gradient-to-r from-primary to-primary/80 bg-clip-text text-transparent">
              For Your Financial Wellbeing
            </span>
          </h2>
          <p className="text-lg text-gray-300 max-w-3xl mx-auto">
            Expert insights, tips, and strategies to improve your financial wellbeing from our founder, Conor.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-10">
          {blogPosts.map((post, index) => (
            <div
              key={index}
              className="group relative bg-gradient-to-br from-dark/60 to-dark-lighter/40 rounded-2xl overflow-hidden border border-white/10 shadow-lg hover:shadow-2xl hover:shadow-primary/20 transition-all duration-300"
            >
              {/* Image */}
              <div className="h-48 w-full overflow-hidden">
                <img
                  src={post.image}
                  alt={post.title}
                  className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-500"
                />
              </div>
              {/* Card Content */}
              <div className="p-6 flex flex-col h-full">
                <div className="flex justify-between items-center mb-3">
                  <span className="text-xs text-gray-400 uppercase tracking-wide font-semibold">{post.date}</span>
                  <span className="text-xs text-primary font-semibold">{post.readTime}</span>
                </div>
                <h3 className="text-xl font-bold text-white mb-2 group-hover:text-primary transition-colors duration-300">
                  {post.title}
                </h3>
                <p className="text-gray-300 mb-4 flex-1">
                  {post.excerpt}
                </p>
                <a
                  href="#"
                  className="text-primary hover:text-primary/80 font-medium inline-flex items-center mt-auto"
                >
                  Read More
                  <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                  </svg>
                </a>
              </div>
            </div>
          ))}
        </div>

        <div className="text-center mt-16">
          <button className="group relative px-8 py-4 rounded-xl bg-gradient-to-r from-primary to-primary/80 text-white font-semibold overflow-hidden transition-all duration-300 hover:shadow-lg hover:shadow-primary/25">
            <span className="relative z-10 flex items-center">
              Explore All Articles
              <svg className="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
              </svg>
            </span>
            <div className="absolute inset-0 bg-gradient-to-r from-primary/80 to-primary opacity-0 group-hover:opacity-100 transition-opacity"></div>
          </button>
        </div>
      </div>
    </section>
  );
};

export default BlogSection; 