# ⚡ Quick Start Guide - Streamlit App

Get your CareerLens app running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

**If you get errors:**
```bash
pip3 install -r requirements.txt
```

## Step 2: Set Up API Keys

```bash
# Copy the example file
cp .streamlit/secrets.toml.example .streamlit/secrets.toml

# Edit it with your API keys
nano .streamlit/secrets.toml
```

**Add your keys:**
```toml
AZURE_OPENAI_API_KEY = "your-actual-key-here"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com"
RAPIDAPI_KEY = "your-actual-key-here"
```

**Save:** `Ctrl+O`, `Enter`, `Ctrl+X`

## Step 3: Run the App

```bash
streamlit run app.py
```

**That's it!** Your app will open at `http://localhost:8501`

## 🚀 Deploy to Streamlit Cloud

See [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md) for complete deployment instructions.

**Quick steps:**
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Deploy your app
4. Add secrets in Streamlit Cloud settings

## 🐛 Troubleshooting

**"Module not found"**
```bash
pip install -r requirements.txt
```

**"Secrets not found"**
- Make sure `.streamlit/secrets.toml` exists
- Check file path is correct

**API errors**
- Verify API keys are correct
- Check keys are valid and active

---

**Need more help?** See [README.md](README.md) for detailed documentation.
