# 📸 Step-by-Step Visual Guide (When Nothing Shows)

## Method 1: Create .env File from Scratch (Easiest)

### Step 1: Open TextEdit
1. Press `Cmd + Space` (Spotlight search)
2. Type: `TextEdit`
3. Press Enter
4. TextEdit opens with a blank document

### Step 2: Type or Paste This
Copy this entire block and paste into TextEdit:

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=
REACT_APP_AZURE_OPENAI_ENDPOINT=
REACT_APP_RAPIDAPI_KEY=
```

### Step 3: Get Your Keys from Streamlit
1. Open your Streamlit project folder
2. Find `.streamlit` folder
3. Open `secrets.toml` file
4. Copy these values:
   - The value after `AZURE_OPENAI_API_KEY = "..."` (without quotes)
   - The value after `AZURE_OPENAI_ENDPOINT = "..."` (without quotes)
   - The value after `RAPIDAPI_KEY = "..."` (without quotes)

### Step 4: Paste Your Keys
In TextEdit, after each `=` sign, paste your keys:

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=paste-your-azure-key-here
REACT_APP_AZURE_OPENAI_ENDPOINT=paste-your-endpoint-here
REACT_APP_RAPIDAPI_KEY=paste-your-rapidapi-key-here
```

**Example (with fake keys):**
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456ghi789jkl012
REACT_APP_AZURE_OPENAI_ENDPOINT=https://careerlens.openai.azure.com
REACT_APP_RAPIDAPI_KEY=xyz789abc123def456ghi789
```

### Step 5: Save the File
1. Press `Cmd + S` (or File → Save)
2. In the save dialog:
   - Navigate to: `/Users/tiffanyhowing/job-search-app`
   - File name: `.env` (with the dot!)
   - **Important:** Uncheck "If no extension is provided, use .txt"
   - Click Save

### Step 6: Verify
1. Go to Finder
2. Press `Cmd + Shift + G`
3. Type: `/Users/tiffanyhowing/job-search-app`
4. Press Enter
5. Press `Cmd + Shift + .` to show hidden files
6. You should see `.env` file
7. Double-click to verify your keys are there

## Method 2: Using VS Code (If You Have It)

### Step 1: Open VS Code
1. Press `Cmd + Space`
2. Type: `Code` or `VS Code`
3. Press Enter

### Step 2: Open Your Project
1. File → Open Folder
2. In the file picker, type: `/Users/tiffanyhowing/job-search-app`
3. Click Open

### Step 3: Create .env File
1. In the left sidebar, you'll see your files
2. Right-click in the sidebar (on empty space)
3. Click "New File"
4. Type: `.env` (with the dot)
5. Press Enter

### Step 4: Add Content
1. Click on `.env` file to open it
2. Paste this:

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=your-key-here
REACT_APP_AZURE_OPENAI_ENDPOINT=your-endpoint-here
REACT_APP_RAPIDAPI_KEY=your-key-here
```

3. Replace `your-key-here` with actual keys
4. Press `Cmd + S` to save

## Method 3: Check if Folder Exists First

### Verify the Folder
1. Open Finder
2. Press `Cmd + Shift + G`
3. Type: `/Users/tiffanyhowing`
4. Press Enter
5. Look for `job-search-app` folder
6. If you see it, double-click to open
7. If you DON'T see it, the folder might not exist

### If Folder Doesn't Exist
**Option A: Clone from GitHub**
1. Go to your GitHub repository
2. Click green "Code" button
3. Copy the HTTPS URL
4. Open Terminal (just this once)
5. Type: `cd ~/Desktop`
6. Type: `git clone <paste-url-here> job-search-app`
7. Wait for it to finish
8. Now you have the folder!

**Option B: Download ZIP**
1. Go to GitHub repository
2. Click green "Code" → "Download ZIP"
3. Extract ZIP file
4. Move folder to `/Users/tiffanyhowing/`
5. Rename to `job-search-app`

## Quick Checklist

Before creating .env, make sure:
- [ ] You can navigate to `/Users/tiffanyhowing/job-search-app` in Finder
- [ ] The folder exists and opens
- [ ] You can see at least some files (even if hidden)

If folder is completely empty or doesn't exist:
- [ ] Clone from GitHub (see Method 3 above)
- [ ] Or download ZIP from GitHub

## What Your .env File Should Look Like

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456ghi789jkl012mno345pqr678
REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
REACT_APP_RAPIDAPI_KEY=xyz789abc123def456ghi789jkl012mno345pqr678
```

**Key Points:**
- No quotes around values
- No spaces around `=`
- Each line is a separate key=value pair
- File name is exactly `.env` (with the dot)

---

**Try Method 1 first - it's the simplest!** ✨
