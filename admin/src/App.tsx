import React from 'react';
import { Navigate, Route, BrowserRouter as Router, Routes } from 'react-router-dom';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedLayout from './layouts/ProtectedLayout';
import PublicLayout from './layouts/PublicLayout';
import Analytics from './pages/Analytics';
import Brokers from './pages/Brokers';
import Dashboard from './pages/Dashboard';
import Login from './pages/Login';
import Settings from './pages/Settings';
import Users from './pages/users/Users';
import apiService from './services/api.service';

const App: React.FC = () => {
  const adminPrefix = apiService.getAdminPrefix();

  return (
    <AuthProvider>
      <Router basename={adminPrefix}>
        <Routes>
          {/* Public routes */}
          <Route element={<PublicLayout />}>
            <Route path="/login" element={<Login />} />
            {/* <Route path="/register" element={<Register />} /> */}
          </Route>

          {/* Protected routes */}
          <Route element={<ProtectedLayout />}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/users/*" element={<Users />} />
            <Route path="/analytics" element={<Analytics />} />
            {/* Temporarily disabled broker routes
            <Route path="/brokers" element={<Brokers />} />
            <Route path="/brokers/new" element={<BrokerForm />} />
            */}
            <Route path="/settings" element={<Settings />} />
          </Route>

          {/* Redirect root to dashboard */}
          <Route path="/" element={<Navigate to="/dashboard" replace />} />

          {/* Catch all route */}
          <Route path="*" element={<Navigate to="/dashboard" replace />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;
