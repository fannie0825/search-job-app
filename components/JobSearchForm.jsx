import React from 'react';
import { useLocalStorage } from '../hooks/useLocalStorage';

const COUNTRY_OPTIONS = [
  { value: 'hk', label: 'hk' },
  { value: 'sg', label: 'sg' },
  { value: 'us', label: 'us' },
  { value: 'uk', label: 'uk' },
  { value: 'au', label: 'au' },
  { value: 'ca', label: 'ca' },
  { value: 'jp', label: 'jp' },
  { value: 'cn', label: 'cn' },
];

const JobSearchForm = ({ onSearch, loading = false }) => {
  const [jobKeywords, setJobKeywords] = useLocalStorage('careerlens_job_keywords', '');
  const [cityRegion, setCityRegion] = useLocalStorage('careerlens_city_region', 'Hong Kong');
  const [countryCode, setCountryCode] = useLocalStorage('careerlens_country_code', 'hk');

  const handleSearch = () => {
    if (onSearch) {
      onSearch({
        keywords: jobKeywords,
        location: cityRegion,
        country: countryCode,
      });
    }
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 shadow-sm">
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Job Keywords Field */}
        <div className="flex flex-col">
          <label 
            htmlFor="job-keywords" 
            className="text-sm font-medium text-gray-600 mb-2"
          >
            Job Keywords<span className="text-red-500">*</span>
          </label>
          <input
            id="job-keywords"
            type="text"
            value={jobKeywords}
            onChange={(e) => setJobKeywords(e.target.value)}
            placeholder="e.g., Project Manager"
            className="w-full px-4 py-2.5 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            disabled={loading}
          />
        </div>

        {/* City/Region Field */}
        <div className="flex flex-col">
          <label 
            htmlFor="city-region" 
            className="text-sm font-medium text-gray-600 mb-2"
          >
            City/Region
          </label>
          <input
            id="city-region"
            type="text"
            value={cityRegion}
            onChange={(e) => setCityRegion(e.target.value)}
            placeholder="Hong Kong"
            className="w-full px-4 py-2.5 bg-white border border-gray-300 rounded-lg text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
            disabled={loading}
          />
        </div>

        {/* Country Code Field */}
        <div className="flex flex-col">
          <label 
            htmlFor="country-code" 
            className="text-sm font-medium text-gray-600 mb-2"
          >
            Country Code
          </label>
          <div className="relative">
            <select
              id="country-code"
              value={countryCode}
              onChange={(e) => setCountryCode(e.target.value)}
              className="w-full px-4 py-2.5 bg-white border border-gray-300 rounded-lg text-gray-900 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all appearance-none cursor-pointer"
              disabled={loading}
            >
              {COUNTRY_OPTIONS.map((option) => (
                <option key={option.value} value={option.value}>
                  {option.label}
                </option>
              ))}
            </select>
            <div className="pointer-events-none absolute inset-y-0 right-0 flex items-center px-3 text-gray-500">
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
              </svg>
            </div>
          </div>
        </div>
      </div>

      {/* Search Button */}
      <div className="mt-6 flex justify-end">
        <button
          onClick={handleSearch}
          disabled={loading || !jobKeywords.trim()}
          className={`px-6 py-2.5 bg-blue-600 text-white font-medium rounded-lg transition-all ${
            loading || !jobKeywords.trim()
              ? 'opacity-50 cursor-not-allowed'
              : 'hover:bg-blue-700 active:bg-blue-800'
          }`}
        >
          {loading ? 'Searching...' : 'Search Jobs'}
        </button>
      </div>
    </div>
  );
};

export default JobSearchForm;
