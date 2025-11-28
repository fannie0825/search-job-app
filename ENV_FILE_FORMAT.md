# 📝 .env File Format Guide

## ✅ Correct Format

Your `.env` file should look exactly like this:

```
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456ghi789jkl012mno345pqr678
REACT_APP_AZURE_OPENAI_ENDPOINT=https://careerlens.openai.azure.com
REACT_APP_RAPIDAPI_KEY=xyz789abc123def456ghi789jkl012mno345pqr678
```

## 📋 Format Rules

### ✅ DO:
- ✅ One key per line
- ✅ Format: `KEY=value` (no spaces around `=`)
- ✅ No quotes around values
- ✅ No blank lines between keys (optional, but cleaner)
- ✅ Each line ends with nothing (no semicolons, no commas)

### ❌ DON'T:
- ❌ NO quotes: `REACT_APP_KEY="value"` ❌
- ❌ NO spaces: `REACT_APP_KEY = value` ❌
- ❌ NO semicolons: `REACT_APP_KEY=value;` ❌
- ❌ NO commas: `REACT_APP_KEY=value,` ❌

## 🔄 Converting from Streamlit Format

### Streamlit Format (secrets.toml):
```toml
AZURE_OPENAI_API_KEY = "abc123def456..."
AZURE_OPENAI_ENDPOINT = "https://careerlens.openai.azure.com"
RAPIDAPI_KEY = "xyz789abc123..."
```

### React Format (.env):
```env
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456...
REACT_APP_AZURE_OPENAI_ENDPOINT=https://careerlens.openai.azure.com
REACT_APP_RAPIDAPI_KEY=xyz789abc123...
```

**Changes:**
1. Remove quotes (`"` and `"`)
2. Remove spaces around `=`
3. Add `REACT_APP_` prefix
4. Change `=` to `=` (same, but no spaces)

## 📸 Visual Examples

### ✅ CORRECT Examples:

**Example 1: Short Keys**
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=sk-abc123xyz
REACT_APP_AZURE_OPENAI_ENDPOINT=https://careerlens.openai.azure.com
REACT_APP_RAPIDAPI_KEY=rapid123key456
```

**Example 2: Long Keys**
```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567
REACT_APP_AZURE_OPENAI_ENDPOINT=https://careerlens-resource.openai.azure.com
REACT_APP_RAPIDAPI_KEY=xyz789abc123def456ghi789jkl012mno345pqr678stu901vwx234
```

**Example 3: With Comments (Optional)**
```env
# Backend API Configuration
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false

# Azure OpenAI Keys
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456ghi789
REACT_APP_AZURE_OPENAI_ENDPOINT=https://careerlens.openai.azure.com

# RapidAPI Key
REACT_APP_RAPIDAPI_KEY=xyz789abc123def456
```

### ❌ WRONG Examples:

**Wrong 1: With Quotes**
```env
REACT_APP_AZURE_OPENAI_API_KEY="abc123def456"  ❌
```
**Fix:** Remove quotes
```env
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456  ✅
```

**Wrong 2: With Spaces**
```env
REACT_APP_AZURE_OPENAI_API_KEY = abc123def456  ❌
```
**Fix:** Remove spaces
```env
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456  ✅
```

**Wrong 3: Missing REACT_APP_ Prefix**
```env
AZURE_OPENAI_API_KEY=abc123def456  ❌
```
**Fix:** Add prefix
```env
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456  ✅
```

**Wrong 4: With Semicolon**
```env
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456;  ❌
```
**Fix:** Remove semicolon
```env
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456  ✅
```

## 📋 Complete Template (Copy-Paste Ready)

Copy this entire block and fill in your keys:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=
REACT_APP_AZURE_OPENAI_ENDPOINT=
REACT_APP_RAPIDAPI_KEY=
```

## 🎯 Step-by-Step Format Conversion

### From Streamlit to React:

**Step 1: Get from Streamlit**
```
AZURE_OPENAI_API_KEY = "abc123def456..."
```

**Step 2: Remove quotes**
```
AZURE_OPENAI_API_KEY = abc123def456...
```

**Step 3: Remove spaces around =**
```
AZURE_OPENAI_API_KEY=abc123def456...
```

**Step 4: Add REACT_APP_ prefix**
```
REACT_APP_AZURE_OPENAI_API_KEY=abc123def456...
```

**Done! ✅**

## 🔍 Character-by-Character Format

```
R E A C T _ A P P _ A Z U R E _ O P E N A I _ A P I _ K E Y = a b c 1 2 3 . . .
│                                                           │ │
│                                                           │ └─ Value (no quotes)
│                                                           └─ Equals sign (no spaces)
└─ Key name with REACT_APP_ prefix
```

## ✅ Format Checklist

Before saving, check:
- [ ] Each line has format: `KEY=value`
- [ ] No quotes around values
- [ ] No spaces around `=`
- [ ] All keys start with `REACT_APP_`
- [ ] Each line is separate (no commas)
- [ ] No semicolons at end
- [ ] File is saved as `.env` (with the dot)

## 📝 Example: Complete File

Here's what a complete, correctly formatted `.env` file looks like:

```env
REACT_APP_API_URL=http://localhost:8000/api
REACT_APP_USE_MOCK_API=false
REACT_APP_AZURE_OPENAI_API_KEY=sk-proj-abc123def456ghi789jkl012mno345pqr678stu901vwx234yz567
REACT_APP_AZURE_OPENAI_ENDPOINT=https://careerlens-resource.openai.azure.com
REACT_APP_RAPIDAPI_KEY=xyz789abc123def456ghi789jkl012mno345pqr678stu901vwx234
```

**That's it!** Simple format: `KEY=value` on each line, no quotes, no spaces. ✅
