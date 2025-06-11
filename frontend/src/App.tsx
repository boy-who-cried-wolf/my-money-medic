import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/landing';
import SignIn from './pages/auth/SignIn';
import SignUp from './pages/auth/SignUp';
import { NotificationProvider } from './context/NotificationContext';
import { ThemeProvider } from './context/ThemeContext';
import { AuthProvider } from './context/AuthContext';
import Dashboard from './pages/dashboard/Dashboard';
import ProtectedRoute from './components/ProtectedRoute';
import OnboardingWizard from './pages/onboarding/OnboardingWizard';
import YodleeConnect from './pages/yodlee/YodleeConnect';
import SpendingAnalysis from './pages/spending/SpendingAnalysis';
import SavingsGoals from './pages/savings/SavingsGoals';
import InvestmentPortfolio from './pages/investments/InvestmentPortfolio';
import BudgetManagement from './pages/budget/BudgetManagement';
import FinancialInsights from './pages/insights/FinancialInsights';
import Recommendations from './pages/recommendations/Recommendations';

const App = () => {
  return (
    <ThemeProvider>
      <NotificationProvider>
        <Router>
          <AuthProvider>
            <Routes>
              {/* Public routes */}
              <Route path="/" element={<LandingPage />} />
              <Route path="/sign-in" element={<SignIn />} />
              <Route path="/sign-up" element={<SignUp />} />

              {/* Protected routes */}
              <Route
                path="/dashboard"
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/onboarding"
                element={
                  <ProtectedRoute>
                    <OnboardingWizard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/yodlee-connect"
                element={
                  <ProtectedRoute>
                    <YodleeConnect />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/spending"
                element={
                  <ProtectedRoute>
                    <SpendingAnalysis />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/savings"
                element={
                  <ProtectedRoute>
                    <SavingsGoals />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/investments"
                element={
                  <ProtectedRoute>
                    <InvestmentPortfolio />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/budget"
                element={
                  <ProtectedRoute>
                    <BudgetManagement />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/insights"
                element={
                  <ProtectedRoute>
                    <FinancialInsights />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/recommendations"
                element={
                  <ProtectedRoute>
                    <Recommendations />
                  </ProtectedRoute>
                }
              />

              {/* Catch all route - redirect to home */}
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </AuthProvider>
        </Router>
      </NotificationProvider>
    </ThemeProvider>
  );
};

export default App;
