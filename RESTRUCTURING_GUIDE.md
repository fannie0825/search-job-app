# Code Restructuring Guide

This guide explains how the code has been restructured into modules.

## Module Structure Created

The following module structure has been created:

```
modules/
├── utils/
│   ├── __init__.py
│   ├── config.py          # Configuration constants
│   └── helpers.py         # Helper functions (retry logic, memory management)
├── resume_upload/
│   ├── __init__.py
│   ├── file_extraction.py
│   └── profile_extraction.py
├── semantic_search/
│   ├── __init__.py
│   ├── job_search.py
│   └── matching.py
├── analysis/
│   ├── __init__.py
│   └── match_analysis.py
├── resume_generator/
│   ├── __init__.py
│   └── generator.py
└── ui/
    ├── __init__.py
    ├── sidebar.py
    ├── hero_banner.py
    └── dashboard.py
```

## Next Steps

To complete the restructuring:

1. **Extract API Client Classes** from `app.py`:
   - `APIMEmbeddingGenerator` (lines ~1624-1765)
   - `AzureOpenAITextGenerator` (lines ~1767-2185)
   - `RateLimiter` (lines ~2187-2227)
   - `IndeedScraperAPI` (lines ~2230-2326)
   - `TokenUsageTracker` (lines ~2329-2372)
   - `SemanticJobSearch` (lines ~2385-2666)

2. **Extract Resume Upload Functions**:
   - `extract_text_from_resume()` (lines ~3228-3261)
   - `extract_relevant_resume_sections()` (lines ~3263-3362)
   - `extract_profile_from_resume()` (lines ~3364-3559)

3. **Extract UI Components**:
   - `render_sidebar()` (lines ~4221-4466)
   - `render_hero_banner()` (lines ~5364-5392)
   - `display_job_card()` (lines ~3153-3226)
   - All other display functions

4. **Extract Analysis Functions**:
   - `calculate_salary_band()` (lines ~3042-3071)
   - `filter_jobs_by_domains()` (lines ~3072-3110)
   - `filter_jobs_by_salary()` (lines ~3111-3152)
   - Skill matching functions

5. **Extract Resume Generator Functions**:
   - `generate_resume()` (already in AzureOpenAITextGenerator)
   - `generate_docx_from_json()` (lines ~3875-3989)
   - `generate_pdf_from_json()` (lines ~5109-5255)
   - `format_resume_as_text()` (lines ~5256-5336)

6. **Update main app.py**:
   - Import all modules
   - Keep only initialization and main() function
   - Call module functions instead of local functions

## Import Structure

Each module should import from:
- `modules.utils.*` for shared utilities
- `modules.resume_upload.*` for resume handling
- `modules.semantic_search.*` for job search
- `modules.analysis.*` for analysis
- `modules.resume_generator.*` for resume generation
- `modules.ui.*` for UI components

## Benefits

- **Easier to maintain**: Each module has a clear purpose
- **Easier to test**: Modules can be tested independently
- **Easier to extend**: New features can be added to specific modules
- **Better organization**: Related code is grouped together
