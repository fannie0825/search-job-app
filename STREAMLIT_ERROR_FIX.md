# Streamlit Console Errors - Fix Guide

## Errors Identified

1. **503/404 errors for `/_stcore/health` and `/_stcore/host-config`**
   - These are Streamlit internal endpoints that should be automatically available
   - 503 = Service Unavailable (server issue)
   - 404 = Not Found (endpoint not available)

2. **WebSocket connection failures**
   - `wss://search-job-app.streamlit.app/~/logstream` failing
   - Related to Streamlit's real-time communication

3. **Segment Analytics warnings** (Non-critical - browser extensions/cache)

## Root Causes

The 503/404 errors typically occur when:
- Streamlit app takes too long to initialize
- App crashes during startup before endpoints are ready
- Missing dependencies causing import failures
- Server configuration issues

## Fixes Applied

### 1. Updated `.streamlit/config.toml`
Added proper server configuration:
- WebSocket compression enabled (`enableWebsocketCompression = true`)
- Proper CORS/XSRF settings for Streamlit Cloud
- Upload size limits configured
- Server address configuration

### 2. Improved Error Handling in `app.py`
Enhanced `_get_config_int()` function to handle cases where:
- Streamlit might not be fully initialized during module import
- Secrets might not be available
- Better exception handling for AttributeError, RuntimeError, and KeyError

### 2. Additional Checks Needed

#### Check 1: Verify App Starts Successfully
Run locally to ensure no startup errors:
```bash
streamlit run app.py
```

#### Check 2: Verify All Dependencies
Ensure `requirements.txt` has all packages:
```bash
pip install -r requirements.txt
```

#### Check 3: Verify Secrets Configuration
On Streamlit Cloud, ensure all secrets are set:
- `AZURE_OPENAI_API_KEY`
- `AZURE_OPENAI_ENDPOINT`
- `RAPIDAPI_KEY`

#### Check 4: Check Streamlit Cloud Logs
1. Go to your Streamlit Cloud dashboard
2. Check the logs for any startup errors
3. Look for import errors or missing dependencies

## Additional Fixes to Try

### Option 1: Add Health Check Endpoint (if needed)
If the app is taking too long to start, you might need to optimize initialization.

### Option 2: Check for Heavy Imports
The app might be importing heavy libraries at startup. Consider lazy loading.

### Option 3: Verify Streamlit Version
Ensure you're using a compatible Streamlit version:
```bash
streamlit --version
```

## Testing the Fix

1. **Local Test:**
   ```bash
   streamlit run app.py
   ```
   - Check browser console for errors
   - Verify app loads completely

2. **Streamlit Cloud:**
   - Redeploy the app
   - Check logs in Streamlit Cloud dashboard
   - Verify endpoints are accessible

## Expected Behavior After Fix

- `/_stcore/health` should return 200 OK
- `/_stcore/host-config` should return 200 OK
- WebSocket connection should establish successfully
- No 503/404 errors in console

## If Errors Persist

1. **Check Streamlit Cloud Status:**
   - Visit https://status.streamlit.io
   - Check for service outages

2. **Review App Logs:**
   - Streamlit Cloud → Your App → Logs
   - Look for Python errors or import failures

3. **Verify Deployment:**
   - Ensure `app.py` is in the root directory
   - Ensure `.streamlit/config.toml` is committed
   - Ensure `requirements.txt` is up to date

4. **Contact Support:**
   - If issues persist, check Streamlit Community Forum
   - Or Streamlit Cloud support

## Notes

- **Segment Analytics errors** are from browser extensions/cache, not your app
- These can be safely ignored or cleared by:
  - Clearing browser cache
  - Disabling browser extensions
  - Using incognito/private mode
