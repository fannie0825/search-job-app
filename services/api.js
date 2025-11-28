/**
 * API Service for CareerLens
 * Handles all API calls to backend services
 */

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';
const USE_MOCK_API = process.env.REACT_APP_USE_MOCK_API === 'true' || !process.env.REACT_APP_API_URL;

// Import mock API for development
let mockApiService = null;
if (USE_MOCK_API) {
  import('./mockApi').then(module => {
    mockApiService = module.default;
  });
}

class ApiService {
  // Use mock API if enabled or if API URL is not set
  _useMock() {
    return USE_MOCK_API && mockApiService;
  }
  /**
   * Upload resume file
   */
  async uploadResume(file) {
    if (this._useMock()) {
      return mockApiService.uploadResume(file);
    }
    const formData = new FormData();
    formData.append('resume', file);

    const response = await fetch(`${API_BASE_URL}/resume/upload`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      throw new Error(`Upload failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Extract profile from resume
   */
  async extractProfile(resumeId) {
    if (this._useMock()) {
      return mockApiService.extractProfile(resumeId);
    }
    const response = await fetch(`${API_BASE_URL}/resume/${resumeId}/extract`, {
      method: 'POST',
    });

    if (!response.ok) {
      throw new Error(`Profile extraction failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Analyze profile and get market positioning
   */
  async analyzeProfile(profileData, filters) {
    if (this._useMock()) {
      return mockApiService.analyzeProfile(profileData, filters);
    }
    const response = await fetch(`${API_BASE_URL}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        profile: profileData,
        filters: filters,
      }),
    });

    if (!response.ok) {
      throw new Error(`Analysis failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get job matches
   */
  async getJobMatches(profileData, filters, topK = 15) {
    if (this._useMock()) {
      return mockApiService.getJobMatches(profileData, filters);
    }
    const response = await fetch(`${API_BASE_URL}/jobs/matches`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        profile: profileData,
        filters: filters,
        top_k: topK,
      }),
    });

    if (!response.ok) {
      throw new Error(`Job matching failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Generate tailored resume
   */
  async generateTailoredResume(profileData, jobId) {
    if (this._useMock()) {
      return mockApiService.generateTailoredResume(profileData, jobId);
    }
    const response = await fetch(`${API_BASE_URL}/resume/tailor`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        profile: profileData,
        job_id: jobId,
      }),
    });

    if (!response.ok) {
      throw new Error(`Resume generation failed: ${response.statusText}`);
    }

    return response.json();
  }

  /**
   * Get market positioning metrics
   */
  async getMarketPositioning(profileData, filters) {
    if (this._useMock()) {
      return mockApiService.getMarketPositioning(profileData, filters);
    }
    const response = await fetch(`${API_BASE_URL}/market/positioning`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        profile: profileData,
        filters: filters,
      }),
    });

    if (!response.ok) {
      throw new Error(`Market positioning failed: ${response.statusText}`);
    }

    return response.json();
  }
}

export default new ApiService();
