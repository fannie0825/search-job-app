# 🔧 Troubleshooting: Nothing Shows in Folder

If you can't see files in your folder, try these solutions:

## Problem 1: Folder Appears Empty

### Solution A: Check You're in the Right Folder
1. In Finder, look at the top bar - it should show: `job-search-app`
2. If it shows something else, navigate again:
   - Press `Cmd + Shift + G`
   - Type: `/Users/tiffanyhowing/job-search-app`
   - Press Enter

### Solution B: Show All Files (Including Hidden)
1. In Finder, press `Cmd + Shift + .` (period key)
2. This toggles hidden files on/off
3. Try pressing it a few times
4. You should see files starting with `.` (like `.env.example`)

### Solution C: Check Different Folders
Try checking all three locations:
1. `/Users/tiffanyhowing/job-search-app`
2. `/Users/tiffanyhowing/job-search-app/job-search-app`
3. `/Users/tiffanyhowing/Desktop/job-search-app`

## Problem 2: Can't Find .env.example

### Solution: Create .env File Manually

**Step 1: Create New File**
1. In Finder, go to your project folder
2. Right-click in empty space
3. If you see "New Document" → Click it
4. If not, open TextEdit separately:
   - Press `Cmd + Space`
   - Type "TextEdit"
   - Press Enter
   - File → New Document

**Step 2: Copy This Template**
Paste this into the new file:

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=
REACT_APP_AZURE_OPENAI_ENDPOINT=
REACT_APP_RAPIDAPI_KEY=
```

**Step 3: Fill in Your Keys**
- Get keys from your Streamlit `secrets.toml`
- Paste them after the `=` sign (no quotes)

**Step 4: Save**
1. File → Save (`Cmd + S`)
2. Name it exactly: `.env`
3. Save location: `/Users/tiffanyhowing/job-search-app`
4. If it asks for extension, just use `.env`

## Problem 3: Using VS Code Instead

If Finder isn't working, use VS Code:

**Step 1: Open VS Code**
1. Press `Cmd + Space`
2. Type "VS Code" or "Code"
3. Press Enter

**Step 2: Open Project**
1. File → Open Folder
2. Navigate to: `/Users/tiffanyhowing/job-search-app`
3. Click Open

**Step 3: Create .env**
1. In VS Code sidebar, you'll see all files
2. Look for `.env.example` (if it exists)
3. Right-click → Copy
4. Right-click in sidebar → Paste
5. Rename to `.env`
6. Edit and add your keys
7. Save (`Cmd + S`)

## Problem 4: Create .env from Scratch

If nothing works, create it completely manually:

**Step 1: Open TextEdit**
- Press `Cmd + Space`
- Type "TextEdit"
- Press Enter

**Step 2: Type This Exactly**
```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=your-key-here
REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-endpoint.openai.azure.com
REACT_APP_RAPIDAPI_KEY=your-key-here
```

**Step 3: Replace Placeholders**
- Replace `your-key-here` with actual keys from Streamlit
- No quotes needed

**Step 4: Save**
1. File → Save (`Cmd + S`)
2. Navigate to: `/Users/tiffanyhowing/job-search-app`
3. File name: `.env`
4. Make sure "If no extension is provided, use .txt" is UNCHECKED
5. Click Save

## Problem 5: Verify Folder Exists

**Check if folder exists:**
1. Open Finder
2. Press `Cmd + Shift + G`
3. Type: `/Users/tiffanyhowing`
4. Press Enter
5. Look for `job-search-app` folder
6. Double-click to open it

## Alternative: Use GitHub Desktop

If you have GitHub Desktop:
1. Open GitHub Desktop
2. Find your `job-search-app` repository
3. Click "Show in Finder"
4. This will open the exact folder location

## Alternative: Check Recent Files

**In Finder:**
1. File → New Finder Window
2. Press `Cmd + Shift + O` (Go to Recent)
3. Look for `job-search-app` in recent folders

## Still Nothing? Create Fresh Project

If the folder is truly empty or missing:

**Option 1: Clone from GitHub**
1. Go to your GitHub repository
2. Click green "Code" button
3. Copy the URL
4. Open Terminal (just this once)
5. Type: `cd ~/Desktop`
6. Type: `git clone <paste-your-url> job-search-app`
7. This creates a fresh copy

**Option 2: Download ZIP**
1. Go to your GitHub repository
2. Click green "Code" button
3. Click "Download ZIP"
4. Extract to Desktop
5. Rename folder to `job-search-app`

---

**Try the VS Code method first - it's usually the easiest!** 💡
