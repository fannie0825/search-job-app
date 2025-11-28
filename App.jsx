import React, { useState, useEffect } from 'react';
import DashboardLayout from './components/DashboardLayout';
import './globals.css';

function App() {
  const [darkMode, setDarkMode] = useState(false);

  useEffect(() => {
    // Check for saved theme preference or default to light mode
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    
    if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
      setDarkMode(true);
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, []);

  const toggleDarkMode = () => {
    const newDarkMode = !darkMode;
    setDarkMode(newDarkMode);
    
    if (newDarkMode) {
      document.documentElement.classList.add('dark');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark');
      localStorage.setItem('theme', 'light');
    }
  };

  return (
    <div className={darkMode ? 'dark' : ''}>
      <DashboardLayout />
      
      {/* Dark Mode Toggle Button (optional, can be moved to header) */}
      <button
        onClick={toggleDarkMode}
        className="fixed bottom-4 right-4 p-3 bg-accent text-white rounded-full shadow-lg hover:bg-accent-dark transition-colors z-50"
        aria-label="Toggle dark mode"
      >
        {darkMode ? '☀️' : '🌙'}
      </button>
    </div>
  );
}

export default App;
