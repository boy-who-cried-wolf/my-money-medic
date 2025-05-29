import React from 'react';

interface DividerProps {
  variant?: 'down' | 'up' | 'wave';
  fromColor?: string;
  toColor?: string;
}

const defaultFrom = 'from-light-100 dark:from-dark-800';
const defaultTo = 'to-transparent';
const defaultFill = '#00AFFF';

const Divider: React.FC<DividerProps> = ({
  variant = 'down',
  fromColor = defaultFrom,
  toColor = defaultTo,
}) => {
  // Smoother SVG paths for each variant
  const paths = {
    down: 'M0,40 C360,120 1080,-40 1440,40 L1440,120 L0,120 Z',
    up: 'M0,80 C360,0 1080,160 1440,80 L1440,0 L0,0 Z',
    wave: 'M0,60 Q360,100 720,60 T1440,60 L1440,120 L0,120 Z',
  };
  return (
    <div className={`relative h-24 overflow-hidden`}>
      <div className={`absolute inset-0 bg-gradient-to-b ${fromColor} ${toColor}`} />
      <svg
        className="absolute bottom-0 w-full"
        viewBox="0 0 1440 120"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d={paths[variant]}
          fill={defaultFill}
          fillOpacity="0.12"
        />
      </svg>
    </div>
  );
};

export default Divider; 