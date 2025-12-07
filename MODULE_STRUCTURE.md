# Module Structure for CareerLens Application

This document outlines the modular structure for the CareerLens application.

## Module Organization

### 1. `modules/utils/`
**Purpose**: Shared utilities, configuration, and helper functions

**Files**:
- `config.py` - Configuration constants and environment setup
- `helpers.py` - API retry logic, memory management, WebSocket keepalive
- `api_clients.py` - API client classes and factory functions
- `__init__.py` - Module exports

**Key Classes/Functions**:
- `APIMEmbeddingGenerator` - Azure OpenAI embedding generation
- `AzureOpenAITextGenerator` - Azure OpenAI text generation
- `RateLimiter` - Rate limiting for API calls
- `IndeedScraperAPI` - Job scraping via RapidAPI
- `TokenUsageTracker` - Token usage tracking
- `api_call_with_retry()` - Retry logic with exponential backoff
- Configuration constants (DEFAULT_EMBEDDING_BATCH_SIZE, etc.)

### 2. `modules/resume_upload/`
**Purpose**: Resume file handling and profile extraction

**Files**:
- `file_extraction.py` - Extract text from PDF/DOCX/TXT files
- `profile_extraction.py` - Extract structured profile from resume text
- `__init__.py` - Module exports

**Key Functions**:
- `extract_text_from_resume()` - Extract text from uploaded file
- `extract_relevant_resume_sections()` - Extract Experience/Education sections
- `extract_profile_from_resume()` - AI-powered profile extraction

### 3. `modules/semantic_search/`
**Purpose**: Job search, embeddings, and semantic matching

**Files**:
- `job_search.py` - Job search functionality
- `embeddings.py` - Embedding generation and storage
- `matching.py` - Semantic matching and similarity calculation
- `cache.py` - Job search caching
- `__init__.py` - Module exports

**Key Classes/Functions**:
- `SemanticJobSearch` - Main semantic search class
- `fetch_jobs_with_cache()` - Fetch jobs with caching
- `generate_and_store_resume_embedding()` - Resume embedding generation
- `is_cache_valid()` - Cache validation
- Job filtering functions

### 4. `modules/analysis/`
**Purpose**: Job match analysis, summaries, and insights

**Files**:
- `match_analysis.py` - Match score calculation and analysis
- `skill_matching.py` - Skill-based matching
- `market_positioning.py` - Market positioning analysis
- `summaries.py` - Generate summaries and insights
- `__init__.py` - Module exports

**Key Functions**:
- `calculate_salary_band()` - Salary analysis
- `filter_jobs_by_domains()` - Domain filtering
- `filter_jobs_by_salary()` - Salary filtering
- Skill matching calculations
- Market positioning profile generation

### 5. `modules/resume_generator/`
**Purpose**: Generative tailored resume creation

**Files**:
- `generator.py` - Resume generation logic
- `formatters.py` - Resume formatting (PDF, DOCX, text)
- `__init__.py` - Module exports

**Key Functions**:
- `generate_resume()` - Generate tailored resume (in AzureOpenAITextGenerator)
- `generate_docx_from_json()` - Export to DOCX
- `generate_pdf_from_json()` - Export to PDF
- `format_resume_as_text()` - Format as text
- `render_structured_resume_editor()` - Resume editor UI

### 6. `modules/ui/`
**Purpose**: Streamlit UI components and rendering

**Files**:
- `sidebar.py` - Sidebar component
- `hero_banner.py` - Hero banner component
- `job_cards.py` - Job card display
- `dashboard.py` - Dashboard displays
- `resume_editor.py` - Resume editor UI
- `__init__.py` - Module exports

**Key Functions**:
- `render_sidebar()` - Render sidebar
- `render_hero_banner()` - Render hero banner
- `display_job_card()` - Display job card
- `display_user_profile()` - Display user profile
- `display_market_positioning_profile()` - Market positioning display
- `display_ranked_matches_table()` - Ranked matches table
- `display_match_breakdown()` - Match breakdown display
- `display_resume_generator()` - Resume generator UI

## Main App File

The main `app.py` file will be simplified to:
1. Import all modules
2. Initialize Streamlit page config
3. Initialize session state
4. Call main UI rendering functions
5. Handle main application flow

## Benefits of This Structure

1. **Modularity**: Each module has a clear, single responsibility
2. **Maintainability**: Easier to find and update specific functionality
3. **Testability**: Each module can be tested independently
4. **Reusability**: Modules can be reused in other projects
5. **Clarity**: Clear separation of concerns
