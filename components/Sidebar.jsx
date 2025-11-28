import React, { useState } from 'react';
import { Upload, X, Menu } from 'lucide-react';
import Logo from './Logo';

const Sidebar = ({ isOpen, onClose, isMobile }) => {
  const [targetIndustries, setTargetIndustries] = useState(['FinTech']);
  const [minSalary, setMinSalary] = useState(4000);
  const [maxSalary, setMaxSalary] = useState(90000);

  const handleFileUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      console.log('File uploaded:', file.name);
      // Handle file upload logic here
    }
  };

  const removeIndustry = (industry) => {
    setTargetIndustries(targetIndustries.filter(i => i !== industry));
  };

  const addIndustry = (e) => {
    if (e.key === 'Enter' && e.target.value.trim()) {
      setTargetIndustries([...targetIndustries, e.target.value.trim()]);
      e.target.value = '';
    }
  };

  const sidebarContent = (
    <div className="h-full flex flex-col bg-bg-sidebar text-white">
      {/* Header with Logo */}
      <div className="p-6 border-b border-navy-light">
        <div className="flex items-center justify-between">
          <div className="text-white">
            <Logo variant="full" size="default" darkMode={true} />
          </div>
          {isMobile && (
            <button
              onClick={onClose}
              className="p-2 hover:bg-navy-light rounded-lg transition-colors"
              aria-label="Close sidebar"
            >
              <X className="w-5 h-5" />
            </button>
          )}
        </div>
      </div>

      {/* Scrollable Content */}
      <div className="flex-1 overflow-y-auto scrollbar-thin p-6 space-y-6">
        {/* Upload Section */}
        <div>
          <h3 className="text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wide">
            Upload Resume
          </h3>
          <label className="block">
            <input
              type="file"
              accept=".pdf,.docx"
              onChange={handleFileUpload}
              className="hidden"
            />
            <div className="border-2 border-dashed border-navy-light rounded-lg p-6 text-center cursor-pointer hover:border-accent transition-colors group">
              <Upload className="w-8 h-8 mx-auto mb-2 text-gray-400 group-hover:text-accent transition-colors" />
              <p className="text-sm text-gray-300 mb-1">PDF or DOCX</p>
              <p className="text-xs text-gray-400">Click to upload or drag and drop</p>
            </div>
          </label>
        </div>

        {/* Filters Section */}
        <div className="space-y-6">
          {/* Target Industries */}
          <div>
            <label className="block text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wide">
              Target Industries
            </label>
            <div className="space-y-2">
              <input
                type="text"
                placeholder="Type and press Enter..."
                onKeyPress={addIndustry}
                className="w-full px-4 py-2 bg-navy-light border border-navy rounded-lg text-white placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-accent"
              />
              <div className="flex flex-wrap gap-2 mt-2">
                {targetIndustries.map((industry, index) => (
                  <span
                    key={index}
                    className="inline-flex items-center gap-1 px-3 py-1 bg-accent text-white rounded-full text-sm"
                  >
                    {industry}
                    <button
                      onClick={() => removeIndustry(industry)}
                      className="hover:text-gray-200"
                      aria-label={`Remove ${industry}`}
                    >
                      <X className="w-3 h-3" />
                    </button>
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Salary Range */}
          <div>
            <label className="block text-sm font-semibold text-gray-300 mb-3 uppercase tracking-wide">
              Min. Salary (HK$)
            </label>
            <div className="space-y-3">
              <div className="flex justify-between text-sm text-white mb-2 font-medium">
                <span>HK${(minSalary / 1000).toFixed(0)}k</span>
                <span className="text-gray-400">Max: HK${(maxSalary / 1000).toFixed(0)}k</span>
              </div>
              <div className="relative">
                <input
                  type="range"
                  min="4000"
                  max="90000"
                  step="1000"
                  value={minSalary}
                  onChange={(e) => {
                    const newMin = Number(e.target.value);
                    if (newMin <= maxSalary) {
                      setMinSalary(newMin);
                    }
                  }}
                  className="w-full h-2 bg-navy-light rounded-lg appearance-none cursor-pointer accent-accent"
                  style={{
                    background: `linear-gradient(to right, #3B82F6 0%, #3B82F6 ${((minSalary - 4000) / (90000 - 4000)) * 100}%, #2C3E50 ${((minSalary - 4000) / (90000 - 4000)) * 100}%, #2C3E50 100%)`
                  }}
                />
              </div>
              <div className="flex justify-between text-xs text-gray-400">
                <span>HK$4k</span>
                <span>HK$90k</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Primary Action Button */}
      <div className="p-6 border-t border-navy-light">
        <button
          onClick={() => {
            console.log('Analyze & Benchmark clicked');
            // Handle analyze action
          }}
          className="w-full bg-accent hover:bg-accent-dark text-white font-semibold py-3 px-4 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl transform hover:-translate-y-0.5"
        >
          Analyze & Benchmark
        </button>
      </div>
    </div>
  );

  if (isMobile) {
    return (
      <>
        {/* Mobile Overlay */}
        {isOpen && (
          <div
            className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
            onClick={onClose}
          />
        )}
        {/* Mobile Sidebar */}
        <div
          className={`fixed top-0 left-0 h-full w-64 z-50 transform transition-transform duration-300 ease-in-out lg:hidden ${
            isOpen ? 'translate-x-0' : '-translate-x-full'
          }`}
        >
          {sidebarContent}
        </div>
      </>
    );
  }

  // Desktop Sidebar
  return (
    <aside className="hidden lg:flex lg:w-64 lg:flex-shrink-0">
      {sidebarContent}
    </aside>
  );
};

export default Sidebar;
