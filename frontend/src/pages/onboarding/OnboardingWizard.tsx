import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { useNavigate } from 'react-router-dom';
import MetaTags from '../../components/MetaTags';
import Navbar from '../../components/Navbar';
import Footer from '../../components/Footer';
import { useAuthContext } from '../../context/AuthContext';
import ProtectedRoute from '../../components/ProtectedRoute';

// Define the types for our questions and answers
interface Question {
  id: number;
  title: string;
  description: string;
  type: 'single' | 'multiple' | 'text' | 'number' | 'slider' | 'rating' | 'date' | 'currency';
  options?: string[];
  placeholder?: string;
  min?: number;
  max?: number;
  step?: number;
  unit?: string;
  currency?: string;
}

interface Answer {
  questionId: number;
  value: string | string[] | number;
}

const questions: Question[] = [
  {
    id: 1,
    title: "What's your primary financial goal?",
    description: "This will help us tailor our recommendations to your needs",
    type: "single",
    options: [
      "Save for retirement",
      "Pay off debt",
      "Build emergency fund",
      "Invest for growth",
      "Plan for major purchase",
      "Start a business",
      "Education funding",
      "Buy a home"
    ]
  },
  {
    id: 2,
    title: "What's your current financial situation?",
    description: "Be honest - this helps us provide better guidance",
    type: "multiple",
    options: [
      "I have credit card debt",
      "I have student loans",
      "I have a mortgage",
      "I have savings",
      "I have investments",
      "I'm living paycheck to paycheck",
      "I have a side business",
      "I receive passive income",
      "I have a pension",
      "I have insurance policies"
    ]
  },
  {
    id: 3,
    title: "What's your monthly income?",
    description: "This helps us understand your financial capacity",
    type: "currency",
    placeholder: "Enter your monthly income in AUD",
    currency: "AUD"
  },
  {
    id: 4,
    title: "What's your risk tolerance?",
    description: "This helps us recommend suitable investment strategies",
    type: "slider",
    min: 1,
    max: 10,
    step: 1,
    options: [
      "Very Conservative",
      "Conservative",
      "Moderate",
      "Aggressive",
      "Very Aggressive"
    ]
  },
  {
    id: 5,
    title: "What's your time horizon?",
    description: "When do you plan to achieve your financial goals?",
    type: "single",
    options: [
      "Less than 1 year",
      "1-3 years",
      "3-5 years",
      "5-10 years",
      "More than 10 years"
    ]
  },
  {
    id: 6,
    title: "How would you rate your financial knowledge?",
    description: "This helps us provide the right level of guidance",
    type: "rating",
    min: 1,
    max: 5,
    options: [
      "Beginner",
      "Intermediate",
      "Advanced",
      "Expert"
    ]
  },
  {
    id: 7,
    title: "What's your target retirement age?",
    description: "This helps us plan your long-term financial strategy",
    type: "date",
    placeholder: "Select your target retirement date"
  },
  {
    id: 8,
    title: "What's your current monthly savings?",
    description: "This helps us understand your saving habits",
    type: "currency",
    placeholder: "Enter your monthly savings in AUD",
    currency: "AUD"
  },
  {
    id: 9,
    title: "What are your investment preferences?",
    description: "Select all that apply to your investment strategy",
    type: "multiple",
    options: [
      "Stocks and shares",
      "Bonds",
      "Real estate",
      "Cryptocurrency",
      "Precious metals",
      "Mutual funds",
      "ETFs",
      "P2P lending",
      "Crowdfunding",
      "None of the above"
    ]
  },
  {
    id: 10,
    title: "How do you feel about financial technology?",
    description: "This helps us recommend suitable digital tools",
    type: "rating",
    min: 1,
    max: 5,
    options: [
      "Not comfortable",
      "Somewhat comfortable",
      "Comfortable",
      "Very comfortable"
    ]
  }
];

const OnboardingWizard = () => {
  const [currentStep, setCurrentStep] = useState(0);
  const [answers, setAnswers] = useState<Answer[]>([]);
  const navigate = useNavigate();
  const { isAuthenticated } = useAuthContext();

  const handleAnswer = (value: string | string[] | number) => {
    const newAnswers = [...answers];
    const existingAnswerIndex = newAnswers.findIndex(
      (answer) => answer.questionId === questions[currentStep].id
    );

    if (existingAnswerIndex !== -1) {
      newAnswers[existingAnswerIndex].value = value;
    } else {
      newAnswers.push({
        questionId: questions[currentStep].id,
        value,
      });
    }

    setAnswers(newAnswers);
  };

  const handleNext = () => {
    if (currentStep < questions.length - 1) {
      setCurrentStep(currentStep + 1);
    } else {
      // Save answers and navigate to dashboard
      // TODO: Implement API call to save answers
      navigate('/dashboard');
    }
  };

  const handleBack = () => {
    if (currentStep > 0) {
      setCurrentStep(currentStep - 1);
    }
  };

  const currentQuestion = questions[currentStep];
  const currentAnswer = answers.find(
    (answer) => answer.questionId === currentQuestion.id
  );

  const renderQuestionInput = () => {
    switch (currentQuestion.type) {
      case 'single':
        return (
          <div className="grid gap-3">
            {currentQuestion.options?.map((option) => (
              <motion.button
                key={option}
                onClick={() => handleAnswer(option)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
                className={`w-full p-4 text-left rounded-xl border transition-all duration-200 ${
                  currentAnswer?.value === option
                    ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20 text-primary-700 dark:text-primary-300 shadow-sm'
                    : 'border-light-300 dark:border-dark-600 hover:border-primary-500 dark:hover:border-primary-500 hover:shadow-sm'
                }`}
              >
                {option}
              </motion.button>
            ))}
          </div>
        );

      case 'multiple':
        return (
          <div className="grid gap-3">
            {currentQuestion.options?.map((option) => (
              <motion.label
                key={option}
                whileHover={{ scale: 1.02 }}
                className="flex items-center space-x-4 p-4 rounded-xl border border-light-300 dark:border-dark-600 hover:border-primary-500 dark:hover:border-primary-500 cursor-pointer transition-all duration-200 hover:shadow-sm"
              >
                <div className="relative">
                  <input
                    type="checkbox"
                    checked={(currentAnswer?.value as string[])?.includes(option)}
                    onChange={(e) => {
                      const currentValues = (currentAnswer?.value as string[]) || [];
                      const newValues = e.target.checked
                        ? [...currentValues, option]
                        : currentValues.filter((v) => v !== option);
                      handleAnswer(newValues);
                    }}
                    className="h-5 w-5 text-primary-500 focus:ring-primary-500 border-light-300 dark:border-dark-600 rounded"
                  />
                </div>
                <span className="text-light-900 dark:text-dark-100">{option}</span>
              </motion.label>
            ))}
          </div>
        );

      case 'slider':
        return (
          <div className="space-y-4">
            <input
              type="range"
              min={currentQuestion.min}
              max={currentQuestion.max}
              step={currentQuestion.step}
              value={(currentAnswer?.value as number) || currentQuestion.min}
              onChange={(e) => handleAnswer(Number(e.target.value))}
              className="w-full h-2 bg-light-200 dark:bg-dark-700 rounded-lg appearance-none cursor-pointer"
            />
            <div className="flex justify-between text-sm text-light-600 dark:text-dark-300">
              {currentQuestion.options?.map((option, index) => (
                <span key={option}>{option}</span>
              ))}
            </div>
          </div>
        );

      case 'rating':
        return (
          <div className="flex justify-center space-x-4">
            {Array.from({ length: currentQuestion.max || 5 }).map((_, index) => (
              <motion.button
                key={index}
                whileHover={{ scale: 1.1 }}
                whileTap={{ scale: 0.9 }}
                onClick={() => handleAnswer(index + 1)}
                className={`w-12 h-12 rounded-full flex items-center justify-center text-xl font-bold transition-all duration-200 ${
                  (currentAnswer?.value as number) === index + 1
                    ? 'bg-primary-500 text-white'
                    : 'bg-light-100 dark:bg-dark-700 text-light-600 dark:text-dark-300 hover:bg-primary-100 dark:hover:bg-primary-900/20'
                }`}
              >
                {index + 1}
              </motion.button>
            ))}
          </div>
        );

      case 'date':
        return (
          <input
            type="date"
            value={(currentAnswer?.value as string) || ''}
            onChange={(e) => handleAnswer(e.target.value)}
            className="w-full px-4 py-3 border border-light-300 dark:border-dark-600 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-dark-700 text-light-900 dark:text-dark-100"
          />
        );

      case 'currency':
        return (
          <div className="relative">
            <span className="absolute left-4 top-1/2 -translate-y-1/2 text-light-600 dark:text-dark-300">
              {currentQuestion.currency}
            </span>
            <input
              type="number"
              value={(currentAnswer?.value as number) || ''}
              onChange={(e) => handleAnswer(Number(e.target.value))}
              placeholder={currentQuestion.placeholder}
              className="w-full pl-12 pr-4 py-3 border border-light-300 dark:border-dark-600 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-dark-700 text-light-900 dark:text-dark-100"
            />
          </div>
        );

      default:
        return (
          <input
            type="text"
            value={(currentAnswer?.value as string) || ''}
            onChange={(e) => handleAnswer(e.target.value)}
            placeholder={currentQuestion.placeholder}
            className="w-full px-4 py-3 border border-light-300 dark:border-dark-600 rounded-xl focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white dark:bg-dark-700 text-light-900 dark:text-dark-100"
          />
        );
    }
  };

  return (
    <ProtectedRoute>
      <MetaTags />
      <div className="min-h-screen flex flex-col bg-gradient-to-br from-light-50/50 to-light-100/50 dark:from-dark-900/50 dark:to-dark-800/50">
        <Navbar />
        <main className="flex-grow container-custom py-12 px-4 sm:px-6 lg:px-8 mt-16">
          <div className="max-w-3xl mx-auto">
            {/* Welcome Section */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5 }}
              className="text-center mb-12"
            >
              <h1 className="text-4xl font-bold text-light-900 dark:text-dark-100 mb-4">
                Let's Get to Know You
              </h1>
              <p className="text-lg text-light-600 dark:text-dark-300">
                Help us understand your financial goals to provide personalized recommendations
              </p>
            </motion.div>

            {/* Progress Bar */}
            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.5, delay: 0.2 }}
              className="mb-12"
            >
              <div className="flex justify-between mb-3">
                <span className="text-sm font-medium text-light-600 dark:text-dark-300">
                  Step {currentStep + 1} of {questions.length}
                </span>
                <span className="text-sm font-medium text-primary-500">
                  {Math.round(((currentStep + 1) / questions.length) * 100)}% Complete
                </span>
              </div>
              <div className="w-full bg-light-200 dark:bg-dark-700 rounded-full h-2.5 overflow-hidden">
                <motion.div
                  className="bg-gradient-to-r from-primary-500 to-primary-600 h-full rounded-full"
                  initial={{ width: 0 }}
                  animate={{
                    width: `${((currentStep + 1) / questions.length) * 100}%`,
                  }}
                  transition={{ duration: 0.5, ease: "easeInOut" }}
                />
              </div>
            </motion.div>

            {/* Question Card */}
            <AnimatePresence mode="wait">
              <motion.div
                key={currentStep}
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                exit={{ opacity: 0, x: -20 }}
                transition={{ duration: 0.3 }}
                className="bg-white dark:bg-dark-800 rounded-2xl shadow-xl p-8 relative overflow-hidden"
              >
                {/* Decorative Elements */}
                <div className="absolute top-0 right-0 w-32 h-32 bg-primary-500/5 rounded-full blur-2xl -translate-y-1/2 translate-x-1/2" />
                <div className="absolute bottom-0 left-0 w-32 h-32 bg-primary-500/5 rounded-full blur-2xl translate-y-1/2 -translate-x-1/2" />

                <div className="relative">
                  <h2 className="text-2xl font-bold text-light-900 dark:text-dark-100 mb-3">
                    {currentQuestion.title}
                  </h2>
                  <p className="text-light-600 dark:text-dark-300 mb-8">
                    {currentQuestion.description}
                  </p>

                  {/* Question Input */}
                  <div className="space-y-4">
                    {renderQuestionInput()}
                  </div>

                  {/* Navigation Buttons */}
                  <div className="flex justify-between mt-10">
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={handleBack}
                      disabled={currentStep === 0}
                      className="px-6 py-3 border border-light-300 dark:border-dark-600 rounded-xl text-light-700 dark:text-dark-300 hover:bg-light-50 dark:hover:bg-dark-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
                    >
                      Back
                    </motion.button>
                    <motion.button
                      whileHover={{ scale: 1.02 }}
                      whileTap={{ scale: 0.98 }}
                      onClick={handleNext}
                      disabled={!currentAnswer}
                      className="px-8 py-3 bg-gradient-to-r from-primary-500 to-primary-600 text-white rounded-xl hover:from-primary-600 hover:to-primary-700 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 shadow-sm hover:shadow-md"
                    >
                      {currentStep === questions.length - 1 ? 'Complete' : 'Next'}
                    </motion.button>
                  </div>
                </div>
              </motion.div>
            </AnimatePresence>
          </div>
        </main>
        <Footer />
      </div>
    </ProtectedRoute>
  );
};

export default OnboardingWizard; 