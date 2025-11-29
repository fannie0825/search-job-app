# Streamlit App Flow Logic Analysis

## 📋 Overview
This is a **CareerLens** application - an AI-powered career copilot for Hong Kong job market that helps users:
1. Upload and parse their resume
2. Find matching jobs using semantic search
3. Generate tailored resumes for specific positions
4. Analyze market positioning and skill gaps

---

## 🔄 Main Application Flow

### **Entry Point: `main()` Function (Line 2554)**

The application follows a **conditional rendering pattern** based on session state:

```python
if show_resume_generator:
    → display_resume_generator()  # Resume generation view
else:
    → render_sidebar()            # Main dashboard view
    → display_dashboard()          # If dashboard_ready
```

---

## 🎯 Core Flow Paths

### **Path 1: Initial Setup & Profile Creation**

```
1. User opens app
   ↓
2. Session state initialized (lines 547-586)
   - search_history, jobs_cache, user_profile, etc.
   ↓
3. Sidebar rendered (render_sidebar, line 2029)
   ↓
4. User uploads resume (optional)
   - extract_text_from_resume() (line 1360)
   - extract_profile_from_resume() (line 1395)
   - Updates st.session_state.user_profile
   ↓
5. User sets market filters:
   - Target domains (FinTech, ESG, etc.)
   - Salary expectation (HKD slider)
   ↓
6. User clicks "Analyze Profile & Find Matches"
```

### **Path 2: Job Search & Matching**

```
1. "Analyze Profile & Find Matches" clicked (line 2105)
   ↓
2. Fetch jobs from Indeed API (line 2119)
   - IndeedScraperAPI.search_jobs()
   - Returns 25 jobs initially
   ↓
3. Apply filters (lines 2126-2132)
   - filter_jobs_by_domains() (line 1230)
   - filter_jobs_by_salary() (line 1261)
   ↓
4. Semantic indexing (line 2146-2148)
   - SemanticJobSearch.index_jobs()
   - Generates embeddings for all jobs using Azure OpenAI
   - Progress bar shows batch processing (10 jobs at a time)
   ↓
5. Build search query from user profile (lines 2151-2157)
   - Combines: resume_text + summary + experience + skills
   ↓
6. Semantic search (line 2159)
   - SemanticJobSearch.search()
   - Generates query embedding
   - Calculates cosine similarity with all job embeddings
   - Returns top 15 matches ranked by similarity
   ↓
7. Calculate skill matches (lines 2161-2167)
   - For each matched job:
     - calculate_skill_match() (line 1117)
     - Compares user skills vs job required skills
     - Identifies missing skills
   ↓
8. Store results in session state (line 2169)
   - st.session_state.matched_jobs = results
   - st.session_state.dashboard_ready = True
   ↓
9. Rerun app to show dashboard
```

### **Path 3: Dashboard Display**

```
1. Dashboard ready check (line 2564)
   ↓
2. Display Market Positioning Profile (line 2570)
   - display_market_positioning_profile() (line 2175)
   - Calculates 4 key metrics:
     a. Estimated Market Salary Band (line 2189)
     b. Target Role Seniority (line 2206)
     c. Top Skill Gap (line 2210)
     d. Recommended Accreditation (line 2230)
   ↓
3. Display Ranked Matches Table (line 2576)
   - display_ranked_matches_table() (line 2269)
   - Creates interactive DataFrame with:
     - Match Score (semantic + skill / 2)
     - Job Title, Company, Location
     - Key Matching Skills
     - Missing Critical Skill
   - User can select a row
   ↓
4. Display Match Breakdown (line 2582)
   - display_match_breakdown() (line 2394)
   - Shows detailed analysis for selected job:
     - Semantic score breakdown
     - Skill overlap percentage
     - AI-generated recruiter note
     - "Tailor Resume" button
```

### **Path 4: Resume Generation**

```
1. User clicks "Tailor Resume for this Job" (line 2460)
   OR clicks "📄 Resume" button on job card (line 1355)
   ↓
2. Sets session state (lines 2461-2462):
   - st.session_state.selected_job = job
   - st.session_state.show_resume_generator = True
   ↓
3. App reruns → shows resume generator view
   ↓
4. display_resume_generator() called (line 1864)
   ↓
5. User clicks "Generate Tailored Resume" (line 1909)
   ↓
6. Resume generation (lines 1910-1941):
   a. Get text generator (AzureOpenAI GPT-4o-mini)
   b. Call generate_resume() (line 656)
      - Uses "Context Sandwich" approach:
        * System instructions
        * Job description
        * Structured profile
        * Raw resume text (if available)
      - Returns structured JSON resume
   c. Calculate match score (lines 1924-1934)
      - calculate_match_score() (line 781)
      - Generates embeddings for resume & job
      - Cosine similarity = match score
      - Extracts missing keywords using AI
   d. Store in session state
   ↓
7. Display match score feedback (line 1944)
   - display_match_score_feedback() (line 1819)
   - Shows percentage, color coding, missing keywords
   ↓
8. Display structured resume editor (line 1956)
   - render_structured_resume_editor() (line 1602)
   - Editable form with all resume sections:
     * Header (name, contact info)
     * Summary
     * Skills
     * Experience (with bullet points)
     * Education
     * Certifications
   ↓
9. Download options (lines 1964-2012):
   - Download as DOCX (line 1969)
   - Download as JSON (line 1984)
   - Download as TXT (line 1995)
   - Apply to Job link (line 2007)
```

---

## 🏗️ Key Components & Classes

### **1. APIMEmbeddingGenerator (Line 588)**
- **Purpose**: Generate text embeddings using Azure OpenAI
- **Key Methods**:
  - `get_embedding(text)`: Single embedding
  - `get_embeddings_batch(texts, batch_size=10)`: Batch processing with progress bar
- **Used for**: Job indexing, semantic search, match scoring

### **2. AzureOpenAITextGenerator (Line 642)**
- **Purpose**: Generate text using GPT-4o-mini
- **Key Methods**:
  - `generate_resume()`: Creates tailored resume JSON
  - `calculate_match_score()`: Compares resume vs job description
  - `analyze_seniority_level()`: Determines job seniority
  - `recommend_accreditations()`: Suggests certifications
  - `generate_recruiter_note()`: Creates personalized feedback
- **Used for**: Resume generation, AI analysis, keyword extraction

### **3. IndeedScraperAPI (Line 995)**
- **Purpose**: Fetch job listings from Indeed via RapidAPI
- **Key Methods**:
  - `search_jobs(query, location, max_rows, job_type, country)`
  - `_parse_job(job_data)`: Parses API response into structured format
- **Returns**: List of job dictionaries with title, company, description, skills, etc.

### **4. SemanticJobSearch (Line 1076)**
- **Purpose**: Semantic search engine for jobs
- **Key Methods**:
  - `index_jobs(jobs)`: Creates embeddings for all jobs
  - `search(query, top_k)`: Finds most similar jobs using cosine similarity
  - `calculate_skill_match()`: Compares user skills vs job skills
- **Algorithm**: Vector similarity search using scikit-learn

---

## 📊 Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    USER INPUT LAYER                          │
└─────────────────────────────────────────────────────────────┘
                            ↓
        ┌───────────────────┴───────────────────┐
        │                                       │
   [Resume Upload]                      [Market Filters]
        │                                       │
        ↓                                       ↓
┌───────────────────┐              ┌───────────────────┐
│ Profile Extraction│              │  Job Fetching     │
│ (Azure OpenAI)    │              │  (Indeed API)     │
└───────────────────┘              └───────────────────┘
        │                                       │
        └───────────────────┬───────────────────┘
                            ↓
                ┌───────────────────────┐
                │  Semantic Indexing     │
                │  (Azure Embeddings)    │
                └───────────────────────┘
                            ↓
                ┌───────────────────────┐
                │  Semantic Search       │
                │  (Cosine Similarity)  │
                └───────────────────────┘
                            ↓
                ┌───────────────────────┐
                │  Skill Matching        │
                │  (String Comparison)  │
                └───────────────────────┘
                            ↓
                ┌───────────────────────┐
                │  Dashboard Display     │
                │  (Market Metrics)     │
                └───────────────────────┘
                            ↓
                ┌───────────────────────┐
                │  Resume Generation     │
                │  (GPT-4o-mini)        │
                └───────────────────────┘
                            ↓
                ┌───────────────────────┐
                │  Match Score Analysis  │
                │  (Embeddings + AI)    │
                └───────────────────────┘
                            ↓
                ┌───────────────────────┐
                │  Download & Apply      │
                └───────────────────────┘
```

---

## 🔐 Session State Management

The app uses **extensive session state** to maintain user data across reruns:

### **Core State Variables:**
- `user_profile`: User's professional information
- `resume_text`: Raw extracted resume text
- `jobs_cache`: Cached job listings with timestamp
- `matched_jobs`: AI-ranked job matches with scores
- `generated_resume`: Structured resume JSON
- `selected_job`: Currently selected job for resume generation
- `show_resume_generator`: Navigation flag
- `dashboard_ready`: Whether to show dashboard
- `embedding_gen`: Cached embedding generator instance
- `text_gen`: Cached text generator instance

### **State Initialization Pattern:**
```python
if 'variable' not in st.session_state:
    st.session_state.variable = default_value
```

---

## 🎨 UI Component Structure

### **Main Views:**

1. **Empty State** (Line 2566)
   - Shows when dashboard not ready
   - Instructions to upload CV

2. **Dashboard View** (Lines 2569-2585)
   - Market Positioning Profile (4 metrics)
   - Ranked Matches Table (interactive DataFrame)
   - Match Breakdown (expander with details)

3. **Resume Generator View** (Line 1864)
   - Selected job display
   - Generate button
   - Match score feedback
   - Structured resume editor
   - Download buttons

4. **Sidebar** (Line 2029)
   - Resume upload
   - Market filters
   - Analyze button

---

## 🔄 Key User Interactions

### **Interaction 1: Upload Resume**
```
User uploads PDF/DOCX
  → extract_text_from_resume()
  → extract_profile_from_resume() [AI]
  → Updates user_profile in session state
  → Shows success message
```

### **Interaction 2: Analyze Profile**
```
User clicks "Analyze Profile & Find Matches"
  → Fetches jobs from Indeed
  → Applies domain/salary filters
  → Indexes jobs (generates embeddings)
  → Performs semantic search
  → Calculates skill matches
  → Stores results
  → Shows dashboard
```

### **Interaction 3: Select Job**
```
User selects row in DataFrame
  → Updates selected_job_index
  → Shows match breakdown expander
  → Displays detailed analysis
```

### **Interaction 4: Generate Resume**
```
User clicks "Tailor Resume"
  → Navigates to resume generator
  → User clicks "Generate Tailored Resume"
  → Calls GPT-4o-mini API
  → Returns structured JSON resume
  → Calculates match score
  → Shows editable resume form
  → User can download (DOCX/JSON/TXT)
```

---

## 🚀 Performance Optimizations

1. **API Instance Caching** (Lines 1143-1161)
   - Embedding generator cached in session state
   - Text generator cached in session state
   - Avoids recreating API clients on each rerun

2. **Batch Processing** (Line 613)
   - Embeddings generated in batches of 10
   - Progress bar for user feedback
   - Reduces API rate limit issues

3. **Job Caching** (Line 2138)
   - Jobs cached with timestamp
   - Can be reused without refetching

4. **Lazy Loading**
   - Resume generator only loads when needed
   - Dashboard only shows when ready

---

## 🔍 Key Algorithms

### **1. Semantic Search Algorithm**
```python
1. Generate embeddings for all jobs
2. Generate embedding for user query
3. Calculate cosine similarity: cos(θ) = (A·B) / (||A|| × ||B||)
4. Sort by similarity score (descending)
5. Return top K results
```

### **2. Skill Matching Algorithm**
```python
1. Normalize skills to lowercase
2. Split user skills by comma
3. For each job skill:
   - Check if substring match with any user skill
   - If match found, add to matched_skills
4. Calculate: match_score = len(matched_skills) / len(job_skills)
5. Return missing_skills = job_skills - matched_skills
```

### **3. Resume Generation Algorithm (Context Sandwich)**
```python
Prompt Structure:
1. System Instructions (role definition)
2. Job Description (what to match)
3. Structured Profile (user's background)
4. Raw Resume Text (original context)
5. Instructions (how to tailor)
6. JSON Schema (output format)
```

---

## 📝 Error Handling

The app includes error handling for:
- API failures (try/except blocks)
- File parsing errors (PDF/DOCX extraction)
- JSON parsing errors (resume generation)
- Missing data (null checks)
- User feedback via `st.error()`, `st.warning()`, `st.info()`

---

## 🎯 Key Design Patterns

1. **Singleton Pattern**: API instances cached in session state
2. **Factory Pattern**: Helper functions create API instances
3. **MVC Pattern**: Separation of data (state), logic (classes), view (display functions)
4. **Progressive Disclosure**: Complex features hidden until needed
5. **Defensive Programming**: Null checks, error handling throughout

---

## 🔄 Complete User Journey Example

```
1. User opens app → Empty state shown
2. User uploads resume → Profile extracted automatically
3. User selects "FinTech" domain, sets salary to 50k HKD
4. User clicks "Analyze Profile & Find Matches"
5. App fetches 25 jobs, filters to 12 FinTech jobs
6. App indexes jobs (generates embeddings)
7. App performs semantic search using user's profile
8. App calculates skill matches for each job
9. Dashboard appears showing:
   - Market salary: HKD 45k-55k/month
   - Seniority: Mid-Senior Level
   - Top skill gap: Blockchain
   - Recommended: PMP certification
10. User sees ranked table with 12 jobs
11. User clicks on row #3 (Software Engineer at FinTech Co)
12. Match breakdown shows: 85% semantic match, 70% skill match
13. User clicks "Tailor Resume for this Job"
14. Resume generator page loads
15. User clicks "Generate Tailored Resume"
16. AI generates tailored resume in JSON format
17. Match score calculated: 82%
18. User edits resume sections
19. User downloads as DOCX
20. User clicks "Apply to Job" → Opens job posting
```

---

## 🎓 Summary

This Streamlit app implements a **sophisticated AI-powered career matching system** with:

- **Semantic search** using vector embeddings
- **Skill-based matching** using string comparison
- **AI resume generation** using GPT-4o-mini
- **Market analysis** with 4 key metrics
- **Interactive dashboard** with DataFrame selection
- **Structured resume editing** with JSON format
- **Multiple export formats** (DOCX, JSON, TXT)

The flow is **well-structured** with clear separation of concerns, proper state management, and user-friendly error handling. The app follows Streamlit best practices and provides a smooth user experience for job seekers in Hong Kong.
