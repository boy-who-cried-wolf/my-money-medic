import React from 'react';
import { APP_NAME } from '../../../utils/constants';

interface LogoProps {
  className?: string;
}

const Logo: React.FC<LogoProps> = ({ className = '' }) => {
  return (
    <div className={`flex items-center space-x-2 ${className}`}>
      <div className="w-8 h-8 rounded-lg bg-primary flex items-center justify-center">
        <span className="text-xl font-bold text-white">M</span>
      </div>
      <span className="text-xl font-bold text-white">{APP_NAME}</span>
    </div>
  );
};

export default Logo; 