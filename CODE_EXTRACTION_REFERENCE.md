# Code Extraction Reference - Line Numbers in app.py

This document provides exact line numbers for extracting code from `app.py` into modules.

## Utils Module (Already Extracted)

- Configuration: Lines 112-181
- Helper functions: Lines 52-426
- API client classes: Lines 1624-2372

## Resume Upload Module

### File: `modules/resume_upload/file_extraction.py`
- `extract_text_from_resume()`: Lines 3228-3261

### File: `modules/resume_upload/profile_extraction.py`
- `extract_relevant_resume_sections()`: Lines 3263-3362
- `extract_profile_from_resume()`: Lines 3364-3559

## Semantic Search Module

### File: `modules/semantic_search/job_search.py`
- `SemanticJobSearch` class: Lines 2385-2666
  - `__init__()`: Lines 2386-2424
  - `_get_job_hash()`: Lines 2426-2429
  - `index_jobs()`: Lines 2431-2521
  - `search()`: Lines 2523-2564
  - `calculate_skill_match()`: Lines 2566-2649
  - `_calculate_skill_match_string_based()`: Lines 2651-2666

### File: `modules/semantic_search/cache.py`
- `is_cache_valid()`: Lines 2668-2688
- `_build_jobs_cache_key()`: Lines 2691-2701
- `_ensure_jobs_cache_structure()`: Lines 2703-2718
- `_get_cached_jobs()`: Lines 2720-2731
- `_store_jobs_in_cache()`: Lines 2733-2751
- `fetch_jobs_with_cache()`: Lines 2753-2795

### File: `modules/semantic_search/embeddings.py`
- `generate_and_store_resume_embedding()`: Lines 2842-2874

## Analysis Module

### File: `modules/analysis/match_analysis.py`
- `extract_salary_from_text()`: Lines 2919-3005
- `extract_salary_from_text_regex()`: Lines 3006-3041
- `calculate_salary_band()`: Lines 3042-3071
- `filter_jobs_by_domains()`: Lines 3072-3110
- `filter_jobs_by_salary()`: Lines 3111-3152

## Resume Generator Module

### File: `modules/resume_generator/formatters.py`
- `render_structured_resume_editor()`: Lines 3703-3874
- `generate_docx_from_json()`: Lines 3875-3989
- `format_resume_as_text()`: Lines 5256-5336
- `generate_pdf_from_json()`: Lines 5109-5255

## UI Module

### File: `modules/ui/job_cards.py`
- `display_job_card()`: Lines 3153-3226

### File: `modules/ui/dashboard.py`
- `display_user_profile()`: Lines 3560-3702
- `display_match_score_feedback()`: Lines 3990-4034
- `display_skill_matching_matrix()`: Lines 4468-4593
- `display_market_positioning_profile()`: Lines 4594-4690
- `display_refine_results_section()`: Lines 4691-4829
- `display_ranked_matches_table()`: Lines 4830-4988
- `display_match_breakdown()`: Lines 4989-5108

### File: `modules/ui/sidebar.py`
- `render_sidebar()`: Lines 4221-4466

### File: `modules/ui/hero_banner.py`
- `render_hero_banner()`: Lines 5364-5392

### File: `modules/ui/resume_editor.py`
- `display_resume_generator()`: Lines 4035-4220

## Factory Functions (Already in utils/api_clients.py)

- `get_token_tracker()`: Lines 2797-2801
- `_create_embedding_generator_resource()`: Lines 2805-2806
- `_create_text_generator_resource()`: Lines 2810-2811
- `get_embedding_generator()`: Lines 2813-2840
- `get_job_scraper()`: Lines 2876-2889
- `get_text_generator()`: Lines 2891-2917

## Validation Functions

- `validate_secrets()`: Lines 5337-5363

## Main Function

- `main()`: Lines 5394-5451

## Notes

- Line numbers are approximate and may vary slightly
- Always check the function/class names to ensure correct extraction
- Update imports after extraction
- Test after each module extraction
