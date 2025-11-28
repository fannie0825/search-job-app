import React from 'react';

/**
 * CareerLens Logo Component
 * "Focus Aperture" design - A stylized camera aperture forming a "C" shape
 * Represents clarity, focus, and AI "zooming in" on the right opportunities
 */

const Logo = ({ 
  variant = 'full', // 'full', 'icon', 'text'
  size = 'default', // 'sm', 'default', 'lg', 'xl'
  className = '',
  darkMode = false 
}) => {
  const sizeClasses = {
    sm: { icon: 'w-6 h-6', text: 'text-lg', container: 'gap-2' },
    default: { icon: 'w-8 h-8', text: 'text-xl', container: 'gap-2' },
    lg: { icon: 'w-12 h-12', text: 'text-2xl', container: 'gap-3' },
    xl: { icon: 'w-16 h-16', text: 'text-3xl', container: 'gap-4' },
  };

  const currentSize = sizeClasses[size] || sizeClasses.default;

  const ApertureIcon = () => (
    <svg 
      className={currentSize.icon}
      viewBox="0 0 200 200" 
      fill="none" 
      xmlns="http://www.w3.org/2000/svg"
      aria-label="CareerLens Logo"
    >
      <defs>
        <linearGradient id="apertureGradient" x1="0%" y1="0%" x2="100%" y2="100%">
          <stop offset="0%" style={{stopColor: darkMode ? '#60A5FA' : '#3B82F6', stopOpacity: 1}} />
          <stop offset="100%" style={{stopColor: darkMode ? '#3B82F6' : '#2563EB', stopOpacity: 1}} />
        </linearGradient>
      </defs>
      
      {/* Outer ring for depth */}
      <circle 
        cx="100" 
        cy="100" 
        r="90" 
        fill="none" 
        stroke={darkMode ? '#60A5FA' : '#3B82F6'} 
        strokeWidth="2" 
        opacity="0.3"
      />
      
      {/* Aperture blades forming "C" shape */}
      <path 
        d="M 100 10 Q 150 10 180 60 L 170 70 Q 140 30 100 30 Z" 
        fill="url(#apertureGradient)" 
        opacity="0.9"
      />
      <path 
        d="M 180 60 Q 190 100 180 140 L 170 130 Q 175 100 170 70 Z" 
        fill="url(#apertureGradient)" 
        opacity="0.85"
      />
      <path 
        d="M 180 140 Q 150 190 100 190 L 100 180 Q 140 180 170 130 Z" 
        fill="url(#apertureGradient)" 
        opacity="0.9"
      />
      <path 
        d="M 100 190 Q 50 190 20 140 L 30 130 Q 60 180 100 180 Z" 
        fill="url(#apertureGradient)" 
        opacity="0.7"
      />
      <path 
        d="M 20 140 Q 10 100 20 60 L 30 70 Q 25 100 30 130 Z" 
        fill="url(#apertureGradient)" 
        opacity="0.6"
      />
      
      {/* Inner lens circle */}
      <circle 
        cx="100" 
        cy="100" 
        r="35" 
        fill="url(#apertureGradient)" 
        opacity="0.2"
      />
      <circle 
        cx="100" 
        cy="100" 
        r="30" 
        fill="none" 
        stroke={darkMode ? '#60A5FA' : '#3B82F6'} 
        strokeWidth="1.5" 
        opacity="0.5"
      />
      
      {/* Center focus point */}
      <circle 
        cx="100" 
        cy="100" 
        r="8" 
        fill="url(#apertureGradient)"
      />
      <circle 
        cx="100" 
        cy="100" 
        r="4" 
        fill="#FFFFFF"
      />
    </svg>
  );

  if (variant === 'icon') {
    return (
      <div className={`inline-flex items-center ${className}`}>
        <ApertureIcon />
      </div>
    );
  }

  if (variant === 'text') {
    return (
      <div className={`inline-flex items-center ${currentSize.container} ${className}`}>
        <span className={`font-bold ${currentSize.text} text-text-heading dark:text-dark-text-primary`}>
          CareerLens
        </span>
      </div>
    );
  }

  // Full logo (icon + text)
  return (
    <div className={`inline-flex items-center ${currentSize.container} ${className}`}>
      <ApertureIcon />
      <span className={`font-bold ${currentSize.text} text-text-heading dark:text-dark-text-primary`}>
        CareerLens
      </span>
    </div>
  );
};

export default Logo;
