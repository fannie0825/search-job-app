# Code Logic Flow Summary - app.py

## Overview
This is a Streamlit-based semantic job search and resume generation application that uses Azure OpenAI for embeddings and text generation, and RapidAPI for job scraping.

---

## 1. INITIALIZATION & IMPORTS (Lines 1-23)

**Flow:**
- Suppresses warnings and sets Streamlit log level to error
- Imports required libraries:
  - `streamlit` for UI
  - `requests` for API calls
  - `numpy` and `sklearn` for similarity calculations
  - `PyPDF2` and `docx` for resume file parsing
- Configures Streamlit page settings (title, icon, layout, sidebar state)
- Defines custom CSS styles for job cards, match scores, and tags

---

## 2. SESSION STATE INITIALIZATION (Lines 75-98)

**Flow:**
Initializes all session state variables to track application state:
- `search_history`: Previous search queries
- `jobs_cache`: Cached job listings
- `embedding_gen`: Embedding generator instance (singleton)
- `user_profile`: User's profile information
- `generated_resume`: AI-generated resume data
- `text_gen`: Text generator instance (singleton)
- `selected_job`: Currently selected job for resume generation
- `show_resume_generator`: Flag to show/hide resume generator UI
- `resume_text`: Extracted text from uploaded resume
- `matched_jobs`: Results from automatic job matching
- `match_score`: Similarity score between resume and job
- `missing_keywords`: Keywords from job description not in resume

---

## 3. CORE CLASSES

### 3.1 APIMEmbeddingGenerator (Lines 100-152)

**Purpose:** Generates embeddings using Azure OpenAI API

**Flow:**
- **`__init__`**: 
  - Takes API key and endpoint
  - Normalizes endpoint URL (removes trailing slashes, handles `/openai` path)
  - Constructs API URL for embeddings endpoint
  - Sets headers with API key

- **`get_embedding`**: 
  - Takes text input
  - Sends POST request to Azure OpenAI embeddings API
  - Returns embedding vector or None on error

- **`get_embeddings_batch`**: 
  - Processes multiple texts in batches (default: 10)
  - Shows progress bar and status updates
  - Handles batch failures by falling back to individual requests
  - Returns list of embeddings

### 3.2 AzureOpenAITextGenerator (Lines 154-352)

**Purpose:** Generates text using Azure OpenAI GPT models

**Flow:**
- **`__init__`**: 
  - Similar to embedding generator
  - Sets up chat completions endpoint
  - Uses `gpt-4o-mini` deployment

- **`generate_resume`** (Lines 168-291):
  - **Input:** User profile, job posting, optional raw resume text
  - **Process:**
    1. Creates system instructions for resume writing
    2. Formats job description section
    3. Formats structured user profile section
    4. Optionally includes raw resume text (Context Sandwich approach)
    5. Constructs prompt with instructions for tailoring resume
    6. Sends request with JSON response format enforced
    7. Parses JSON response (handles markdown code blocks)
  - **Output:** Structured JSON resume data

- **`calculate_match_score`** (Lines 293-352):
  - **Input:** Resume content, job description, embedding generator
  - **Process:**
    1. Generates embeddings for resume and job description
    2. Calculates cosine similarity between embeddings
    3. Extracts keywords from job description using AI
    4. Checks which keywords are missing from resume
  - **Output:** Match score (0-1) and list of missing keywords

### 3.3 IndeedScraperAPI (Lines 354-428)

**Purpose:** Fetches job listings from Indeed via RapidAPI

**Flow:**
- **`__init__`**: Sets up API endpoint and headers
- **`search_jobs`**: 
  - Takes search parameters (query, location, max_rows, job_type, country)
  - Sends POST request to RapidAPI
  - Parses response and extracts job data
  - Returns list of job dictionaries
- **`_parse_job`**: 
  - Extracts and formats job data from API response
  - Handles location, job type, benefits, skills, ratings
  - Returns structured job dictionary

### 3.4 SemanticJobSearch (Lines 430-469)

**Purpose:** Performs semantic search on job listings

**Flow:**
- **`__init__`**: Initializes with embedding generator
- **`index_jobs`**: 
  - Takes list of jobs
  - Creates text representations (title + company + description + skills)
  - Generates embeddings for all jobs in batch
  - Stores embeddings and jobs
- **`search`**: 
  - Takes query string and top_k parameter
  - Generates embedding for query
  - Calculates cosine similarity between query and all job embeddings
  - Returns top_k most similar jobs with similarity scores

---

## 4. HELPER FUNCTIONS

### 4.1 Singleton Getters (Lines 471-489)

**Flow:**
- **`get_embedding_generator`**: Returns singleton embedding generator instance
- **`get_job_scraper`**: Creates new scraper instance (not singleton)
- **`get_text_generator`**: Returns singleton text generator instance

### 4.2 Display Functions

**`display_job_card`** (Lines 491-551):
- Renders a single job card with:
  - Job title, company, location, remote badge
  - Match score percentage
  - Job type, salary, posted date
  - Benefits and skills tags
  - Full description expander
  - "Apply" link button
  - "Resume" button (triggers resume generator)

**`extract_text_from_resume`** (Lines 553-586):
- Handles PDF, DOCX, and TXT file uploads
- Extracts text content from files
- Returns extracted text or None on error

**`extract_profile_from_resume`** (Lines 588-666):
- Uses Azure OpenAI to parse resume text
- Extracts structured profile information (name, email, experience, etc.)
- Returns JSON profile data
- Handles JSON parsing errors and markdown code blocks

**`display_user_profile`** (Lines 668-793):
- Shows profile management UI with:
  1. Resume upload section
  2. Automatic profile extraction from uploaded resume
  3. Editable form fields for all profile information
  4. Save functionality

**`render_structured_resume_editor`** (Lines 795-895):
- Displays generated resume in editable form
- Sections: Header, Summary, Skills, Experience (with bullets), Education, Certifications
- Allows inline editing of all resume sections
- Returns edited resume data

**`generate_docx_from_json`** (Lines 897-1010):
- Converts structured resume JSON to professional DOCX file
- Formats with proper styling, margins, fonts
- Returns BytesIO object for download

**`display_match_score_feedback`** (Lines 1012-1053):
- Shows match score with color coding (green/yellow/red)
- Displays missing keywords
- Provides feedback and tips

**`display_resume_generator`** (Lines 1055-1218):
- Main resume generation interface
- **Flow:**
  1. Checks if job is selected
  2. Validates user profile is complete
  3. "Generate Resume" button triggers:
     - Calls `generate_resume()` with user profile and job
     - Calculates match score
     - Stores results in session state
  4. Displays match score feedback
  5. Shows structured resume editor
  6. Provides download buttons (DOCX, JSON, TXT)
  7. "Recalculate Match Score" button for updated resume

**`format_resume_as_text`** (Lines 1220-1299):
- Converts structured resume JSON to plain text format
- Formats with headers, sections, bullet points

---

## 5. MAIN APPLICATION FLOW (Lines 1301-1506)

### Entry Point: `main()` Function

**Flow:**

1. **Check Resume Generator State** (Lines 1302-1305):
   - If `show_resume_generator` is True, display resume generator and return

2. **Main UI Setup** (Lines 1307-1311):
   - Displays header and subtitle
   - Creates two tabs: "Job Search" and "My Profile"

3. **Profile Tab** (Lines 1313-1314):
   - Calls `display_user_profile()` function

4. **Job Search Tab** (Lines 1316-1503):

   **A. Sidebar Settings** (Lines 1317-1342):
   - Search query input
   - Location input
   - Country and job type selectors
   - Max jobs slider
   - "Fetch Jobs" button
   - Cache display and clear button

   **B. Fetch Jobs** (Lines 1344-1361):
   - When "Fetch Jobs" clicked:
     1. Gets job scraper instance
     2. Calls `search_jobs()` with parameters
     3. Stores results in `jobs_cache` session state
     4. Shows success message and reruns

   **C. Automatic Job Matching** (Lines 1371-1449):
   - **Condition:** Only shown if user has uploaded resume OR has profile data
   - **Flow:**
     1. Checks for resume text or profile data
     2. Shows info message about automatic matching
     3. User can set number of results and minimum score
     4. When "Find Best Matching Jobs" clicked:
        - Creates `SemanticJobSearch` instance
        - Indexes all jobs (generates embeddings)
        - Creates query from resume text or profile data
        - Performs semantic search
        - Filters by minimum score
        - Stores results in `matched_jobs`
        - Displays results with metrics
     5. Shows previously matched jobs if available

   **D. Manual Semantic Search** (Lines 1451-1503):
   - **Flow:**
     1. User enters text query describing ideal job
     2. Sets number of results and minimum score
     3. When "Search" clicked:
        - Creates `SemanticJobSearch` instance
        - Indexes all jobs
        - Performs semantic search with user query
        - Filters by minimum score
        - Displays results with metrics
     4. Shows warning if query is empty

---

## 6. EXECUTION FLOW SUMMARY

### Application Startup:
1. Imports and configuration
2. Session state initialization
3. CSS styling applied
4. `main()` function called

### User Journey:

**Path 1: Profile Setup**
1. User navigates to "My Profile" tab
2. Optionally uploads resume → text extracted → profile auto-filled
3. User edits and saves profile

**Path 2: Job Search**
1. User sets search parameters in sidebar
2. Clicks "Fetch Jobs" → jobs retrieved and cached
3. **Option A - Automatic Matching:**
   - System uses resume/profile to find best matches
   - Results displayed with match scores
4. **Option B - Manual Search:**
   - User enters query
   - System performs semantic search
   - Results displayed

**Path 3: Resume Generation**
1. User clicks "Resume" button on a job card
2. Resume generator page shown
3. User clicks "Generate Tailored Resume"
4. AI generates resume based on profile + job description
5. Match score calculated and displayed
6. User can edit resume sections
7. User downloads resume (DOCX/JSON/TXT)
8. User can apply to job

---

## KEY DATA FLOWS

### Embedding Flow:
```
Text → APIMEmbeddingGenerator → Azure OpenAI API → Embedding Vector
```

### Resume Generation Flow:
```
User Profile + Job Description → AzureOpenAITextGenerator → Structured JSON Resume
```

### Job Matching Flow:
```
Resume/Profile → Embedding → Cosine Similarity → Ranked Job List
```

### Job Fetching Flow:
```
Search Parameters → IndeedScraperAPI → RapidAPI → Job Listings
```

---

## ERROR HANDLING

- API errors: Displayed via `st.error()`
- File parsing errors: Graceful fallback with error messages
- JSON parsing errors: Multiple fallback strategies (strip markdown, regex extraction)
- Missing data: Uses "N/A" or empty strings
- Network timeouts: 30-60 second timeouts on API calls

---

## STATE MANAGEMENT

All application state is managed through Streamlit's `st.session_state`:
- Persists across reruns
- Used for caching expensive operations (embeddings, job listings)
- Tracks user selections and generated content
- Enables navigation between views
