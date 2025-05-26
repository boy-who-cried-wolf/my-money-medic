import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { Button, Input } from '../common';
import { APP_NAME } from '../../utils/constants';

const AuthForm: React.FC = () => {
  const [isSignIn, setIsSignIn] = useState(true);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    // TODO: Implement authentication logic
    setTimeout(() => setIsLoading(false), 1000);
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
      className="w-full max-w-md mx-auto"
    >
      <div className="text-center mb-8">
        <h2 className="text-3xl font-bold text-white mb-2">
          {isSignIn ? 'Welcome Back' : 'Create Account'}
        </h2>
        <p className="text-gray-400">
          {isSignIn
            ? 'Sign in to continue to your account'
            : 'Join us to start your financial journey'}
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {!isSignIn && (
          <Input
            label="Full Name"
            type="text"
            placeholder="John Doe"
            required
          />
        )}
        <Input
          label="Email"
          type="email"
          placeholder="you@example.com"
          required
        />
        <Input
          label="Password"
          type="password"
          placeholder="••••••••"
          required
        />
        {!isSignIn && (
          <Input
            label="Confirm Password"
            type="password"
            placeholder="••••••••"
            required
          />
        )}

        <Button
          type="submit"
          variant="primary"
          fullWidth
          isLoading={isLoading}
        >
          {isSignIn ? 'Sign In' : 'Create Account'}
        </Button>

        <div className="text-center">
          <button
            type="button"
            onClick={() => setIsSignIn(!isSignIn)}
            className="text-primary hover:text-primary-light transition-colors"
          >
            {isSignIn
              ? "Don't have an account? Sign up"
              : 'Already have an account? Sign in'}
          </button>
        </div>
      </form>
    </motion.div>
  );
};

export default AuthForm; 