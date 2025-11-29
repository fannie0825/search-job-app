# 🔧 Fix: Update package.json to Use Vite

Your local `package.json` is still configured for Next.js, but your project uses Vite. Here's how to fix it.

## 🎯 Quick Fix: Update package.json

### Option 1: Edit with Nano (Recommended)

1. **Open package.json in nano:**
   ```bash
   nano package.json
   ```

2. **Find the "scripts" section** and change these lines:

   **Change FROM:**
   ```json
   "scripts": {
     "dev": "next dev",
     "build": "next build",
     "start": "next start",
     "lint": "next lint",
   ```

   **Change TO:**
   ```json
   "scripts": {
     "dev": "vite",
     "build": "vite build",
     "preview": "vite preview",
     "start": "vite",
     "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0",
   ```

3. **Add this line** right after `"description"` (before `"scripts"`):
   ```json
   "type": "module",
   ```

4. **Find the "devDependencies" section** and replace it with:
   ```json
   "devDependencies": {
     "@types/react": "^18.2.43",
     "@types/react-dom": "^18.2.17",
     "@vitejs/plugin-react": "^4.2.1",
     "autoprefixer": "^10.4.16",
     "eslint": "^8.55.0",
     "eslint-plugin-react": "^7.33.2",
     "eslint-plugin-react-hooks": "^4.6.0",
     "eslint-plugin-react-refresh": "^0.4.5",
     "postcss": "^8.4.32",
     "tailwindcss": "^3.4.0",
     "vite": "^5.0.8"
   }
   ```

5. **Save:** Press `Ctrl+O`, then `Enter`
6. **Exit:** Press `Ctrl+X`

### Option 2: Replace Entire File

If editing is too complex, you can replace the entire file:

1. **Backup your current file:**
   ```bash
   cp package.json package.json.backup
   ```

2. **Open package.json:**
   ```bash
   nano package.json
   ```

3. **Delete everything** (`Ctrl+K` repeatedly, or select all and delete)

4. **Paste this entire content:**

```json
{
  "name": "careerlens",
  "version": "1.0.0",
  "description": "CareerLens - AI Career Copilot for Hong Kong",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "preview": "vite preview",
    "start": "vite",
    "lint": "eslint . --ext js,jsx --report-unused-disable-directives --max-warnings 0",
    "build:css": "tailwindcss -i ./globals.css -o ./dist/output.css --watch",
    "check-env": "node scripts/check-env.js",
    "check-security": "node scripts/check-security.js"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "lucide-react": "^0.294.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.43",
    "@types/react-dom": "^18.2.17",
    "@vitejs/plugin-react": "^4.2.1",
    "autoprefixer": "^10.4.16",
    "eslint": "^8.55.0",
    "eslint-plugin-react": "^7.33.2",
    "eslint-plugin-react-hooks": "^4.6.0",
    "eslint-plugin-react-refresh": "^0.4.5",
    "postcss": "^8.4.32",
    "tailwindcss": "^3.4.0",
    "vite": "^5.0.8"
  },
  "keywords": [
    "career",
    "job-search",
    "ai",
    "hong-kong"
  ],
  "author": "",
  "license": "MIT"
}
```

5. **Save:** `Ctrl+O`, then `Enter`
6. **Exit:** `Ctrl+X`

## 🎯 Step 2: Create vite.config.js

You also need to create a Vite configuration file:

1. **Create the file:**
   ```bash
   nano vite.config.js
   ```

2. **Paste this content:**
   ```javascript
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'

   // https://vitejs.dev/config/
   export default defineConfig({
     plugins: [react()],
     server: {
       port: 3000,
       open: true
     }
   })
   ```

3. **Save:** `Ctrl+O`, then `Enter`
4. **Exit:** `Ctrl+X`

## 🎯 Step 3: Install Dependencies

Now install the new dependencies:

```bash
npm install
```

This will install Vite and all the other required packages.

## 🎯 Step 4: Start the App

```bash
npm start
```

Or:

```bash
npm run dev
```

The app should now start successfully! 🎉

## ✅ Verification

After making these changes, verify:

1. **Check package.json is correct:**
   ```bash
   cat package.json | grep vite
   ```
   Should show `"vite"` in the output

2. **Check vite.config.js exists:**
   ```bash
   ls -la vite.config.js
   ```

3. **Try starting:**
   ```bash
   npm start
   ```

## 🐛 Troubleshooting

### Still getting "next: command not found"
- Make sure you saved package.json
- Verify the "start" script says `"vite"` not `"next start"`
- Run `npm install` again

### "vite: command not found"
- Run `npm install` to install Vite
- Check that `vite` is in devDependencies

### Syntax errors in package.json
- Make sure all quotes are properly closed
- Check for commas (no comma after last item in objects/arrays)
- Use `cat package.json` to verify the file looks correct

---

**After these steps, your app should start with Vite!** 🚀
