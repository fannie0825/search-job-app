# Python Code Data Flow Summary

## Overview
This document describes the data flow and logic of the `app.py` Streamlit application, which is a job matching system that uses semantic search and AI to match user resumes with job postings.

---

## 1. Application Entry Point

**Function:** `main()` (line 4627)

**Flow:**
1. Checks if resume generator should be shown (`show_resume_generator` flag)
2. Renders sidebar with controls (`render_sidebar()`)
3. If dashboard is ready and matched jobs exist, displays:
   - Market positioning profile
   - Refine results section
   - Ranked matches table
   - Match breakdown

---

## 2. Resume Upload & Text Extraction Flow

**Trigger:** User uploads PDF/DOCX file in sidebar

**Functions Involved:**
- `render_sidebar()` → `extract_text_from_resume()` (line 2607)
- `generate_and_store_resume_embedding()` (line 2202)
- `extract_profile_from_resume()` (line 2743)

**Data Flow:**

```
User Uploads File (PDF/DOCX)
    ↓
extract_text_from_resume()
    ├─ PDF: PyPDF2.PdfReader → Extract text from all pages
    └─ DOCX: python-docx Document → Extract paragraphs
    ↓
resume_text stored in st.session_state.resume_text
    ↓
generate_and_store_resume_embedding()
    ├─ Builds resume query: resume_text + profile_data (if available)
    ├─ Calls get_embedding_generator() → APIMEmbeddingGenerator
    ├─ Generates embedding via Azure OpenAI API
    ├─ Tracks tokens via TokenUsageTracker
    └─ Stores embedding in st.session_state.resume_embedding
    ↓
extract_profile_from_resume() [Two-Pass Extraction]
    ├─ PASS 1: Initial extraction
    │   ├─ Builds prompt with full resume text
    │   ├─ Calls Azure OpenAI GPT-4o-mini via get_text_generator()
    │   ├─ Extracts: name, email, phone, location, summary, experience, education, skills, certifications
    │   └─ Returns JSON profile data
    │
    └─ PASS 2: Self-correction (verification)
        ├─ extract_relevant_resume_sections() → Only Experience & Education sections
        ├─ Builds verification prompt with Pass 1 data + relevant sections
        ├─ Calls Azure OpenAI again to verify dates, company names, job titles
        └─ Returns corrected profile data
    ↓
Profile stored in st.session_state.user_profile
```

**Key Data Structures:**
- `resume_text`: Raw text string
- `resume_embedding`: Vector embedding (1536 dimensions for text-embedding-3-small)
- `user_profile`: Dictionary with keys: name, email, phone, location, summary, experience, education, skills, certifications

---

## 3. Job Fetching Flow

**Trigger:** User clicks "Analyze Profile & Find Matches" button

**Functions Involved:**
- `render_sidebar()` → `get_job_scraper()` (line 2236)
- `fetch_jobs_with_cache()` (line 2113)
- `MultiSourceJobAggregator.search_jobs()` (line 1691)
- `IndeedScraperAPI.search_jobs()` (line 1434) or `LinkedInJobsAPI.search_jobs()` (line 1541)

**Data Flow:**

```
User Clicks "Analyze Profile & Find Matches"
    ↓
Profile Analysis (AI Inference)
    ├─ Domain Inference:
    │   ├─ Builds prompt from user profile (summary + experience + skills)
    │   ├─ Calls Azure OpenAI to infer target domains (FinTech, ESG, Data Analytics, etc.)
    │   └─ Returns JSON: {"domains": [...], "reasoning": "..."}
    │
    └─ Salary Inference:
        ├─ Builds prompt from user profile
        ├─ Calls Azure OpenAI to estimate minimum salary (HKD monthly)
        └─ Returns JSON: {"min_salary_hkd_monthly": <number>, "reasoning": "..."}
    ↓
get_job_scraper() → MultiSourceJobAggregator
    ├─ Primary: IndeedScraperAPI (if not USE_LINKEDIN_ONLY)
    └─ Fallback: LinkedInJobsAPI
    ↓
fetch_jobs_with_cache()
    ├─ Checks cache: _get_cached_jobs() (TTL: 168 hours default)
    ├─ If cache hit: Returns cached jobs (skips API call)
    └─ If cache miss: Proceeds to API call
    ↓
MultiSourceJobAggregator.search_jobs()
    ├─ Try Primary Source (Indeed):
    │   ├─ RateLimiter.wait_if_needed() → Enforces max requests/minute
    │   ├─ IndeedScraperAPI.search_jobs()
    │   │   ├─ POST to RapidAPI Indeed endpoint
    │   │   ├─ api_call_with_retry() → Handles 429 errors with exponential backoff
    │   │   ├─ Parses response: _parse_job() → Standardizes job format
    │   │   └─ Returns list of job dictionaries
    │   └─ If QuotaExceededError: Mark indeed_quota_exceeded = True
    │
    └─ Try Fallback Source (LinkedIn) if primary failed or insufficient results:
        ├─ LinkedInJobsAPI.search_jobs()
        │   ├─ RateLimiter.wait_if_needed()
        │   ├─ GET to RapidAPI LinkedIn endpoint (paginated)
        │   ├─ api_call_with_retry() → Handles retries
        │   ├─ _filter_jobs() → Filters by query/location if needed
        │   ├─ _parse_job() → Standardizes job format
        │   └─ Returns list of job dictionaries
        │
    └─ Deduplicate: Remove jobs with same (title, company)
    ↓
filter_jobs_by_domains() → Filters jobs matching inferred domains
filter_jobs_by_salary() → Filters jobs meeting minimum salary
    ↓
Jobs stored in memory (not yet in session_state)
```

**Key Data Structures:**
- **Job Dictionary Format:**
  ```python
  {
      'title': str,
      'company': str,
      'location': str,
      'description': str,  # Full description (up to 50,000 chars)
      'salary': str,
      'job_type': str,
      'url': str,
      'posted_date': str,
      'benefits': list,
      'skills': list,  # Up to 10 skills
      'company_rating': float,
      'is_remote': bool
  }
  ```

**Caching Strategy:**
- Cache key: `query|location|max_rows|job_type|country`
- TTL: 168 hours (7 days) by default
- Cache stored in `st.session_state.jobs_cache` (dict keyed by cache_key)

---

## 4. Semantic Matching Flow

**Trigger:** After jobs are fetched

**Functions Involved:**
- `SemanticJobSearch.__init__()` (line 1788)
- `SemanticJobSearch.index_jobs()` (line 1816) - **Currently Disabled** (line 3772)
- `SemanticJobSearch.search()` (line 1908)
- `generate_and_store_resume_embedding()` (if not already done)

**Data Flow:**

```
Jobs Fetched (list of job dictionaries)
    ↓
SemanticJobSearch initialized
    ├─ embedding_gen: APIMEmbeddingGenerator instance
    ├─ use_persistent_store: True (default)
    ├─ ChromaDB initialization:
    │   ├─ Creates/connects to .chroma_db directory
    │   └─ Gets/creates collection "job_embeddings" (cosine similarity)
    │
    └─ NOTE: index_jobs() is currently DISABLED (line 3772)
        └─ This means job embeddings are NOT generated/stored
    ↓
Resume Embedding Check
    ├─ If st.session_state.resume_embedding exists: Use it
    └─ If not: generate_and_store_resume_embedding()
        ├─ Builds query: resume_text + profile_data
        ├─ Calls APIMEmbeddingGenerator.get_embedding()
        │   ├─ POST to Azure OpenAI embeddings endpoint
        │   ├─ api_call_with_retry() → Handles rate limits
        │   └─ Returns (embedding_vector, tokens_used)
        └─ Stores in st.session_state.resume_embedding
    ↓
SemanticJobSearch.search()
    ├─ Input: resume_embedding (pre-computed) OR query string
    ├─ Since index_jobs() is disabled, job_embeddings is empty
    ├─ Returns empty list [] (no semantic matching occurs)
    │
    └─ [IF index_jobs() were enabled]:
        ├─ For each job: Build text = "title at company. description Skills: ..."
        ├─ Check ChromaDB for existing embeddings (by job hash)
        ├─ Generate embeddings for new jobs only (batch processing)
        ├─ Store in ChromaDB with job hash as ID
        ├─ Retrieve all embeddings (existing + new)
        └─ Calculate cosine similarity: resume_embedding vs all job_embeddings
        └─ Return top_k results sorted by similarity
    ↓
Results: Currently returns empty list (semantic matching disabled)
```

**Current State:**
- **Semantic matching is DISABLED** (line 3772: `# search_engine.index_jobs(jobs, max_jobs_to_index=jobs_to_index_limit)`)
- This means the system currently relies on skill-based matching only (see Section 5)

**If Enabled, Data Flow Would Be:**
```
index_jobs()
    ├─ Build job texts: "title at company. description Skills: skill1, skill2..."
    ├─ Generate job hashes (MD5 of title+company+url)
    ├─ Check ChromaDB for existing embeddings
    ├─ Batch generate embeddings for new jobs:
    │   ├─ APIMEmbeddingGenerator.get_embeddings_batch()
    │   │   ├─ Splits into batches (default: 20 jobs/batch)
    │   │   ├─ POST to Azure OpenAI (batch API)
    │   │   ├─ Handles rate limits with exponential backoff
    │   │   └─ Returns (embeddings_list, total_tokens)
    │   └─ Store in ChromaDB: upsert(ids=[hash], embeddings=[emb], documents=[text])
    └─ Retrieve all embeddings: collection.get(ids=[hashes])
    ↓
search()
    ├─ Use resume_embedding (1536-dim vector)
    ├─ Calculate cosine_similarity(resume_embedding, job_embeddings_matrix)
    ├─ Get top_k indices (highest similarity)
    └─ Return results: [{'job': job_dict, 'similarity_score': float, 'rank': int}, ...]
```

---

## 5. Skill Matching Flow

**Trigger:** After semantic search (or directly on jobs if semantic is disabled)

**Functions Involved:**
- `SemanticJobSearch.calculate_skill_match()` (line 1951)
- `SemanticJobSearch._calculate_skill_match_string_based()` (line 2011) - Fallback

**Data Flow:**

```
For each job in results (or all jobs if semantic disabled):
    ↓
SemanticJobSearch.calculate_skill_match(user_skills, job_skills)
    ├─ Parse skills:
    │   ├─ user_skills: Split by comma → list
    │   └─ job_skills: Already a list (from job dictionary)
    │
    ├─ Try Semantic Matching:
    │   ├─ Generate embeddings for user skills (batch)
    │   ├─ Generate embeddings for job skills (batch)
    │   ├─ Calculate similarity matrix: cosine_similarity(job_skills_emb, user_skills_emb)
    │   ├─ For each job skill: Find best matching user skill (threshold: 0.7)
    │   ├─ Calculate match_score = matched_skills_count / total_job_skills
    │   └─ Return (match_score, missing_skills[:5])
    │
    └─ Fallback to String Matching (if semantic fails):
        ├─ Convert all to lowercase
        ├─ Check if job_skill in user_skill or user_skill in job_skill
        ├─ Calculate match_score = matched_skills_count / total_job_skills
        └─ Return (match_score, missing_skills[:5])
    ↓
Add to result:
    ├─ result['skill_match_score'] = match_score (0.0 to 1.0)
    └─ result['missing_skills'] = missing_skills (list of up to 5)
    ↓
Sort results by skill_match_score (highest first)
    ↓
Store in st.session_state.matched_jobs
```

**Key Metrics:**
- `skill_match_score`: Percentage of job skills matched by user (0.0 to 1.0)
- `missing_skills`: List of job skills not found in user profile (max 5)

---

## 6. Display & Ranking Flow

**Trigger:** After matched_jobs are stored, `st.rerun()` is called

**Functions Involved:**
- `display_market_positioning_profile()` (line 3943)
- `display_refine_results_section()` (line 4040)
- `display_ranked_matches_table()` (line 4161)
- `display_match_breakdown()` (line 4290)

**Data Flow:**

```
st.session_state.matched_jobs populated
st.session_state.dashboard_ready = True
st.rerun() called
    ↓
main() executes again
    ├─ render_sidebar() → Shows filters and controls
    └─ Dashboard sections displayed:
        │
        ├─ display_market_positioning_profile()
        │   ├─ Calculates market statistics:
        │   │   ├─ Average salary across matched jobs
        │   │   ├─ Salary range (min/max)
        │   │   ├─ Top skills in demand
        │   │   └─ Industry distribution
        │   └─ Displays cards with market insights
        │
        ├─ display_refine_results_section()
        │   ├─ Provides filters: industry, salary range, job type
        │   └─ Applies filters to matched_jobs (in-memory, not persisted)
        │
        ├─ display_ranked_matches_table()
        │   ├─ Shows table of matched jobs
        │   ├─ Columns: Rank, Job Title, Company, Location, Match Score, Actions
        │   ├─ Match Score = skill_match_score (since semantic is disabled)
        │   └─ Actions: "Apply" button, "Resume" button (triggers resume generator)
        │
        └─ display_match_breakdown()
            ├─ For selected job: Shows detailed breakdown
            ├─ Displays: job description, required skills, missing skills
            └─ Shows match score feedback
```

**Ranking Logic:**
- **Primary Sort:** `skill_match_score` (descending)
- **Secondary Sort:** Not explicitly defined (maintains original order)
- **Display Order:** Top matches shown first in table

---

## 7. Resume Generation Flow

**Trigger:** User clicks "Resume" button on a job card

**Functions Involved:**
- `display_resume_generator()` (line 3387)
- `AzureOpenAITextGenerator.generate_resume()` (line 981)

**Data Flow:**

```
User Clicks "Resume" Button
    ↓
st.session_state.selected_job = job_dict
st.session_state.show_resume_generator = True
st.rerun()
    ↓
main() → Checks show_resume_generator flag
    └─ display_resume_generator()
        ├─ Gets user_profile from session_state
        ├─ Gets selected_job from session_state
        ├─ AzureOpenAITextGenerator.generate_resume()
        │   ├─ Builds prompt with:
        │   │   ├─ System instructions (ATS optimization expert)
        │   │   ├─ Job posting details (title, company, description, skills)
        │   │   ├─ User profile (structured: name, email, summary, experience, etc.)
        │   │   └─ Raw resume text (if available)
        │   ├─ POST to Azure OpenAI chat/completions endpoint
        │   ├─ api_call_with_retry() → Handles rate limits
        │   ├─ Parses JSON response (structured resume data)
        │   └─ Returns resume_data (JSON structure)
        │
        ├─ Displays resume editor (structured form)
        ├─ Allows user to edit resume sections
        └─ Export options: DOCX, PDF, Text
    ↓
User can:
    ├─ Edit resume sections
    ├─ Generate new version (calls generate_resume() again)
    └─ Export resume (generate_docx_from_json() or generate_pdf_from_json())
```

**Resume Data Structure:**
```python
{
    "personal_info": {
        "name": str,
        "email": str,
        "phone": str,
        "location": str,
        "linkedin": str,
        "portfolio": str
    },
    "summary": str,
    "experience": [
        {
            "title": str,
            "company": str,
            "location": str,
            "start_date": str,
            "end_date": str,
            "description": str,
            "achievements": list
        }
    ],
    "education": [...],
    "skills": [...],
    "certifications": [...]
}
```

---

## 8. Rate Limiting & Error Handling

**Key Mechanisms:**

### API Rate Limiting:
1. **RapidAPI Rate Limiter** (`RateLimiter` class, line 1382):
   - Tracks request times in sliding window
   - Default: 3 requests/minute (configurable)
   - Blocks requests if limit exceeded

2. **Azure OpenAI Rate Limiting** (`api_call_with_retry` function, line 174):
   - Handles 429 (rate limit) errors
   - Exponential backoff: initial_delay * (2^attempt)
   - Parses Retry-After headers
   - Max retries: 3 (default)

### Error Handling:
- **QuotaExceededError**: Raised when Indeed API quota exceeded → Switches to LinkedIn
- **Fallback Mechanisms**:
  - Semantic matching → String matching
  - Batch embeddings → Individual embeddings
  - Primary source → Fallback source

---

## 9. Token Usage Tracking

**Class:** `TokenUsageTracker` (line 1743)

**Tracking:**
- Total tokens (embedding + completion)
- Embedding tokens (separate)
- Prompt tokens (completion)
- Completion tokens (completion)
- Estimated cost (USD)

**Cost Calculation:**
- Embedding: $0.00002 per 1K tokens (text-embedding-3-small)
- GPT-4o-mini prompt: $0.00015 per 1K tokens
- GPT-4o-mini completion: $0.0006 per 1K tokens

---

## 10. Data Persistence

**Session State Variables:**
- `resume_text`: Raw resume text
- `resume_embedding`: Pre-computed embedding vector
- `user_profile`: Extracted profile dictionary
- `matched_jobs`: List of matched job results
- `jobs_cache`: Dictionary of cached job searches (TTL: 168 hours)
- `dashboard_ready`: Boolean flag
- `token_tracker`: TokenUsageTracker instance

**Persistent Storage:**
- **ChromaDB**: `.chroma_db/` directory (if enabled)
  - Stores job embeddings with job hash as ID
  - Persists across sessions
  - Currently not used (index_jobs disabled)

---

## Summary of Current Data Flow

```
1. User uploads resume
   → Extract text → Generate embedding → Extract profile (2-pass)

2. User clicks "Analyze Profile & Find Matches"
   → Infer domains & salary (AI) → Fetch jobs (Indeed/LinkedIn) → Filter by domain/salary

3. Semantic matching (DISABLED)
   → Would index jobs → Search with resume embedding → Rank by similarity

4. Skill matching (ACTIVE)
   → For each job: Calculate skill match score → Sort by score

5. Display results
   → Market positioning → Ranked table → Match breakdown

6. Resume generation (optional)
   → User selects job → Generate tailored resume (AI) → Edit & export
```

---

## Key Configuration Variables

- `DEFAULT_EMBEDDING_BATCH_SIZE`: 20 (jobs per batch)
- `DEFAULT_MAX_JOBS_TO_INDEX`: 50 (max jobs to embed)
- `EMBEDDING_BATCH_DELAY`: 1 second (between batches)
- `RAPIDAPI_MAX_REQUESTS_PER_MINUTE`: 3 (rate limit)
- Cache TTL: 168 hours (7 days)

---

## Notes

1. **Semantic matching is currently disabled** (line 3772) to save embedding costs and avoid rate limits
2. **System relies on skill-based matching** for ranking
3. **Two-pass profile extraction** ensures accuracy (especially dates and company names)
4. **Caching is aggressive** (7 days) to minimize API calls
5. **Multi-source job aggregation** with automatic failover (Indeed → LinkedIn)
6. **Rate limiting is enforced** at multiple levels (RapidAPI, Azure OpenAI)
