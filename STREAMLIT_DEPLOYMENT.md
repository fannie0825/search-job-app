# 🚀 Deploy CareerLens to Streamlit Cloud

Complete guide to deploy your Streamlit app to Streamlit Cloud.

## Prerequisites

- ✅ GitHub account
- ✅ Your code pushed to GitHub repository
- ✅ Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

## Step 1: Prepare Your Repository

### Check Required Files

Make sure these files exist in your repository:

```bash
# Main application file
app.py

# Python dependencies
requirements.txt

# Streamlit configuration (optional)
.streamlit/config.toml

# Secrets example (for reference)
.streamlit/secrets.toml.example
```

### Verify .gitignore

Make sure `.streamlit/secrets.toml` is in `.gitignore` (so you don't commit your API keys):

```bash
cat .gitignore | grep secrets.toml
```

**Should show:** `.streamlit/secrets.toml`

If not, add it:
```bash
echo ".streamlit/secrets.toml" >> .gitignore
```

## Step 2: Push to GitHub

### If Repository Already Exists

```bash
# Make sure you're in the project folder
cd ~/Desktop/job-search-app

# Check status
git status

# Add all files (secrets.toml will be ignored)
git add .

# Commit
git commit -m "Ready for Streamlit Cloud deployment"

# Push to GitHub
git push origin main
```

### If Creating New Repository

```bash
# Initialize git (if not already done)
git init

# Add remote
git remote add origin https://github.com/your-username/your-repo-name.git

# Add and commit
git add .
git commit -m "Initial commit - Streamlit app"

# Push
git push -u origin main
```

## Step 3: Deploy on Streamlit Cloud

### 3.1 Create Account

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"Sign up"** or **"Get started"**
3. Sign in with your **GitHub account**
4. Authorize Streamlit Cloud to access your repositories

### 3.2 Deploy Your App

1. Click **"New app"** button
2. Fill in the form:
   - **Repository**: Select your GitHub repository
   - **Branch**: Select `main` (or your default branch)
   - **Main file path**: Enter `app.py`
3. Click **"Deploy!"**

### 3.3 Wait for Deployment

- Streamlit Cloud will:
  - Install dependencies from `requirements.txt`
  - Run your app
  - Show you the deployment URL

**Your app will be available at:** `https://your-app-name.streamlit.app`

## Step 4: Add API Keys (Secrets)

### 4.1 Access Secrets Settings

1. Go to your app on Streamlit Cloud
2. Click **"Settings"** (⚙️ icon) or **"Manage app"**
3. Click **"Secrets"** tab

### 4.2 Add Your Secrets

Paste your secrets in TOML format:

```toml
AZURE_OPENAI_API_KEY = "your-actual-azure-openai-key-here"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com"
RAPIDAPI_KEY = "your-actual-rapidapi-key-here"
```

**Important:**
- Use the exact same format as `.streamlit/secrets.toml`
- No quotes needed around values (but they're okay if you include them)
- One key per line

### 4.3 Save and Restart

1. Click **"Save"**
2. Your app will automatically restart with the new secrets
3. Check the app - it should now work with API calls

## Step 5: Verify Deployment

### Check Your App

1. Visit your app URL: `https://your-app-name.streamlit.app`
2. Test the features:
   - Create a profile
   - Search for jobs
   - Generate a resume

### Check Logs

If something doesn't work:

1. Go to your app on Streamlit Cloud
2. Click **"Manage app"** → **"Logs"**
3. Look for error messages
4. Common issues:
   - Missing dependencies → Add to `requirements.txt`
   - API key errors → Check secrets are correct
   - Import errors → Check file paths

## 🐛 Troubleshooting

### Problem: "Module not found" error

**Solution:**
1. Check `requirements.txt` includes all dependencies
2. Add missing packages to `requirements.txt`
3. Push changes and redeploy

### Problem: "Secrets not found" error

**Solution:**
1. Go to Settings → Secrets
2. Verify secrets are added correctly
3. Check format matches `secrets.toml.example`
4. Save and wait for app to restart

### Problem: App won't deploy

**Solution:**
1. Check `app.py` is in the root of your repository
2. Verify `requirements.txt` exists
3. Check Streamlit Cloud logs for specific errors
4. Ensure your repository is public (or you have Streamlit Cloud Pro for private repos)

### Problem: API calls failing

**Solution:**
1. Verify API keys are correct in Secrets
2. Check API keys are still valid
3. Verify Azure OpenAI deployments are active
4. Check RapidAPI subscription is active

### Problem: Slow loading

**Solution:**
- First load can be slow (cold start)
- Subsequent loads should be faster
- Consider upgrading to Streamlit Cloud Pro for better performance

## 📋 Deployment Checklist

Before deploying, verify:

- [ ] `app.py` exists and runs locally
- [ ] `requirements.txt` includes all dependencies
- [ ] `.streamlit/secrets.toml` is in `.gitignore`
- [ ] Code is pushed to GitHub
- [ ] Repository is accessible (public or authorized)
- [ ] Ready to add secrets in Streamlit Cloud

## 🔄 Updating Your App

### After Making Changes

1. **Make changes locally**
2. **Test locally:** `streamlit run app.py`
3. **Commit and push:**
   ```bash
   git add .
   git commit -m "Update app"
   git push origin main
   ```
4. **Streamlit Cloud automatically redeploys** when you push to main branch

### Update Secrets

1. Go to Settings → Secrets
2. Edit the secrets
3. Save - app restarts automatically

## 📚 Additional Resources

- [Streamlit Cloud Documentation](https://docs.streamlit.io/streamlit-community-cloud)
- [Streamlit Secrets Management](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)
- [Streamlit Community Forum](https://discuss.streamlit.io/)

## ✅ Success!

Once deployed, your app is:
- ✅ Live on the internet
- ✅ Accessible 24/7
- ✅ Automatically updates when you push to GitHub
- ✅ Free (with Streamlit Cloud free tier)

**Share your app URL:** `https://your-app-name.streamlit.app`

---

Need help? Check the [Troubleshooting](#-troubleshooting) section or open an issue on GitHub.
