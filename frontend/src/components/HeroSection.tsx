import React from 'react';

const HeroSection: React.FC = () => {
  return (
    <div className="relative min-h-screen bg-gradient-to-br from-dark via-dark-lighter to-black overflow-hidden">
      {/* Animated background elements */}
      <div className="absolute inset-0">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_var(--tw-gradient-stops))] from-primary/10 via-transparent to-transparent"></div>
        <div className="absolute inset-0 bg-[linear-gradient(to_right,#10b981,#10b981)] opacity-5 mix-blend-multiply"></div>
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAzNGMwIDIuMjA5LTEuNzkxIDQtNCA0cy00LTEuNzkxLTQtNCAxLjc5MS00IDQtNCA0IDEuNzkxIDQgNHoiIGZpbGw9IiNmZmYiIGZpbGwtb3BhY2l0eT0iLjEiLz48L2c+PC9zdmc+')] opacity-10"></div>
      </div>

      {/* Floating orbs */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -left-40 w-80 h-80 bg-primary/20 rounded-full filter blur-3xl animate-blob"></div>
        <div className="absolute top-0 -right-40 w-80 h-80 bg-primary/10 rounded-full filter blur-3xl animate-blob animation-delay-2000"></div>
        <div className="absolute -bottom-40 left-20 w-80 h-80 bg-primary/5 rounded-full filter blur-3xl animate-blob animation-delay-4000"></div>
      </div>

      {/* Main content */}
      <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-16">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center mt-8">
          {/* Left content */}
          <div className="relative z-10">
            {/* Badge */}
            <div className="inline-flex items-center px-4 py-2 rounded-full bg-gradient-to-r from-primary/20 to-primary/10 backdrop-blur-sm border border-white/10 mb-10">
              <span className="flex h-2 w-2 mr-2">
                <span className="animate-ping absolute inline-flex h-2 w-2 rounded-full bg-primary opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2 w-2 bg-primary"></span>
              </span>
              <span className="text-sm font-medium bg-gradient-to-r from-primary to-primary/80 bg-clip-text text-transparent">
                AI-Powered Financial Wellness
              </span>
            </div>

            {/* Main heading */}
            <h1 className="text-5xl md:text-7xl font-bold text-white mb-8 leading-tight">
              Transform Your
              <span className="block bg-gradient-to-r from-primary to-primary/80 bg-clip-text text-transparent">
                Financial Future
              </span>
            </h1>

            {/* Description */}
            <p className="text-xl text-gray-300 mb-10 max-w-xl">
              Experience the power of AI-driven financial guidance. Get personalized insights, real-time monitoring, and expert recommendations for your financial wellbeing.
            </p>

            {/* CTA Buttons */}
            <div className="flex flex-col sm:flex-row gap-4 mb-12">
              <button className="group relative px-8 py-4 rounded-xl bg-gradient-to-r from-primary to-primary/80 text-white font-semibold overflow-hidden transition-all duration-300 hover:shadow-lg hover:shadow-primary/25">
                <span className="relative z-10 flex items-center">
                  Start Your Journey
                  <svg className="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                  </svg>
                </span>
                <div className="absolute inset-0 bg-gradient-to-r from-primary/80 to-primary opacity-0 group-hover:opacity-100 transition-opacity"></div>
              </button>
              <button className="group px-8 py-4 rounded-xl bg-white/10 backdrop-blur-sm text-white font-semibold border border-white/10 hover:bg-white/20 transition-all duration-300">
                <span className="flex items-center">
                  Watch Demo
                  <svg className="w-5 h-5 ml-2 transform group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14.752 11.168l-3.197-2.132A1 1 0 0010 9.87v4.263a1 1 0 001.555.832l3.197-2.132a1 1 0 000-1.664z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </span>
              </button>
            </div>

            {/* Trust badges */}
            <div className="mt-16 flex flex-wrap gap-8">
              <div className="flex items-center text-gray-400">
                <svg className="w-5 h-5 mr-2 text-primary" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span>Bank-Level Security</span>
              </div>
              <div className="flex items-center text-gray-400">
                <svg className="w-5 h-5 mr-2 text-primary" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span>24/7 AI Support</span>
              </div>
              <div className="flex items-center text-gray-400">
                <svg className="w-5 h-5 mr-2 text-primary" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span>Real-time Insights</span>
              </div>
            </div>
          </div>

          {/* Right content - Professional Dashboard */}
          <div className="relative">
            <div className="relative w-full aspect-[4/3] transform perspective-1000">
              {/* Main Dashboard Card */}
              <div className="absolute inset-0 bg-gradient-to-br from-dark/50 to-dark-lighter/30 rounded-2xl backdrop-blur-xl border border-white/10 transform rotate-y-6 transition-transform duration-500 hover:rotate-y-0">
                <div className="absolute inset-0 p-8">
                  {/* Header */}
                  <div className="flex justify-between items-center mb-6">
                    <div className="flex items-center space-x-2">
                      <div className="w-3 h-3 rounded-full bg-primary"></div>
                      <span className="text-sm text-gray-300">Live Portfolio</span>
                    </div>
                    <div className="text-sm text-gray-400">Last updated: Just now</div>
                  </div>

                  {/* Main Chart */}
                  <div className="relative h-48 mb-6">
                    <svg className="w-full h-full" viewBox="0 0 400 200" fill="none" xmlns="http://www.w3.org/2000/svg">
                      {/* Grid Lines */}
                      <path d="M0 40H400" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />
                      <path d="M0 80H400" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />
                      <path d="M0 120H400" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />
                      <path d="M0 160H400" stroke="rgba(255,255,255,0.1)" strokeWidth="1" />
                      
                      {/* Main Chart Line */}
                      <path d="M0 160L50 150L100 155L150 140L200 145L250 130L300 135L350 120L400 125" 
                            stroke="url(#gradientLine)" strokeWidth="3" strokeLinecap="round" strokeLinejoin="round"/>
                      
                      {/* Area Fill */}
                      <path d="M0 160L50 150L100 155L150 140L200 145L250 130L300 135L350 120L400 125L400 200L0 200Z" 
                            fill="url(#gradientArea)" fillOpacity="0.2"/>
                      
                      <defs>
                        <linearGradient id="gradientLine" x1="0" y1="0" x2="400" y2="0">
                          <stop offset="0%" stopColor="#10b981" />
                          <stop offset="100%" stopColor="#059669" />
                        </linearGradient>
                        <linearGradient id="gradientArea" x1="0" y1="0" x2="0" y2="200">
                          <stop offset="0%" stopColor="#10b981" stopOpacity="0.4" />
                          <stop offset="100%" stopColor="#10b981" stopOpacity="0" />
                        </linearGradient>
                      </defs>
                    </svg>
                  </div>

                  {/* Stats Grid */}
                  <div className="grid grid-cols-2 gap-4">
                    {/* Portfolio Value */}
                    <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                      <div className="text-sm text-gray-400 mb-1">Portfolio Value</div>
                      <div className="text-xl font-semibold text-white">$24,500</div>
                      <div className="text-sm text-primary flex items-center mt-1">
                        <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                        </svg>
                        +24.5%
                      </div>
                    </div>

                    {/* Monthly Growth */}
                    <div className="bg-white/5 rounded-xl p-4 border border-white/10">
                      <div className="text-sm text-gray-400 mb-1">Monthly Growth</div>
                      <div className="text-xl font-semibold text-white">$2,450</div>
                      <div className="text-sm text-primary flex items-center mt-1">
                        <svg className="w-4 h-4 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
                        </svg>
                        +12.3%
                      </div>
                    </div>
                  </div>

                  {/* AI Insights */}
                  <div className="mt-4 bg-gradient-to-r from-primary/10 to-primary/5 rounded-xl p-4 border border-white/10">
                    <div className="flex items-start space-x-3">
                      <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
                        <svg className="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                        </svg>
                      </div>
                      <div>
                        <div className="text-sm font-medium text-white">AI Insight</div>
                        <div className="text-sm text-gray-400">Your portfolio is performing above market average. Consider diversifying into tech stocks.</div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              {/* Decorative Elements */}
              <div className="absolute -top-4 -right-4 w-32 h-32 bg-gradient-to-br from-primary to-primary/80 rounded-full filter blur-2xl opacity-20"></div>
              <div className="absolute -bottom-4 -left-4 w-32 h-32 bg-gradient-to-br from-primary/80 to-primary/40 rounded-full filter blur-2xl opacity-20"></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default HeroSection; 