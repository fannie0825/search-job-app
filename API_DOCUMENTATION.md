# API Documentation

This document describes all the APIs used in the application.

## 📡 APIs Used

The application uses **3 main APIs**:

### 1. **Azure OpenAI API** (Primary AI Service)

Used for two purposes:

#### A. Text Embeddings API
- **Purpose**: Semantic job search (vector embeddings)
- **Endpoint**: `{endpoint}/deployments/text-embedding-3-small/embeddings`
- **Model**: `text-embedding-3-small`
- **API Version**: `2024-02-01`
- **Authentication**: API Key (via `api-key` header)
- **Usage**: 
  - Converts job descriptions into vector embeddings
  - Converts user search queries into embeddings
  - Enables semantic similarity matching

**Code Location**: `APIMEmbeddingGenerator` class (lines 820-962)

**Key Methods**:
- `get_embedding(text)`: Returns `(embedding, tokens_used)` tuple
- `get_embeddings_batch(texts, batch_size)`: Returns `(embeddings, total_tokens_used)` tuple
- Both methods use `api_call_with_retry()` for automatic rate limit handling

**Example Request**:
```python
POST {endpoint}/deployments/text-embedding-3-small/embeddings?api-version=2024-02-01
Headers:
  api-key: {AZURE_OPENAI_API_KEY}
  Content-Type: application/json
Body:
{
  "input": "software developer python",
  "model": "text-embedding-3-small"
}
```

#### B. Chat Completions API
- **Purpose**: 
  - Generate tailored resumes
  - Extract structured information from uploaded resumes
- **Endpoint**: `{endpoint}/openai/deployments/gpt-4o-mini/chat/completions`
- **Model**: `gpt-4o-mini`
- **API Version**: `2024-02-01`
- **Authentication**: API Key (via `api-key` header)
- **Usage**:
  - Resume generation: Creates tailored resumes based on user profile and job posting
  - Resume parsing: Extracts structured data from uploaded resume text

**Code Location**: `AzureOpenAITextGenerator` class (lines 141-200)

**Example Request (Resume Generation)**:
```python
POST {endpoint}/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-01
Headers:
  api-key: {AZURE_OPENAI_API_KEY}
  Content-Type: application/json
Body:
{
  "messages": [
    {"role": "system", "content": "You are a professional resume writer..."},
    {"role": "user", "content": "Create a tailored resume..."}
  ],
  "max_tokens": 2000,
  "temperature": 0.7
}
```

**Example Request (Resume Parsing)**:
```python
POST {endpoint}/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-01
Headers:
  api-key: {AZURE_OPENAI_API_KEY}
  Content-Type: application/json
Body:
{
  "messages": [
    {"role": "system", "content": "You are a resume parser..."},
    {"role": "user", "content": "Extract structured information from resume..."}
  ],
  "max_tokens": 2000,
  "temperature": 0.3
}
```

### 2. **RapidAPI - Indeed Scraper API** (Job Search)

- **Purpose**: Fetch real job postings from Indeed
- **Endpoint**: `https://indeed-scraper-api.p.rapidapi.com/api/job`
- **Provider**: RapidAPI
- **Authentication**: RapidAPI Key (via `x-rapidapi-key` header)
- **Usage**: Searches and retrieves job listings from Indeed

**Code Location**: `IndeedScraperAPI` class (lines 202-273)

**Example Request**:
```python
POST https://indeed-scraper-api.p.rapidapi.com/api/job
Headers:
  Content-Type: application/json
  x-rapidapi-host: indeed-scraper-api.p.rapidapi.com
  x-rapidapi-key: {RAPIDAPI_KEY}
Body:
{
  "scraper": {
    "maxRows": 15,
    "query": "software developer",
    "location": "Hong Kong",
    "jobType": "fulltime",
    "radius": "50",
    "sort": "relevance",
    "fromDays": "7",
    "country": "hk"
  }
}
```

## 🔑 API Keys Required

All API keys are stored in `.streamlit/secrets.toml`:

```toml
AZURE_OPENAI_API_KEY = "your-azure-openai-api-key"
AZURE_OPENAI_ENDPOINT = "https://your-resource.openai.azure.com/"
RAPIDAPI_KEY = "your-rapidapi-key"
```

## 📊 API Usage Summary

| API | Purpose | Model/Service | Cost |
|-----|---------|---------------|------|
| Azure OpenAI Embeddings | Semantic search | text-embedding-3-small | Pay-per-token |
| Azure OpenAI Chat | Resume generation & parsing | gpt-4o-mini | Pay-per-token |
| RapidAPI Indeed Scraper | Job search | Indeed Scraper API | Subscription-based |

## 🔧 API Configuration

### Azure OpenAI Setup
1. Create Azure OpenAI resource in Azure Portal
2. Deploy models:
   - `text-embedding-3-small` (for embeddings)
   - `gpt-4o-mini` (for text generation)
3. Get API key and endpoint from Azure Portal
4. Update deployment names in code if different

### RapidAPI Setup
1. Sign up at [RapidAPI](https://rapidapi.com)
2. Subscribe to [Indeed Scraper API](https://rapidapi.com/indeed-scraper-api/api/indeed-scraper-api)
3. Get your RapidAPI key from dashboard

## 📝 API Endpoints Used

### Azure OpenAI Endpoints

1. **Embeddings Endpoint**:
   ```
   {endpoint}/deployments/text-embedding-3-small/embeddings?api-version=2024-02-01
   ```

2. **Chat Completions Endpoint**:
   ```
   {endpoint}/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-01
   ```

### RapidAPI Endpoint

1. **Indeed Scraper Endpoint**:
   ```
   https://indeed-scraper-api.p.rapidapi.com/api/job
   ```

## 🛠️ HTTP Methods

- **POST**: All API calls use POST method
- **Headers**: JSON content type, API key authentication
- **Timeout**: 
  - Embeddings: 30 seconds
  - Chat completions: 60 seconds
  - Job search: 60 seconds

## 🔄 API Call Flow

### Resume Generation Flow:
```
User Profile + Job Posting 
  → Azure OpenAI Chat API 
  → Tailored Resume
```

### Resume Parsing Flow:
```
Uploaded Resume File 
  → Extract Text (PDF/DOCX/TXT) 
  → Azure OpenAI Chat API 
  → Structured Profile Data
```

### Job Search Flow:
```
User Query 
  → RapidAPI Indeed Scraper 
  → Job Listings
```

### Semantic Search Flow:
```
Job Listings 
  → Azure OpenAI Embeddings 
  → Vector Database 
  → User Query Embedding 
  → Cosine Similarity 
  → Ranked Results
```

## ⚠️ Error Handling

All API calls include:
- Try-catch blocks for exception handling
- HTTP status code checking
- User-friendly error messages
- Graceful fallbacks where possible

## 🔄 Rate Limiting & Retry Logic

### Exponential Backoff Strategy

The application uses a sophisticated rate limiting strategy to handle API rate limits gracefully:

1. **`api_call_with_retry()` Function** (lines 173-240):
   - Implements exponential backoff for 429 (Rate Limit) errors
   - Automatically retries with increasing delays (1s, 2s, 4s, etc.)
   - Respects server-provided `Retry-After` headers when available
   - Maximum delay capped at 60 seconds (configurable)
   - Shows user-friendly progress messages during retries

2. **Embedding API Rate Limiting**:
   - **No conflicting throttling**: Removed basic 100ms throttling that conflicted with exponential backoff
   - **Batch processing**: Uses configurable batch delays (`EMBEDDING_BATCH_DELAY`) between successful batches
   - **Automatic retry**: All embedding calls use `api_call_with_retry()` which handles 429 errors automatically
   - **Token tracking**: Returns token usage instead of mutating cached objects (prevents Streamlit cache issues)

3. **Configuration** (via environment variables or Streamlit secrets):
   - `EMBEDDING_BATCH_SIZE`: Number of texts to process per batch (default: 20)
   - `EMBEDDING_BATCH_DELAY`: Delay in seconds between batches (default: 1)
   - Retry parameters: `max_retries=3`, `initial_delay=1`, `max_delay=60`

### Token Usage Tracking

- **Embedding Generator**: Returns `(embedding, tokens_used)` tuple instead of mutating cached objects
- **Callers**: Update `st.session_state.token_tracker` directly to avoid cache invalidation
- **Benefits**: Prevents Streamlit cache confusion and ensures accurate token tracking

### Best Practices

1. **Let exponential backoff handle rate limits**: Don't add additional throttling that conflicts with retry logic
2. **Avoid mutating cached objects**: Return values instead of mutating cached resources
3. **Respect server hints**: The retry logic automatically uses `Retry-After` headers when provided
4. **User feedback**: Progress messages inform users when rate limits are encountered

## 📚 Additional Resources

- [Azure OpenAI Documentation](https://learn.microsoft.com/azure/ai-services/openai/)
- [RapidAPI Indeed Scraper](https://rapidapi.com/indeed-scraper-api/api/indeed-scraper-api)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference)

---

**Last Updated**: 2025-01-28

## 🔧 Recent Improvements (2025-01-28)

### Rate Limiting Fixes
- ✅ Removed conflicting 100ms throttling that interfered with exponential backoff
- ✅ Removed `rate_limit_encountered` flag (redundant with `api_call_with_retry()`)
- ✅ Simplified rate limit handling to rely solely on exponential backoff
- ✅ Fixed token tracker mutation issue in cached objects

### Token Tracking Improvements
- ✅ Embedding methods now return token usage instead of mutating cached objects
- ✅ Callers update `st.session_state.token_tracker` directly
- ✅ Prevents Streamlit cache invalidation issues
