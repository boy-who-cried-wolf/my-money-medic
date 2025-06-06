import { createBrowserRouter } from 'react-router-dom';
import LandingPage from './pages/landing/LandingPage';
import SignIn from './pages/auth/SignIn';
import SignUp from './pages/auth/SignUp';
import Dashboard from './pages/dashboard/Dashboard';
import OnboardingWizard from './pages/onboarding/OnboardingWizard';
import ProtectedRoute from './components/ProtectedRoute';

export const router = createBrowserRouter([
  {
    path: '/',
    element: <LandingPage />,
  },
  {
    path: '/sign-in',
    element: <SignIn />,
  },
  {
    path: '/sign-up',
    element: <SignUp />,
  },
  {
    path: '/onboarding',
    element: <OnboardingWizard />,
  },
  {
    path: '/dashboard',
    element: <Dashboard />,
  },
]); 