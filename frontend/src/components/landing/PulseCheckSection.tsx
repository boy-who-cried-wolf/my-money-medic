import React from 'react';

const PulseCheckSection: React.FC = () => {
  return (
    <section className="relative py-24 overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 bg-gradient-to-b from-dark via-dark-lighter to-dark">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-primary/5 via-transparent to-transparent"></div>
      </div>

      {/* Content */}
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          {/* Left Side - Interactive Pulse Check */}
          <div className="relative">
            <div className="relative bg-gradient-to-br from-dark/50 to-dark-lighter/30 rounded-2xl backdrop-blur-xl border border-white/10 p-8">
              {/* Pulse Animation */}
              <div className="relative w-full aspect-square max-w-md mx-auto">
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="w-48 h-48 rounded-full bg-primary/10 animate-pulse"></div>
                  <div className="absolute w-48 h-48 rounded-full border-2 border-primary/20 animate-ping"></div>
                </div>
                <div className="absolute inset-0 flex items-center justify-center">
                  <div className="text-center">
                    <div className="text-4xl font-bold text-white mb-2">98</div>
                    <div className="text-sm text-gray-400">Financial Health Score</div>
                  </div>
                </div>
              </div>

              {/* Health Indicators */}
              <div className="grid grid-cols-3 gap-4 mt-8">
                <div className="text-center">
                  <div className="text-2xl font-semibold text-primary">92%</div>
                  <div className="text-sm text-gray-400">Savings Rate</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-semibold text-primary">85%</div>
                  <div className="text-sm text-gray-400">Investment</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-semibold text-primary">78%</div>
                  <div className="text-sm text-gray-400">Debt Ratio</div>
                </div>
              </div>
            </div>

            {/* Decorative Elements */}
            <div className="absolute -top-4 -right-4 w-32 h-32 bg-gradient-to-br from-primary to-primary/80 rounded-full filter blur-2xl opacity-20"></div>
            <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-gradient-to-br from-primary/80 to-primary/40 rounded-full filter blur-2xl opacity-20"></div>
          </div>

          {/* Right Side - Content */}
          <div className="relative">
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-primary/20 to-primary/10 backdrop-blur-sm border border-white/10 mb-6">
              <span className="flex h-2 w-2 mr-2">
                <span className="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-primary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
              </span>
              <span className="text-sm font-medium bg-gradient-to-r from-primary to-primary/80 bg-clip-text text-transparent">
                Real-time Financial Health
              </span>
            </div>

            <h2 className="text-4xl font-bold text-white mb-6">
              Your Financial
              <span className="block bg-gradient-to-r from-primary to-primary/80 bg-clip-text text-transparent">
                Pulse Check
              </span>
            </h2>

            <p className="text-lg text-gray-300 mb-8">
              Get instant insights into your financial health with our AI-powered pulse check. Monitor your savings, investments, and debt ratios in real-time.
            </p>

            {/* Features List */}
            <div className="space-y-4">
              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 mt-1">
                  <svg className="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                  </svg>
                </div>
                <div>
                  <div className="text-white font-medium">Real-time Monitoring</div>
                  <div className="text-sm text-gray-400">Track your financial metrics 24/7 with live updates</div>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 mt-1">
                  <svg className="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                </div>
                <div>
                  <div className="text-white font-medium">AI-Powered Insights</div>
                  <div className="text-sm text-gray-400">Get personalized recommendations based on your data</div>
                </div>
              </div>

              <div className="flex items-start space-x-3">
                <div className="w-6 h-6 rounded-full bg-primary/20 flex items-center justify-center flex-shrink-0 mt-1">
                  <svg className="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                </div>
                <div>
                  <div className="text-white font-medium">Instant Analysis</div>
                  <div className="text-sm text-gray-400">Quick assessment of your financial health status</div>
                </div>
              </div>
            </div>

            {/* CTA Button */}
            <button className="mt-8 group relative px-8 py-4 rounded-xl bg-gradient-to-r from-primary to-primary/80 text-white font-semibold overflow-hidden transition-all duration-300 hover:shadow-lg hover:shadow-primary/25">
              <span className="relative z-10 flex items-center">
                Check Your Pulse
                <svg className="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              </span>
              <div className="absolute inset-0 bg-gradient-to-r from-primary/80 to-primary opacity-0 group-hover:opacity-100 transition-opacity"></div>
            </button>
          </div>
        </div>
      </div>
    </section>
  );
};

export default PulseCheckSection; 