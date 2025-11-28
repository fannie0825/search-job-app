# CareerLens Dashboard - Implementation Guide

This guide covers the enhanced features implemented in the CareerLens dashboard.

## ✅ Implemented Features

### 1. **API Integration** (`services/api.js`)
- Complete API service layer for backend communication
- Automatic fallback to mock API for development
- Methods for:
  - Resume upload
  - Profile extraction
  - Market positioning analysis
  - Job matching
  - Tailored resume generation

**Usage:**
```jsx
import ApiService from './services/api';

// Upload resume
const result = await ApiService.uploadResume(file);

// Get job matches
const matches = await ApiService.getJobMatches(profileData, filters);
```

### 2. **Toast Notifications** (`hooks/useToast.js`, `components/Toast.jsx`)
- Custom toast notification system
- Four types: success, error, warning, info
- Auto-dismiss after 3 seconds
- Slide-in animations

**Usage:**
```jsx
import { useToast } from './hooks/useToast';

const { success, error, warning, info } = useToast();

success('Resume uploaded successfully!');
error('Upload failed. Please try again.');
```

### 3. **File Upload** (`hooks/useFileUpload.js`)
- Complete file upload handling
- File validation (type, size)
- Upload progress tracking
- Error handling
- Profile extraction after upload

**Features:**
- Accepts PDF and DOCX files
- Max file size: 10MB
- Progress indicator
- Success/error callbacks

### 4. **Loading States** (`components/LoadingSpinner.jsx`)
- Loading spinner component
- Loading overlay for full-screen operations
- Loading button states
- Multiple sizes (sm, default, lg, xl)

**Usage:**
```jsx
import { LoadingSpinner, LoadingOverlay, LoadingButton } from './components/LoadingSpinner';

<LoadingSpinner size="lg" />
<LoadingOverlay message="Processing..." />
<LoadingButton loading={isLoading}>Submit</LoadingButton>
```

### 5. **Data Persistence** (`hooks/useLocalStorage.js`)
- React hook for localStorage
- Automatic state synchronization
- Type-safe storage

**Usage:**
```jsx
import { useLocalStorage } from './hooks/useLocalStorage';

const [filters, setFilters] = useLocalStorage('careerlens_filters', []);
```

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=true
```

- **REACT_APP_API_URL**: Your backend API endpoint
- **REACT_APP_USE_MOCK_API**: Set to `false` when using real API

### Mock API Mode

By default, the app uses mock API for development. The mock API:
- Simulates network delays
- Returns realistic mock data
- Allows testing without backend

To use real API:
1. Set `REACT_APP_USE_MOCK_API=false`
2. Set `REACT_APP_API_URL` to your backend endpoint
3. Ensure backend matches API contract

## 📁 File Structure

```
/workspace
├── services/
│   ├── api.js              # Main API service
│   └── mockApi.js          # Mock API for development
├── hooks/
│   ├── useToast.js         # Toast notification hook
│   ├── useFileUpload.js    # File upload hook
│   └── useLocalStorage.js  # localStorage hook
├── components/
│   ├── Toast.jsx           # Toast notification component
│   ├── LoadingSpinner.jsx # Loading indicators
│   ├── Sidebar.jsx         # Enhanced with upload & persistence
│   ├── JobMatchTable.jsx   # Enhanced with loading & API
│   └── DashboardLayout.jsx # Enhanced with state management
└── .env.example            # Environment variables template
```

## 🚀 Usage Examples

### Complete Dashboard with All Features

```jsx
import DashboardLayout from './components/DashboardLayout';
import './globals.css';

function App() {
  return <DashboardLayout />;
}
```

The dashboard now includes:
- ✅ File upload with progress
- ✅ Toast notifications
- ✅ Loading states
- ✅ Data persistence
- ✅ API integration (with mock fallback)

### Custom API Integration

```jsx
import ApiService from './services/api';

// In your component
const handleAnalyze = async () => {
  try {
    const positioning = await ApiService.getMarketPositioning(profile, filters);
    setMarketData(positioning);
  } catch (error) {
    toast.error(error.message);
  }
};
```

## 🔄 Data Flow

1. **User uploads resume** → `useFileUpload` hook → API service → Toast notification
2. **User clicks "Analyze"** → API service → Loading overlay → Market positioning + Job matches
3. **User clicks "Tailor Resume"** → API service → Loading → Toast notification → Download

## 🎨 Enhanced Components

### Sidebar
- ✅ File upload with progress
- ✅ Persistent filters (localStorage)
- ✅ Upload success indicator
- ✅ Disabled states

### JobMatchTable
- ✅ Loading state
- ✅ Empty state
- ✅ API-driven data
- ✅ Error handling

### MarketPositionCards
- ✅ Loading state
- ✅ API-driven data
- ✅ Fallback to mock data

## 🧪 Testing

### Mock API Testing
1. Ensure `REACT_APP_USE_MOCK_API=true`
2. Upload a file → See mock upload
3. Click "Analyze" → See mock data after delay
4. Click "Tailor Resume" → See mock generation

### Real API Testing
1. Set `REACT_APP_USE_MOCK_API=false`
2. Set `REACT_APP_API_URL` to your backend
3. Ensure backend implements the API contract
4. Test all flows

## 📝 API Contract

Your backend should implement these endpoints:

```
POST /api/resume/upload
POST /api/resume/:id/extract
POST /api/analyze
POST /api/jobs/matches
POST /api/resume/tailor
POST /api/market/positioning
```

See `services/api.js` for request/response formats.

## 🐛 Error Handling

All API calls include error handling:
- Network errors → Toast error notification
- Validation errors → Toast warning
- Success → Toast success
- Loading states prevent duplicate requests

## 🔐 Best Practices

1. **Always use hooks** for state management
2. **Show loading states** for async operations
3. **Display toast notifications** for user feedback
4. **Persist user preferences** in localStorage
5. **Handle errors gracefully** with user-friendly messages

## 📚 Next Steps

1. **Connect to real backend** - Update API service
2. **Add authentication** - Implement user login
3. **Add error boundaries** - Catch React errors
4. **Add unit tests** - Test hooks and components
5. **Add E2E tests** - Test complete user flows
