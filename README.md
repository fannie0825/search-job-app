# CareerLens - AI Career Copilot

An AI-powered job search application with intelligent resume generation capabilities. Built with Streamlit and Azure OpenAI.

## 🌟 Features

### 1. **Semantic Job Search**
- Search jobs from Indeed using keywords and location
- AI-powered semantic matching using Azure OpenAI embeddings
- Intelligent ranking based on job description similarity
- Filter by country, job type, and match score

### 2. **AI-Powered Resume Generation**
- Create personalized resumes tailored to specific job postings
- Automatic keyword optimization for ATS (Applicant Tracking Systems)
- Highlight relevant experience and skills for each position
- Edit and download generated resumes

### 3. **User Profile Management**
- Store your professional information securely
- Include work experience, education, skills, and certifications
- Reuse profile for multiple job applications

### 4. **Direct Job Application**
- Access job posting websites directly
- Generate resume before applying
- Seamless integration with Indeed job links

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Azure OpenAI API account
- RapidAPI account (for Indeed Scraper API)

### Installation

1. **Clone the repository:**
```bash
git clone <repository-url>
cd job-search-app
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up API keys:**

Create a `.streamlit/secrets.toml` file:
```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml` and add your API keys:
```toml
AZURE_OPENAI_API_KEY = "your-azure-openai-api-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource-name.openai.azure.com"
RAPIDAPI_KEY = "your-rapidapi-key"
```

4. **Run the application:**
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 📖 Usage Guide

### Step 1: Set Up Your Profile
1. Navigate to the **"My Profile"** tab
2. Fill in your personal information:
   - Contact details (name, email, phone)
   - Professional summary
   - Work experience
   - Education
   - Skills and certifications
3. Click **"Save Profile"**

### Step 2: Search for Jobs
1. Go to the **"Job Search"** tab
2. Configure search settings in the sidebar:
   - Keywords (e.g., "software developer")
   - Location
   - Country
   - Job type
   - Number of results
3. Click **"Fetch Jobs"**

### Step 3: Find Relevant Matches
1. Enter your ideal job description in the semantic search box
2. Adjust the number of results and minimum match score
3. Click **"Search"** to get AI-ranked results

### Step 4: Generate Tailored Resume
1. Click the **"📄 Resume"** button on any job card
2. Review your profile information
3. Click **"Generate Tailored Resume"**
4. Edit the generated resume if needed
5. Download as TXT or copy to clipboard
6. Click **"Apply to Job"** to visit the job posting

## 🚀 Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- Streamlit Cloud account (free at [share.streamlit.io](https://share.streamlit.io))

### Deployment Steps

1. **Push your code to GitHub:**
```bash
git add .
git commit -m "Ready for Streamlit Cloud"
git push origin main
```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click **"New app"**
   - Select your repository and branch
   - Set **Main file path** to: `app.py`
   - Click **"Deploy!"**

3. **Add Secrets:**
   - Go to your app → **Settings** → **Secrets**
   - Add your API keys in the same format as `secrets.toml`
   - Save - your app will automatically restart

Your app will be live at: `https://your-app-name.streamlit.app`

For detailed deployment instructions, see [STREAMLIT_DEPLOYMENT.md](STREAMLIT_DEPLOYMENT.md)

## 🔧 Configuration

### Azure OpenAI Setup
1. Go to [Azure Portal](https://portal.azure.com)
2. Create an Azure OpenAI resource
3. Deploy these models:
   - `text-embedding-3-small` (for semantic search)
   - `gpt-4o-mini` or `gpt-4` (for resume generation)
4. Copy the API key and endpoint from "Keys and Endpoint" section

**Note**: If your deployment names are different, update them in `app.py`:
- Line ~81: `self.deployment = "text-embedding-3-small"`
- Line ~257: `self.deployment = "gpt-4o-mini"`

### RapidAPI Setup
1. Sign up at [RapidAPI](https://rapidapi.com)
2. Subscribe to [Indeed Scraper API](https://rapidapi.com/indeed-scraper-api/api/indeed-scraper-api)
3. Copy your RapidAPI key from the API dashboard

## 🛠️ Technical Stack

- **Frontend**: Streamlit
- **AI/ML**: Azure OpenAI (embeddings & text generation)
- **Job Data**: Indeed Scraper API (via RapidAPI)
- **Vector Search**: Scikit-learn (cosine similarity)

## 📊 Data Flow

1. **Job Fetching**: Indeed API → Job data with descriptions
2. **Indexing**: Job descriptions → Azure OpenAI embeddings → Vector database
3. **Search**: User query → Embedding → Similarity search → Ranked results
4. **Resume Generation**: User profile + Job description → GPT-4 → Tailored resume

## 🐛 Troubleshooting

**Issue**: API errors when generating resumes
- **Solution**: Check Azure OpenAI API key and endpoint configuration in `.streamlit/secrets.toml`

**Issue**: No jobs found
- **Solution**: Try broader keywords or different locations

**Issue**: Low match scores
- **Solution**: Adjust minimum score slider or refine search query

**Issue**: Module not found errors
- **Solution**: Run `pip install -r requirements.txt`

## 📝 Project Structure

```
job-search-app/
├── app.py                    # Main Streamlit application
├── requirements.txt          # Python dependencies
├── .streamlit/
│   ├── config.toml          # Streamlit configuration
│   └── secrets.toml.example  # Example secrets file
├── README.md                 # This file
└── STREAMLIT_DEPLOYMENT.md  # Deployment guide
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is provided as-is for educational and personal use.

## 🙏 Acknowledgments

- Azure OpenAI for powerful AI capabilities
- Streamlit for the intuitive web framework
- RapidAPI for job search API access

---

Made with ❤️ using Streamlit and Azure OpenAI
