# Technical Review: Resume Upload API Calling Process

## Overview
This document provides a detailed technical review of the API calling process that occurs after a user uploads their resume in the Streamlit application. The system performs multiple API calls to extract information, generate embeddings, and prepare the resume for job matching.

---

## 1. Resume Upload Flow

### 1.1 Entry Point
**Location:** `display_user_profile()` function (line ~2629)

**Trigger:** User clicks "🔍 Extract Information from Resume" button after uploading a file (PDF, DOCX, or TXT)

**Initial Steps:**
```python
# Step 1: Extract raw text from uploaded file
resume_text = extract_text_from_resume(uploaded_file)

# Step 2: Store resume text in session state
st.session_state.resume_text = resume_text

# Step 3: Generate embedding (FIRST API CALL)
generate_and_store_resume_embedding(resume_text)

# Step 4: Extract structured profile (SECOND API CALL - Two Passes)
profile_data = extract_profile_from_resume(resume_text)
```

---

## 2. API Call #1: Resume Embedding Generation

### 2.1 Function: `generate_and_store_resume_embedding()`
**Location:** Line ~2034

### 2.2 Technical Process

#### Step 1: Text Preparation
```python
# Build resume query text
if user_profile:
    profile_data = f"{user_profile.get('summary', '')} {user_profile.get('experience', '')} {user_profile.get('skills', '')}"
    resume_query = f"{resume_text} {profile_data}"
else:
    resume_query = resume_text
```
- **Purpose:** Combines resume text with user profile data (if available) to create a richer embedding
- **Note:** If no user profile exists yet, uses only resume text

#### Step 2: Get Embedding Generator
```python
embedding_gen = get_embedding_generator()
```
- **Resource Management:** Uses `@st.cache_resource` decorator to ensure singleton instance
- **Initialization:** Creates `APIMEmbeddingGenerator` instance with Azure OpenAI credentials

#### Step 3: API Call via `APIMEmbeddingGenerator.get_embedding()`
**Location:** Line ~838

**Technical Details:**

**a) Rate Limiting Protection:**
```python
# Check if rate limit was previously encountered
if self.rate_limit_encountered:
    time.sleep(EMBEDDING_RATE_LIMIT_DELAY)

# Throttle requests (minimum 100ms between requests)
current_time = time.time()
time_since_last = current_time - self.last_request_time
min_delay = 0.1
if time_since_last < min_delay:
    time.sleep(min_delay - time_since_last)
```

**b) Request Payload:**
```python
payload = {
    "input": text,  # The resume query text
    "model": self.deployment  # "text-embedding-3-small"
}
```

**c) API Endpoint Construction:**
```python
# Endpoint normalization
endpoint = endpoint.rstrip('/')
if endpoint.endswith('/openai'):
    endpoint = endpoint[:-7]

# Final URL
self.url = f"{self.endpoint}/openai/deployments/{self.deployment}/embeddings?api-version={self.api_version}"
# Example: https://your-resource.openai.azure.com/openai/deployments/text-embedding-3-small/embeddings?api-version=2024-02-01
```

**d) Headers:**
```python
self.headers = {
    "api-key": self.api_key,
    "Content-Type": "application/json"
}
```

**e) HTTP Request:**
```python
def make_request():
    return requests.post(self.url, headers=self.headers, json=payload, timeout=30)

response = api_call_with_retry(make_request, max_retries=3)
```

**f) Response Processing:**
```python
if response and response.status_code == 200:
    result = response.json()
    embedding = result['data'][0]['embedding']  # Vector of 1536 dimensions
    
    # Reset rate limit flag on success
    self.rate_limit_encountered = False
    
    # Track token usage
    if self.token_tracker and 'usage' in result:
        tokens_used = result['usage'].get('total_tokens', 0)
        self.token_tracker.add_embedding_tokens(tokens_used)
    
    return embedding
```

**g) Error Handling:**
- **429 (Rate Limit):** Sets `rate_limit_encountered = True`, returns `None`
- **Other Errors:** Returns `None`, error logged via Streamlit

#### Step 4: Store Embedding
```python
if embedding:
    st.session_state.resume_embedding = embedding
    return embedding
```
- **Purpose:** Stores embedding in session state for reuse in all subsequent job searches
- **Optimization:** Avoids regenerating embedding on every search

---

## 3. API Call #2: Profile Extraction (Two-Pass Process)

### 3.1 Function: `extract_profile_from_resume()`
**Location:** Line ~2442

### 3.2 Technical Process Overview
This function performs **TWO sequential API calls** to extract and verify structured profile data:

1. **Pass 1:** Initial extraction of profile information
2. **Pass 2:** Self-correction to verify dates, company names, and accuracy

---

### 3.3 Pass 1: Initial Extraction

#### Step 1: Get Text Generator
```python
text_gen = get_text_generator()
```
- **Resource:** Uses `@st.cache_resource` to get singleton `AzureOpenAITextGenerator`
- **Model:** `gpt-4o-mini` deployment

#### Step 2: Construct Prompt
```python
prompt_pass1 = f"""You are an expert at parsing resumes. Extract structured information from the following resume text.

RESUME TEXT:
{resume_text}

Please extract and return the following information in JSON format:
{{
    "name": "Full name",
    "email": "Email address",
    "phone": "Phone number",
    "location": "City, State/Country",
    "linkedin": "LinkedIn URL if mentioned",
    "portfolio": "Portfolio/website URL if mentioned",
    "summary": "Professional summary or objective (2-3 sentences)",
    "experience": "Work experience in chronological order...",
    "education": "Education details...",
    "skills": "Comma-separated list of technical and soft skills",
    "certifications": "Professional certifications..."
}}
"""
```

#### Step 3: Request Payload
```python
payload_pass1 = {
    "messages": [
        {
            "role": "system",
            "content": "You are a resume parser. Extract structured information and return only valid JSON."
        },
        {
            "role": "user",
            "content": prompt_pass1
        }
    ],
    "max_tokens": 2000,
    "temperature": 0.3,  # Lower temperature for more deterministic extraction
    "response_format": {"type": "json_object"}  # Forces JSON output
}
```

#### Step 4: API Call
```python
def make_request_pass1():
    return requests.post(
        text_gen.url,  # Chat completions endpoint
        headers=text_gen.headers,
        json=payload_pass1,
        timeout=60
    )

response_pass1 = api_call_with_retry(make_request_pass1, max_retries=3)
```

**Endpoint Details:**
- **URL:** `{endpoint}/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-01`
- **Method:** POST
- **Headers:** `{"api-key": api_key, "Content-Type": "application/json"}`

#### Step 5: Response Processing
```python
if response_pass1.status_code == 200:
    result_pass1 = response_pass1.json()
    content_pass1 = result_pass1['choices'][0]['message']['content']
    
    # Track token usage
    if text_gen.token_tracker and 'usage' in result_pass1:
        usage = result_pass1['usage']
        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)
        text_gen.token_tracker.add_completion_tokens(prompt_tokens, completion_tokens)
    
    # Parse JSON
    profile_data_pass1 = json.loads(content_pass1)
```

**Error Handling:**
- **429 (Rate Limit):** Shows user-friendly error, returns `None`
- **Other Errors:** Shows error with status code and endpoint info, returns `None`
- **JSON Parse Error:** Attempts regex extraction of JSON from response

---

### 3.4 Pass 2: Self-Correction

#### Step 1: Construct Verification Prompt
```python
prompt_pass2 = f"""You are a resume quality checker. Review the extracted profile data against the original resume text and verify accuracy, especially for dates and company names.

ORIGINAL RESUME TEXT:
{resume_text[:4000]}  # Limited to 4000 chars to stay within token limits

EXTRACTED PROFILE DATA (from first pass):
{json.dumps(profile_data_pass1, indent=2)}

Please review and correct the extracted data, paying special attention to:
1. **Dates** - Verify all employment dates, education dates, and certification dates are accurate
2. **Company Names** - Verify all company/organization names are spelled correctly
3. **Job Titles** - Verify job titles are accurate
4. **Education Institutions** - Verify institution names are correct

Return the corrected profile data in the same JSON format...
"""
```

#### Step 2: Request Payload
```python
payload_pass2 = {
    "messages": [
        {
            "role": "system",
            "content": "You are a resume quality checker. Verify and correct extracted data, especially dates and company names. Return only valid JSON."
        },
        {
            "role": "user",
            "content": prompt_pass2
        }
    ],
    "max_tokens": 2000,
    "temperature": 0.1,  # Very low temperature for accurate corrections
    "response_format": {"type": "json_object"}
}
```

#### Step 3: API Call
```python
def make_request_pass2():
    return requests.post(
        text_gen.url,
        headers=text_gen.headers,
        json=payload_pass2,
        timeout=60
    )

response_pass2 = api_call_with_retry(make_request_pass2, max_retries=3)
```

#### Step 4: Response Processing
```python
if response_pass2.status_code == 200:
    result_pass2 = response_pass2.json()
    content_pass2 = result_pass2['choices'][0]['message']['content']
    
    # Track token usage
    if text_gen.token_tracker and 'usage' in result_pass2:
        usage = result_pass2['usage']
        prompt_tokens = usage.get('prompt_tokens', 0)
        completion_tokens = usage.get('completion_tokens', 0)
        text_gen.token_tracker.add_completion_tokens(prompt_tokens, completion_tokens)
    
    # Parse corrected JSON
    profile_data_corrected = json.loads(content_pass2)
    return profile_data_corrected
else:
    # Fallback: Return first pass result if second pass fails
    st.warning("⚠️ Self-correction pass failed, using initial extraction...")
    return profile_data_pass1
```

**Fallback Strategy:**
- If Pass 2 fails (API error, timeout, etc.), returns Pass 1 result
- User is warned but not blocked from proceeding

---

## 4. Retry Logic: `api_call_with_retry()`

### 4.1 Function Location
**Line:** ~173

### 4.2 Technical Implementation

#### Exponential Backoff Algorithm
```python
def api_call_with_retry(func, max_retries=3, initial_delay=1, max_delay=60):
    for attempt in range(max_retries):
        response = func()
        
        # Success
        if response.status_code in [200, 201]:
            return response
        
        # Rate Limit (429) - Retry with exponential backoff
        elif response.status_code == 429:
            if attempt < max_retries - 1:
                fallback_delay = _calculate_exponential_delay(initial_delay, attempt, max_delay)
                delay, delay_source = _determine_retry_delay(response, fallback_delay, max_delay)
                
                st.warning(f"⏳ Rate limit reached. Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                continue
            else:
                # Max retries exceeded
                st.error("🚫 Rate Limit Exceeded...")
                return None
        
        # Other HTTP errors - Don't retry
        else:
            return response
```

#### Delay Calculation
```python
def _calculate_exponential_delay(initial_delay, attempt, max_delay):
    delay = initial_delay * (2 ** attempt)  # Exponential: 1s, 2s, 4s, 8s...
    return min(delay, max_delay)  # Cap at max_delay
```

#### Retry-After Header Support
```python
def _determine_retry_delay(response, fallback_delay, max_delay):
    # Check for Retry-After header (server-suggested delay)
    retry_after = response.headers.get('Retry-After')
    if retry_after:
        try:
            server_delay = int(retry_after)
            return min(server_delay, max_delay), "server"
        except ValueError:
            pass
    
    return fallback_delay, "fallback"
```

**Key Features:**
- **Exponential Backoff:** Delays increase exponentially (1s → 2s → 4s)
- **Server Hints:** Respects `Retry-After` header if provided
- **User Feedback:** Shows progress messages during retries
- **Max Retries:** Default 3 attempts before giving up

---

## 5. Token Tracking

### 5.1 Purpose
Track API usage and costs for both embedding and completion tokens.

### 5.2 Implementation

#### Embedding Tokens
```python
# In APIMEmbeddingGenerator.get_embedding()
if self.token_tracker and 'usage' in result:
    tokens_used = result['usage'].get('total_tokens', 0)
    self.token_tracker.add_embedding_tokens(tokens_used)
elif self.token_tracker:
    # Fallback: Estimate using tiktoken
    tokens = len(self.encoding.encode(text))
    self.token_tracker.add_embedding_tokens(tokens)
```

#### Completion Tokens
```python
# In extract_profile_from_resume()
if text_gen.token_tracker and 'usage' in result_pass1:
    usage = result_pass1['usage']
    prompt_tokens = usage.get('prompt_tokens', 0)
    completion_tokens = usage.get('completion_tokens', 0)
    text_gen.token_tracker.add_completion_tokens(prompt_tokens, completion_tokens)
```

---

## 6. Error Handling Summary

### 6.1 API Error Types Handled

| Status Code | Handling Strategy | User Feedback |
|------------|-------------------|---------------|
| **200/201** | Success, process response | None (proceeds normally) |
| **429** | Retry with exponential backoff (up to 3 times) | Warning during retries, error if max retries exceeded |
| **400/401/403** | No retry, return None | Error message with status code |
| **500/502/503** | No retry, return None | Error message with status code |
| **Timeout** | Caught by exception handler | Error message with exception details |

### 6.2 JSON Parsing Errors
```python
try:
    profile_data = json.loads(content)
except json.JSONDecodeError:
    # Attempt regex extraction
    json_match = re.search(r'\{.*\}', content, re.DOTALL)
    if json_match:
        profile_data = json.loads(json_match.group())
    else:
        st.error("Could not parse JSON response")
        return None
```

---

## 7. Performance Optimizations

### 7.1 Resource Caching
- **`@st.cache_resource`** decorator ensures API clients are created only once
- Prevents unnecessary re-initialization on every function call

### 7.2 Embedding Reuse
- Resume embedding generated once and stored in `st.session_state.resume_embedding`
- Reused for all subsequent job searches (no regeneration needed)

### 7.3 Request Throttling
- Minimum 100ms delay between embedding requests
- Prevents hitting rate limits from rapid successive calls

### 7.4 Token Limits
- Resume text limited to 4000 characters in Pass 2 prompt
- Raw resume text limited to 3000 characters in resume generation prompts

---

## 8. API Endpoints Used

### 8.1 Azure OpenAI Embeddings API
```
POST {endpoint}/openai/deployments/text-embedding-3-small/embeddings?api-version=2024-02-01
```
- **Purpose:** Generate vector embeddings for resume text
- **Model:** `text-embedding-3-small`
- **Output:** 1536-dimensional vector

**Request Example:**
```json
{
  "input": "John Doe\nSoftware Engineer\n5 years experience in Python...",
  "model": "text-embedding-3-small"
}
```

**Response Example:**
```json
{
  "data": [
    {
      "embedding": [0.0123, -0.0456, 0.0789, ...],  // 1536 dimensions
      "index": 0
    }
  ],
  "usage": {
    "prompt_tokens": 150,
    "total_tokens": 150
  }
}
```

### 8.2 Azure OpenAI Chat Completions API
```
POST {endpoint}/openai/deployments/gpt-4o-mini/chat/completions?api-version=2024-02-01
```
- **Purpose:** Extract and verify structured profile data
- **Model:** `gpt-4o-mini`
- **Format:** JSON object (enforced via `response_format`)

**Request Example (Pass 1):**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a resume parser. Extract structured information and return only valid JSON."
    },
    {
      "role": "user",
      "content": "You are an expert at parsing resumes. Extract structured information...\n\nRESUME TEXT:\n[resume content]"
    }
  ],
  "max_tokens": 2000,
  "temperature": 0.3,
  "response_format": {"type": "json_object"}
}
```

**Response Example:**
```json
{
  "choices": [
    {
      "message": {
        "content": "{\"name\": \"John Doe\", \"email\": \"john@example.com\", ...}"
      }
    }
  ],
  "usage": {
    "prompt_tokens": 1200,
    "completion_tokens": 800,
    "total_tokens": 2000
  }
}
```

---

## 9. Data Flow Diagram

```
User Uploads Resume
        ↓
extract_text_from_resume() [Local - No API]
        ↓
Store resume_text in session_state
        ↓
┌───────────────────────────────────────┐
│ API Call #1: Embedding Generation    │
│ - Endpoint: /embeddings               │
│ - Model: text-embedding-3-small       │
│ - Retries: 3 with exponential backoff │
│ - Output: 1536-dim vector             │
└───────────────────────────────────────┘
        ↓
Store embedding in session_state.resume_embedding
        ↓
┌───────────────────────────────────────┐
│ API Call #2a: Profile Extraction      │
│ - Endpoint: /chat/completions         │
│ - Model: gpt-4o-mini                  │
│ - Temperature: 0.3                    │
│ - Format: JSON                        │
└───────────────────────────────────────┘
        ↓
Parse JSON → profile_data_pass1
        ↓
┌───────────────────────────────────────┐
│ API Call #2b: Self-Correction        │
│ - Endpoint: /chat/completions         │
│ - Model: gpt-4o-mini                  │
│ - Temperature: 0.1                    │
│ - Format: JSON                        │
│ - Fallback: Use Pass 1 if fails       │
└───────────────────────────────────────┘
        ↓
Parse JSON → profile_data_corrected
        ↓
Update session_state.user_profile
        ↓
Display profile form (pre-filled)
```

---

## 10. Security Considerations

### 10.1 API Key Management
- API keys stored in Streamlit secrets (`st.secrets`)
- Never exposed in code or error messages
- Endpoint URLs sanitized in error messages (only base URL shown)

### 10.2 Request Timeouts
- Embedding requests: 30 seconds
- Chat completion requests: 60 seconds
- Prevents hanging requests

### 10.3 Input Validation
- File type validation (PDF, DOCX, TXT only)
- Text extraction error handling
- JSON parsing with fallback regex extraction

---

## 11. Configuration Constants

### 11.1 Embedding Configuration
```python
# Default batch size for batch embedding generation
DEFAULT_EMBEDDING_BATCH_SIZE = 20  # Configurable via EMBEDDING_BATCH_SIZE env var

# Delay between embedding batches (seconds)
EMBEDDING_BATCH_DELAY = 1  # Configurable via EMBEDDING_BATCH_DELAY env var

# Delay when rate limit is encountered (seconds)
EMBEDDING_RATE_LIMIT_DELAY = 2  # Configurable via EMBEDDING_RATE_LIMIT_DELAY env var
```

### 11.2 Configuration Source Priority
1. Streamlit secrets (`st.secrets.get(key)`)
2. Environment variables (`os.getenv(key)`)
3. Default values (as shown above)

### 11.3 API Configuration
- **Embedding Model:** `text-embedding-3-small`
- **Text Generation Model:** `gpt-4o-mini`
- **API Version:** `2024-02-01`
- **Request Timeouts:**
  - Embeddings: 30 seconds
  - Chat Completions: 60 seconds

---

## 12. Potential Issues & Recommendations

### 12.1 Current Issues

1. **No Request Size Validation**
   - **Issue:** Very large resumes could exceed token limits
   - **Recommendation:** Add text truncation before API calls (e.g., max 8000 chars)

2. **No Concurrent Request Limiting**
   - **Issue:** Multiple users could trigger simultaneous API calls
   - **Recommendation:** Implement request queue or semaphore for concurrent requests

3. **Pass 2 Failure Silent Fallback**
   - **Issue:** If Pass 2 fails, user may not notice incorrect data
   - **Recommendation:** Make warning more prominent or require user confirmation

### 12.2 Optimization Opportunities

1. **Batch Embedding Generation**
   - Currently generates one embedding at a time
   - Could batch multiple texts if needed in future

2. **Caching Extracted Profiles**
   - Could cache profile extraction results by resume hash
   - Avoids re-extraction if same resume uploaded again

3. **Async API Calls**
   - Could use async/await for non-blocking API calls
   - Improves user experience during long operations

---

## 13. Summary

The resume upload process involves **3 API calls total**:
1. **1 Embedding API call** - Generates vector representation of resume
2. **2 Chat Completion API calls** - Two-pass extraction and verification of structured profile data

**Key Technical Features:**
- ✅ Exponential backoff retry logic for rate limits
- ✅ Token usage tracking
- ✅ Resource caching for API clients
- ✅ Comprehensive error handling
- ✅ Self-correction mechanism for data accuracy
- ✅ Embedding reuse for performance

**Total API Calls per Resume Upload:** 3
**Estimated Time:** 5-15 seconds (depending on resume size and API latency)
**Token Usage:** ~2000-5000 tokens per upload (varies by resume length)
