# API Configuration Guide for CareerLens

This guide explains how to configure API keys for CareerLens, similar to how you used Streamlit's `secrets.toml`.

## 🔑 Quick Start (Similar to Streamlit)

### In Streamlit (what you're used to):
```toml
# .streamlit/secrets.toml
AZURE_OPENAI_API_KEY = "your-key-here"
AZURE_OPENAI_ENDPOINT = "https://your-endpoint.openai.azure.com"
RAPIDAPI_KEY = "your-key-here"
```

### In React (what you need now):
```env
# .env file
REACT_APP_AZURE_OPENAI_API_KEY=your-key-here
REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
REACT_APP_RAPIDAPI_KEY=your-key-here
```

## 📝 Step-by-Step Setup

### 1. Create `.env` File

Create a file named `.env` in the root of your project (same level as `package.json`):

```bash
# In your terminal
touch .env
```

### 2. Add Your API Keys

Copy the example file and add your keys:

```bash
# Copy the example
cp .env.example .env

# Then edit .env with your actual keys
```

Your `.env` file should look like:

```env
# Backend API
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false

# Azure OpenAI (from your Streamlit secrets)
REACT_APP_AZURE_OPENAI_API_KEY=abc123xyz...
REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com

# RapidAPI (from your Streamlit secrets)
REACT_APP_RAPIDAPI_KEY=def456uvw...

# Backend API Key (if needed)
REACT_APP_BACKEND_API_KEY=ghi789rst...
```

### 3. Restart Your Development Server

After adding/updating `.env` file, **restart your React app**:

```bash
# Stop the server (Ctrl+C)
# Then restart
npm start
```

## 🔄 Migration from Streamlit Secrets

If you have existing Streamlit secrets, here's the mapping:

| Streamlit Secret | React Environment Variable |
|-----------------|---------------------------|
| `AZURE_OPENAI_API_KEY` | `REACT_APP_AZURE_OPENAI_API_KEY` |
| `AZURE_OPENAI_ENDPOINT` | `REACT_APP_AZURE_OPENAI_ENDPOINT` |
| `RAPIDAPI_KEY` | `REACT_APP_RAPIDAPI_KEY` |

## 📁 File Structure

```
/workspace
├── .env                    # Your API keys (DO NOT COMMIT!)
├── .env.example           # Template (safe to commit)
├── config/
│   └── api.config.js      # Configuration loader
└── services/
    └── api.js             # Uses config.apiKeys
```

## 🔒 Security Best Practices

### ✅ DO:
- ✅ Keep `.env` in `.gitignore` (already done)
- ✅ Use `.env.example` as a template (without real keys)
- ✅ Use environment variables in production
- ✅ Rotate keys regularly

### ❌ DON'T:
- ❌ Commit `.env` to git
- ❌ Share API keys in chat/email
- ❌ Hardcode keys in source code
- ❌ Use the same keys for dev and production

## 🌍 Environment-Specific Configuration

### Development (Local)
Use `.env` file:
```env
REACT_APP_USE_MOCK_API=true
REACT_APP_AZURE_OPENAI_API_KEY=dev-key-here
```

### Production (Hosting Platform)

Set environment variables in your hosting platform:

**Vercel:**
1. Go to Project Settings → Environment Variables
2. Add each variable (e.g., `REACT_APP_AZURE_OPENAI_API_KEY`)
3. Redeploy

**Netlify:**
1. Go to Site Settings → Build & Deploy → Environment
2. Add variables
3. Redeploy

**Other Platforms:**
- Check your platform's documentation for setting environment variables

## 🔍 How It Works

### 1. Configuration File (`config/api.config.js`)
```javascript
// Reads from environment variables
apiKeys: {
  azureOpenAI: {
    apiKey: process.env.REACT_APP_AZURE_OPENAI_API_KEY,
    endpoint: process.env.REACT_APP_AZURE_OPENAI_ENDPOINT,
  }
}
```

### 2. API Service (`services/api.js`)
```javascript
import config from '../config/api.config';

// Uses the config
const apiKey = config.apiKeys.azureOpenAI.apiKey;
```

### 3. Usage in Components
```javascript
// API keys are automatically included in requests
const result = await ApiService.uploadResume(file);
```

## 🧪 Testing Your Configuration

### Check if keys are loaded:
```javascript
// In browser console (after app loads)
console.log(process.env.REACT_APP_AZURE_OPENAI_API_KEY);
// Should show your key (in development)
```

### Validate configuration:
The app automatically validates on startup. Check browser console for warnings.

## 🚨 Troubleshooting

### Problem: API keys not working
**Solution:**
1. Check `.env` file exists in project root
2. Ensure variable names start with `REACT_APP_`
3. Restart development server after changes
4. Check browser console for errors

### Problem: "API key is undefined"
**Solution:**
- Make sure `.env` file is in the root directory
- Variable names must start with `REACT_APP_`
- Restart the dev server

### Problem: Keys work in Streamlit but not React
**Solution:**
- React requires `REACT_APP_` prefix
- Check you copied the keys correctly
- Ensure no extra spaces/quotes in `.env`

## 📋 Example `.env` File

```env
# ============================================
# CareerLens API Configuration
# ============================================

# Backend API
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false

# Azure OpenAI (from Streamlit secrets.toml)
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz
REACT_APP_AZURE_OPENAI_ENDPOINT=https://careerlens.openai.azure.com

# RapidAPI (from Streamlit secrets.toml)
REACT_APP_RAPIDAPI_KEY=xyz789abc123def456ghi789jkl012mno345pqr678stu901vwx234

# Backend API Key (if your backend requires it)
REACT_APP_BACKEND_API_KEY=backend-secret-key-here
```

## 🔄 Using Mock API (No Keys Needed)

If you want to test without API keys:

```env
REACT_APP_USE_MOCK_API=true
```

This uses mock data and doesn't require any API keys.

## 📞 Need Help?

1. Check browser console for errors
2. Verify `.env` file format
3. Ensure server was restarted after changes
4. Compare with `.env.example` template

---

**Remember:** Never commit your `.env` file to git! It's already in `.gitignore`.
