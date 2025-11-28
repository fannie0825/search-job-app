import React, { useState, useEffect } from 'react';
import { Menu } from 'lucide-react';
import Sidebar from './Sidebar';
import MarketPositionCards from './MarketPositionCards';
import JobMatchTable from './JobMatchTable';
import ToastContainer from './Toast';
import LoadingOverlay from './LoadingSpinner';
import { useToast } from '../hooks/useToast';
import ApiService from '../services/api';

const DashboardLayout = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [isMobile, setIsMobile] = useState(false);
  const [loading, setLoading] = useState(false);
  const [profileData, setProfileData] = useState(null);
  const [marketPositioning, setMarketPositioning] = useState(null);
  const [jobMatches, setJobMatches] = useState(null);
  const { toasts, removeToast, success, error, warning, info } = useToast();

  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 1024); // lg breakpoint
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  const handleFileUploaded = async (fileResult, profile) => {
    if (profile) {
      setProfileData(profile);
      success('Profile extracted from resume successfully!');
    }
  };

  const handleAnalyze = async (filters) => {
    if (!profileData) {
      warning('Please upload a resume first');
      return;
    }

    setLoading(true);
    try {
      // Get market positioning
      const positioning = await ApiService.getMarketPositioning(profileData, filters);
      setMarketPositioning(positioning);

      // Get job matches
      const matches = await ApiService.getJobMatches(profileData, filters);
      setJobMatches(matches.jobs || matches);

      success('Analysis complete! Your market positioning and job matches are ready.');
    } catch (err) {
      console.error('Analysis error:', err);
      error(err.message || 'Analysis failed. Please try again.');
      
      // Fallback to mock data on error
      setMarketPositioning(null);
      setJobMatches(null);
    } finally {
      setLoading(false);
    }
  };

  const handleTailorResume = async (job) => {
    if (!profileData) {
      warning('Please upload a resume first');
      return;
    }

    setLoading(true);
    try {
      const result = await ApiService.generateTailoredResume(profileData, job.id);
      success(`Tailored resume generated for ${job.jobTitle}!`);
      
      // Handle resume download or display
      if (result.downloadUrl) {
        window.open(result.downloadUrl, '_blank');
      }
    } catch (err) {
      console.error('Resume generation error:', err);
      error(err.message || 'Failed to generate tailored resume. Please try again.');
    } finally {
      setLoading(false);
    }
  };

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
          onFileUploaded={handleFileUploaded}
          onAnalyze={handleAnalyze}
          toast={{ success, error, warning, info }}
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
            <MarketPositionCards data={marketPositioning} />

            {/* Job Matches Table */}
            <JobMatchTable
              jobs={jobMatches}
              loading={loading}
              onTailorResume={handleTailorResume}
              toast={{ success, error, warning, info }}
            />
          </div>
        </main>
      </div>

      {/* Toast Notifications */}
      <ToastContainer toasts={toasts} onRemove={removeToast} />

      {/* Loading Overlay */}
      {loading && <LoadingOverlay message="Analyzing your profile..." />}
    </div>
  );
};

export default DashboardLayout;
