# 📝 How to Add API Keys to .env File

Simple step-by-step guide to add your API keys.

## 🎯 Quick Steps

### Step 1: Create the .env File

**Option A: Using Terminal/Command Line**
```bash
# Navigate to your project folder
cd /workspace

# Copy the example file
cp .env.example .env
```

**Option B: Using File Explorer/Finder**
1. Go to your project folder (`/workspace`)
2. Find the file `.env.example`
3. Copy it
4. Rename the copy to `.env` (remove `.example`)

**Option C: Create New File**
1. In your project root folder, create a new file
2. Name it exactly: `.env` (with the dot at the beginning)
3. Make sure it's in the same folder as `package.json`

### Step 2: Open .env File

**Using VS Code:**
```bash
code .env
```

**Using any text editor:**
- Right-click `.env` → Open with → Text Editor
- Or use Notepad (Windows), TextEdit (Mac), or any editor

### Step 3: Add Your API Keys

Open your Streamlit `secrets.toml` file and copy your keys, then paste them into `.env`:

**Your Streamlit secrets.toml:**
```toml
AZURE_OPENAI_API_KEY = "abc123xyz789..."
AZURE_OPENAI_ENDPOINT = "https://careerlens.openai.azure.com"
RAPIDAPI_KEY = "def456uvw012..."
```

**Your React .env file (what to write):**
```env
# Backend API
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false

# Azure OpenAI (copy from Streamlit secrets.toml)
REACT_APP_AZURE_OPENAI_API_KEY=abc123xyz789...
REACT_APP_AZURE_OPENAI_ENDPOINT=https://careerlens.openai.azure.com

# RapidAPI (copy from Streamlit secrets.toml)
REACT_APP_RAPIDAPI_KEY=def456uvw012...
```

**Important Notes:**
- ❌ NO quotes around values (unlike Streamlit)
- ❌ NO spaces around the `=` sign
- ✅ Just: `KEY=value`
- ✅ Keep the `REACT_APP_` prefix

### Step 4: Save the File

Save the `.env` file (Ctrl+S or Cmd+S)

### Step 5: Restart Your React App

**IMPORTANT:** After editing `.env`, you MUST restart:
```bash
# Stop the server (press Ctrl+C)
# Then start again
npm start
```

## 📋 Complete Example

Here's what a complete `.env` file looks like:

```env
# ============================================
# CareerLens API Configuration
# ============================================

# Backend API URL
REACT_APP_API_URL=http://localhost:8000/api

# Use Mock API? (set to false to use real APIs)
REACT_APP_USE_MOCK_API=false

# ============================================
# API Keys (from Streamlit secrets.toml)
# ============================================

# Azure OpenAI API Key
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567

# Azure OpenAI Endpoint
REACT_APP_AZURE_OPENAI_ENDPOINT=https://careerlens.openai.azure.com

# RapidAPI Key
REACT_APP_RAPIDAPI_KEY=xyz789abc123def456ghi789jkl012mno345pqr678stu901vwx234

# Backend API Key (if your backend requires it)
REACT_APP_BACKEND_API_KEY=your-backend-key-here
```

## ✅ Verify It's Working

After saving and restarting, check:

```bash
# Run the check script
npm run check-env
```

You should see:
```
✅ REACT_APP_AZURE_OPENAI_API_KEY = abc123...xyz567
✅ REACT_APP_AZURE_OPENAI_ENDPOINT = https://...
✅ REACT_APP_RAPIDAPI_KEY = xyz789...vwx234
```

## 🎨 Visual Guide

### In VS Code:

1. **Open the file:**
   ```
   File → Open File → .env
   ```

2. **Edit the file:**
   ```
   REACT_APP_AZURE_OPENAI_API_KEY=paste-your-key-here
   ```

3. **Save:**
   ```
   Ctrl+S (Windows) or Cmd+S (Mac)
   ```

### In Terminal:

```bash
# Open with nano editor
nano .env

# Or with vim
vim .env

# Or with VS Code
code .env
```

## ⚠️ Common Mistakes

### ❌ Wrong:
```env
REACT_APP_AZURE_OPENAI_API_KEY = "abc123"  # ❌ Has quotes and spaces
REACT_APP_AZURE_OPENAI_API_KEY="abc123"   # ❌ Has quotes
REACT_APP_AZURE_OPENAI_API_KEY = abc123   # ❌ Has spaces
```

### ✅ Correct:
```env
REACT_APP_AZURE_OPENAI_API_KEY=abc123      # ✅ Perfect!
```

## 🔍 Troubleshooting

### Problem: Changes not working
**Solution:** Restart your React app after editing `.env`

### Problem: "API key is undefined"
**Solution:**
1. Check variable name starts with `REACT_APP_`
2. Check no quotes around value
3. Check no spaces around `=`
4. Restart the app

### Problem: Can't find .env file
**Solution:**
1. Make sure it's in the project root (same folder as `package.json`)
2. Make sure it's named exactly `.env` (with the dot)
3. Some file explorers hide files starting with `.` - enable "Show hidden files"

## 📍 File Location

Your `.env` file should be here:
```
/workspace/
├── .env              ← Your API keys go here
├── .env.example      ← Template (safe to commit)
├── package.json
├── src/
└── components/
```

## 🎯 Quick Copy-Paste Template

Copy this and fill in your keys:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=PASTE_YOUR_KEY_HERE
REACT_APP_AZURE_OPENAI_ENDPOINT=PASTE_YOUR_ENDPOINT_HERE
REACT_APP_RAPIDAPI_KEY=PASTE_YOUR_KEY_HERE
```

## ✅ Final Checklist

- [ ] Created `.env` file in project root
- [ ] Copied keys from Streamlit `secrets.toml`
- [ ] Added `REACT_APP_` prefix to each key
- [ ] Removed quotes from values
- [ ] No spaces around `=` signs
- [ ] Saved the file
- [ ] Restarted React app
- [ ] Verified with `npm run check-env`

---

**That's it!** Your API keys are now configured. 🎉
