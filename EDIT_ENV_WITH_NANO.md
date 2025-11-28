# 📝 Step-by-Step: Editing .env File with Nano (Terminal Editor)

This guide will walk you through editing your `.env` file using nano, a simple terminal-based text editor.

---

## 🎯 Step 1: Open the .env File in Nano

In your terminal, make sure you're in your project folder, then type:

```bash
nano .env
```

Press **Enter**.

**What you'll see:**
- The nano editor will open
- You'll see the contents of your `.env` file
- At the bottom, you'll see helpful commands like `^X Exit`, `^O Write Out`, etc.
- The `^` symbol means the `Ctrl` key

---

## 🎯 Step 2: Navigate to the First API Key

You'll see lines like this:

```
REACT_APP_AZURE_OPENAI_API_KEY=your-azure-openai-api-key-here
REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
REACT_APP_RAPIDAPI_KEY=your-rapidapi-key-here
REACT_APP_BACKEND_API_KEY=your-backend-api-key-here
```

**How to navigate:**
- Use the **arrow keys** (↑ ↓ ← →) to move your cursor
- Or use **Page Up** / **Page Down** to scroll
- Move your cursor to the line with `REACT_APP_AZURE_OPENAI_API_KEY=your-azure-openai-api-key-here`

---

## 🎯 Step 3: Replace the Placeholder Text

### For REACT_APP_AZURE_OPENAI_API_KEY:

1. **Position your cursor** at the end of the `=` sign:
   ```
   REACT_APP_AZURE_OPENAI_API_KEY=|your-azure-openai-api-key-here
                                  ↑ cursor here
   ```

2. **Select the placeholder text:**
   - Press and hold **Shift** and use **→** (right arrow) to select all of `your-azure-openai-api-key-here`
   - Or simply press **Ctrl+K** to delete from cursor to end of line (easier!)

3. **Delete the placeholder:**
   - If you selected it, just start typing (it will replace)
   - Or press **Delete** or **Backspace** to remove it

4. **Type your actual API key:**
   - Paste or type your Azure OpenAI API key
   - Example: `REACT_APP_AZURE_OPENAI_API_KEY=abc123def456ghi789...`
   - **NO quotes, NO spaces around the = sign**

### For REACT_APP_AZURE_OPENAI_ENDPOINT:

1. Move cursor to this line:
   ```
   REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
   ```

2. Position cursor after the `=` sign

3. Delete the placeholder and type your endpoint:
   ```
   REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-actual-resource-name.openai.azure.com
   ```

### For REACT_APP_RAPIDAPI_KEY:

1. Move cursor to this line:
   ```
   REACT_APP_RAPIDAPI_KEY=your-rapidapi-key-here
   ```

2. Position cursor after the `=` sign

3. Delete the placeholder and type your RapidAPI key:
   ```
   REACT_APP_RAPIDAPI_KEY=your-actual-rapidapi-key
   ```

### For REACT_APP_USE_MOCK_API:

You might want to change this from `true` to `false` if you have real API keys:

1. Find this line:
   ```
   REACT_APP_USE_MOCK_API=true
   ```

2. Change `true` to `false`:
   ```
   REACT_APP_USE_MOCK_API=false
   ```

---

## 🎯 Step 4: Save the File

After you've added all your API keys:

1. **Press `Ctrl + O`** (that's the letter O, not zero)
   - This means "Write Out" (save the file)
   - You'll see a prompt at the bottom: `File Name to Write: .env`

2. **Press Enter** to confirm
   - You'll see: `[ Wrote X lines ]` where X is the number of lines

---

## 🎯 Step 5: Exit Nano

1. **Press `Ctrl + X`** to exit nano
   - You'll return to your terminal prompt
   - If you haven't saved, nano will ask: `Save modified buffer?`
   - Type `Y` for Yes or `N` for No

---

## 📋 Quick Reference: Nano Commands

| Action | Command | What It Does |
|--------|---------|--------------|
| **Save** | `Ctrl + O` | Write Out (save) the file |
| **Exit** | `Ctrl + X` | Exit nano |
| **Cut Line** | `Ctrl + K` | Delete entire line (useful for removing placeholders) |
| **Paste** | `Ctrl + U` | Paste cut/copied text |
| **Search** | `Ctrl + W` | Search for text |
| **Go to Line** | `Ctrl + _` | Jump to specific line number |
| **Help** | `Ctrl + G` | Show help menu |

---

## ✅ Example: What Your Final .env Should Look Like

After editing, your `.env` file should look something like this:

```env
# ============================================
# CareerLens API Configuration
# ============================================

REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false

REACT_APP_AZURE_OPENAI_API_KEY=abc123def456ghi789jkl012mno345pqr678
REACT_APP_AZURE_OPENAI_ENDPOINT=https://careerlens.openai.azure.com
REACT_APP_RAPIDAPI_KEY=xyz789abc123def456ghi789jkl012mno345pqr678
REACT_APP_BACKEND_API_KEY=your-backend-key-if-needed
```

**Notice:**
- ✅ No quotes around values
- ✅ No spaces around `=` signs
- ✅ Real API keys (not placeholders)
- ✅ `REACT_APP_USE_MOCK_API=false` (if you have real keys)

---

## 🎬 Visual Walkthrough

### Step 1: Opening nano
```bash
$ nano .env
```

You'll see:
```
  GNU nano 6.0                    .env                          Modified

REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=true
REACT_APP_AZURE_OPENAI_API_KEY=your-azure-openai-api-key-here
REACT_APP_AZURE_OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
REACT_APP_RAPIDAPI_KEY=your-rapidapi-key-here

^G Get Help  ^O Write Out  ^W Where Is  ^K Cut Text  ^J Justify  ^C Cur Pos
^X Exit      ^R Read File  ^\ Replace   ^U Paste Text ^T To Spell ^_ Go To Line
```

### Step 2: Editing a line
1. Use arrow keys to move cursor to `your-azure-openai-api-key-here`
2. Press `Ctrl+K` to delete the line from cursor to end
3. Type your actual key: `abc123def456...`

### Step 3: Saving
1. Press `Ctrl+O`
2. See prompt: `File Name to Write: .env`
3. Press `Enter`
4. See: `[ Wrote 7 lines ]`

### Step 4: Exiting
1. Press `Ctrl+X`
2. You're back at the terminal prompt!

---

## 🐛 Troubleshooting

### Problem: Can't see the file content
**Solution:** Make sure you created the `.env` file first:
```bash
cp .env.example .env
nano .env
```

### Problem: Can't edit (file is read-only)
**Solution:** Check file permissions:
```bash
ls -la .env
```
If needed, fix permissions:
```bash
chmod 644 .env
```

### Problem: Accidentally deleted something
**Solution:** 
- Press `Ctrl+X` and type `N` to exit without saving
- Or press `Ctrl+U` to undo (paste back)

### Problem: Can't find where to type
**Solution:**
- The cursor (blinking `_`) shows where you'll type
- Use arrow keys to move it
- The bottom of the screen shows available commands

---

## 💡 Pro Tips

1. **Use `Ctrl+K` to quickly delete placeholders:**
   - Position cursor after `=`
   - Press `Ctrl+K` to delete everything to end of line
   - Type your key

2. **Use `Ctrl+W` to search:**
   - Press `Ctrl+W`
   - Type `AZURE_OPENAI` to jump to that line

3. **Copy from another file:**
   - Open your Streamlit `secrets.toml` in another window
   - Copy the key value
   - In nano, position cursor and paste (`Cmd+V` on Mac, `Shift+Insert` on Linux)

---

## ✅ Verification After Editing

After you save and exit, verify your file:

```bash
# Check the file exists
ls -la .env

# View the file (without editing)
cat .env

# Or use the check script
npm run check-env
```

---

**That's it!** You've successfully edited your `.env` file using nano. 🎉

Now you can proceed to install dependencies and start your app:
```bash
npm install
npm start
```
