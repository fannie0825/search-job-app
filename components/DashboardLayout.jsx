import React, { useState, useEffect } from 'react';
import { Menu } from 'lucide-react';
import Sidebar from './Sidebar';
import MarketPositionCards from './MarketPositionCards';
import JobMatchTable from './JobMatchTable';

const DashboardLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 1024); // lg breakpoint
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  return (
    <div className="min-h-screen bg-bg-main dark:bg-dark-bg-main">
      {/* Mobile Header */}
      {isMobile && (
        <header className="lg:hidden fixed top-0 left-0 right-0 z-30 bg-bg-sidebar text-white p-4 flex items-center justify-between shadow-lg">
          <h1 className="text-lg font-bold">CareerLens</h1>
          <button
            onClick={() => setSidebarOpen(!sidebarOpen)}
            className="p-2 hover:bg-navy-light rounded-lg transition-colors"
            aria-label="Toggle sidebar"
          >
            <Menu className="w-6 h-6" />
          </button>
        </header>
      )}

      <div className="flex h-screen overflow-hidden">
        {/* Sidebar */}
        <Sidebar
          isOpen={sidebarOpen}
          onClose={() => setSidebarOpen(false)}
          isMobile={isMobile}
        />

        {/* Main Content Area */}
        <main className={`flex-1 overflow-y-auto scrollbar-thin ${
          isMobile ? 'pt-16' : ''
        }`}>
          <div className="max-w-7xl mx-auto p-6 lg:p-8">
            {/* Header */}
            <div className="mb-8">
              <h1 className="text-3xl font-bold text-text-heading dark:text-dark-text-primary mb-2">
                Market Positioning & Smart Matches
              </h1>
              <p className="text-text-muted dark:text-dark-text-secondary">
                AI-powered career insights for the Hong Kong market
              </p>
            </div>

            {/* Market Positioning Cards */}
            <MarketPositionCards />

            {/* Job Matches Table */}
            <JobMatchTable />
          </div>
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
