import React from 'react';
import { Link } from 'react-router-dom';

interface AuthLayoutProps {
  children: React.ReactNode;
  title: string;
  subtitle: string;
  footerText?: string;
  footerLink?: string;
  footerLinkText?: string;
}

const AuthLayout: React.FC<AuthLayoutProps> = ({
  children,
  title,
  subtitle,
  footerText,
  footerLink,
  footerLinkText,
}) => {
  return (
    <div className="min-h-screen flex">
      {/* Left side - Form */}
      <div className="flex-1 flex items-center justify-center px-4 sm:px-6 lg:px-8">
        <div className="max-w-md w-full space-y-8">
          <div>
            <h2 className="mt-6 text-center text-3xl font-extrabold text-gray-900">
              {title}
            </h2>
            <p className="mt-2 text-center text-sm text-gray-600">
              {subtitle}
            </p>
          </div>
          {children}
          {footerText && footerLink && footerLinkText && (
            <div className="text-center">
              <p className="text-sm text-gray-600">
                {footerText}{' '}
                <Link
                  to={footerLink}
                  className="font-medium text-primary-600 hover:text-primary-500"
                >
                  {footerLinkText}
                </Link>
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Right side - Image/Pattern */}
      <div className="hidden lg:block relative w-0 flex-1">
        <div className="absolute inset-0 bg-gradient-to-br from-primary-600 to-primary-800">
          <div className="absolute inset-0 bg-opacity-75 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxwYXRoIGQ9Ik0zNiAzNGMwLTIuMjA5IDEuNzkxLTQgNC00czQgMS43OTEgNCA0LTEuNzkxIDQtNCA0LTQtMS43OTEtNC00eiIgZmlsbD0iI2ZmZiIgZmlsbC1vcGFjaXR5PSIuMSIvPjwvZz48L3N2Zz4=')]"></div>
          <div className="absolute inset-0 flex items-center justify-center">
            <div className="text-center px-12">
              <h2 className="text-4xl font-bold text-white mb-4">
                Welcome to Admin Panel
              </h2>
              <p className="text-xl text-white text-opacity-90">
                Manage your platform with ease and efficiency
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AuthLayout; 