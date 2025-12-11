/**
 * Indeed Job Scraper API Service
 * Direct integration with RapidAPI Indeed Scraper
 * 
 * This service calls the Indeed Scraper API directly from the frontend
 * when a backend is not available.
 */

import config from '../config/api.config';

const INDEED_API_URL = 'https://indeed-scraper-api.p.rapidapi.com/api/job';

class IndeedApiService {
  constructor() {
    this.apiKey = config.apiKeys.rapidAPI.apiKey;
  }

  /**
   * Check if API key is configured
   */
  isConfigured() {
    return Boolean(this.apiKey);
  }

  /**
   * Fetch jobs from Indeed API
   * @param {Object} params - Search parameters
   * @param {string} params.keywords - Job search keywords (required)
   * @param {string} params.location - City/Region (default: "Hong Kong")
   * @param {string} params.country - Country code (default: "hk")
   * @param {string} params.jobType - Job type: fulltime, parttime, contract, internship
   * @param {number} params.numJobs - Number of jobs to fetch (max 50)
   * @returns {Promise<Array>} Array of job objects
   */
  async fetchJobs({
    keywords = '',
    location = 'Hong Kong',
    country = 'hk',
    jobType = 'fulltime',
    numJobs = 25,
  }) {
    if (!this.apiKey) {
      throw new Error('RapidAPI key not configured. Please set REACT_APP_RAPIDAPI_KEY in your environment.');
    }

    if (!keywords.trim()) {
      throw new Error('Job keywords are required');
    }

    const payload = {
      scraper: {
        maxRows: Math.min(numJobs, 50),
        query: keywords,
        location: location,
        jobType: jobType,
        radius: '50',
        sort: 'relevance',
        fromDays: '7',
        country: country,
      },
    };

    const headers = {
      'Content-Type': 'application/json',
      'x-rapidapi-host': 'indeed-scraper-api.p.rapidapi.com',
      'x-rapidapi-key': this.apiKey,
    };

    try {
      console.log('Fetching jobs with params:', payload);
      
      const response = await fetch(INDEED_API_URL, {
        method: 'POST',
        headers,
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        if (response.status === 429) {
          throw new Error('Rate limit exceeded. Please wait a few minutes and try again.');
        }
        if (response.status === 401 || response.status === 403) {
          throw new Error('Invalid API key. Please check your RapidAPI key configuration.');
        }
        const errorText = await response.text();
        throw new Error(`API Error: ${response.status} - ${errorText.slice(0, 200)}`);
      }

      const data = await response.json();
      console.log('API Response:', data);

      // Parse the response
      if (data.returnvalue && data.returnvalue.data) {
        return data.returnvalue.data.map((job) => this._parseJob(job));
      }

      return [];
    } catch (error) {
      console.error('Indeed API Error:', error);
      throw error;
    }
  }

  /**
   * Parse job data from API response
   * @private
   */
  _parseJob(jobData) {
    const locationData = jobData.location || {};
    const city = locationData.city || 'Not specified';
    
    const jobTypes = jobData.jobType || [];
    const jobType = jobTypes.length > 0 ? jobTypes.join(', ') : 'Full-time';
    
    const benefits = jobData.benefits || [];
    const attributes = jobData.attributes || [];
    
    const description = jobData.descriptionText || 'No description available';

    return {
      id: jobData.jobId || `job_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      title: jobData.title || 'N/A',
      company: jobData.companyName || 'N/A',
      location: city,
      description: description.slice(0, 50000),
      salary: 'Not specified',
      jobType: jobType,
      jobUrl: jobData.jobUrl || '#',
      postedDate: jobData.age || 'Recently',
      benefits: benefits.slice(0, 5),
      skills: attributes.slice(0, 10),
      companyRating: jobData.rating?.rating || 0,
      isRemote: jobData.isRemote || false,
    };
  }
}

export default new IndeedApiService();
