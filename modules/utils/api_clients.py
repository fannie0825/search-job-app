"""
API Client Classes for CareerLens Application

This module contains all API client classes including:
- APIMEmbeddingGenerator: Azure OpenAI embedding generation
- AzureOpenAITextGenerator: Azure OpenAI text generation  
- RateLimiter: Rate limiting for API calls
- IndeedScraperAPI: Job scraping via RapidAPI
- TokenUsageTracker: Token usage tracking
"""

import os
import time
import json
import re
import hashlib
import streamlit as st
import requests
import tiktoken
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from .config import (
    DEFAULT_EMBEDDING_BATCH_SIZE,
    EMBEDDING_BATCH_DELAY,
    RAPIDAPI_MAX_REQUESTS_PER_MINUTE,
    USE_FAST_SKILL_MATCHING
)
from .helpers import (
    api_call_with_retry,
    _websocket_keepalive,
    _chunked_sleep,
    _is_streamlit_cloud
)


class APIMEmbeddingGenerator:
    """Azure OpenAI Embedding Generator"""
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        endpoint = endpoint.rstrip('/')
        if endpoint.endswith('/openai'):
            endpoint = endpoint[:-7]
        self.endpoint = endpoint
        self.deployment = "text-embedding-3-small"
        self.api_version = "2024-02-01"
        self.url = f"{self.endpoint}/openai/deployments/{self.deployment}/embeddings?api-version={self.api_version}"
        self.headers = {"api-key": self.api_key, "Content-Type": "application/json"}
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def get_embedding(self, text):
        """Generate embedding for a single text."""
        try:
            payload = {"input": text, "model": self.deployment}
            estimated_tokens = len(self.encoding.encode(text))
            
            def make_request():
                return requests.post(self.url, headers=self.headers, json=payload, timeout=30)
            
            response = api_call_with_retry(make_request, max_retries=3)
            
            if response and response.status_code == 200:
                result = response.json()
                embedding = result['data'][0]['embedding']
                tokens_used = result['usage'].get('total_tokens', 0) if 'usage' in result else estimated_tokens
                return embedding, tokens_used
            else:
                return None, 0
        except Exception as e:
            st.error(f"Error generating embedding: {e}")
            return None, 0
    
    def get_embeddings_batch(self, texts, batch_size=None):
        """Generate embeddings for a batch of texts."""
        if not texts:
            return [], 0
        
        effective_batch_size = batch_size or DEFAULT_EMBEDDING_BATCH_SIZE
        if effective_batch_size <= 0:
            effective_batch_size = DEFAULT_EMBEDDING_BATCH_SIZE
        
        embeddings = []
        total_tokens_used = 0
        progress_bar = st.progress(0)
        status_text = st.empty()
        total_batches = (len(texts) + effective_batch_size - 1) // effective_batch_size
        
        for i in range(0, len(texts), effective_batch_size):
            batch = texts[i:i + effective_batch_size]
            batch_num = i // effective_batch_size + 1
            progress = (i + len(batch)) / len(texts)
            progress_bar.progress(progress)
            status_text.text(f"🔄 Generating embeddings: {i + len(batch)}/{len(texts)} (batch {batch_num}/{total_batches})")
            
            if i > 0 and EMBEDDING_BATCH_DELAY > 0:
                _chunked_sleep(EMBEDDING_BATCH_DELAY, f"Batch {batch_num}/{total_batches}")
            
            try:
                payload = {"input": batch, "model": self.deployment}
                estimated_batch_tokens = sum(len(self.encoding.encode(text)) for text in batch)
                _websocket_keepalive(f"Processing batch {batch_num}/{total_batches}...")
                
                def make_request():
                    return requests.post(self.url, headers=self.headers, json=payload, timeout=25)
                
                response = api_call_with_retry(make_request, max_retries=3)
                
                if response and response.status_code == 200:
                    data = response.json()
                    sorted_data = sorted(data['data'], key=lambda x: x['index'])
                    embeddings.extend([item['embedding'] for item in sorted_data])
                    tokens_used = data['usage'].get('total_tokens', 0) if 'usage' in data else estimated_batch_tokens
                    total_tokens_used += tokens_used
                elif response and response.status_code == 429:
                    st.warning(f"⚠️ Rate limit reached after retries. Skipping batch {batch_num}/{total_batches}.")
                else:
                    st.warning(f"⚠️ Batch embedding failed, trying individual calls for batch {batch_num}...")
                    for text in batch:
                        emb, tokens = self.get_embedding(text)
                        if emb:
                            embeddings.append(emb)
                            total_tokens_used += tokens
            except Exception as e:
                st.warning(f"⚠️ Error processing batch {batch_num}, trying individual calls: {e}")
                for text in batch:
                    emb, tokens = self.get_embedding(text)
                    if emb:
                        embeddings.append(emb)
                        total_tokens_used += tokens
        
        progress_bar.empty()
        status_text.empty()
        return embeddings, total_tokens_used


class AzureOpenAITextGenerator:
    """Azure OpenAI Text Generator for resume generation and analysis"""
    def __init__(self, api_key, endpoint, token_tracker=None):
        self.api_key = api_key
        endpoint = endpoint.rstrip('/')
        if endpoint.endswith('/openai'):
            endpoint = endpoint[:-7]
        self.endpoint = endpoint
        self.deployment = "gpt-4o-mini"
        self.api_version = "2024-02-01"
        self.url = f"{self.endpoint}/openai/deployments/{self.deployment}/chat/completions?api-version={self.api_version}"
        self.headers = {"api-key": self.api_key, "Content-Type": "application/json"}
        self.token_tracker = token_tracker
        self.encoding = tiktoken.get_encoding("cl100k_base")
    
    def generate_resume(self, user_profile, job_posting, raw_resume_text=None):
        """Generate a tailored resume based on user profile and job posting."""
        # Implementation from app.py lines ~1783-1921
        # (Full implementation should be extracted from app.py)
        pass
    
    def calculate_match_score(self, resume_content, job_description, embedding_generator):
        """Calculate match score between resume and job description."""
        # Implementation from app.py lines ~1923-2004
        # (Full implementation should be extracted from app.py)
        pass
    
    def analyze_seniority_level(self, job_titles):
        """Analyze job titles to determine seniority level."""
        # Implementation from app.py lines ~2006-2065
        # (Full implementation should be extracted from app.py)
        pass
    
    def recommend_accreditations(self, job_descriptions, user_skills):
        """Recommend accreditations based on job requirements."""
        # Implementation from app.py lines ~2067-2125
        # (Full implementation should be extracted from app.py)
        pass
    
    def generate_recruiter_note(self, job, user_profile, semantic_score, skill_score):
        """Generate a personalized recruiter note."""
        # Implementation from app.py lines ~2127-2185
        # (Full implementation should be extracted from app.py)
        pass


class RateLimiter:
    """Simple rate limiter that enforces requests per minute limit."""
    def __init__(self, max_requests_per_minute):
        self.max_requests_per_minute = max_requests_per_minute
        self.request_times = []
        self.lock = False
    
    def wait_if_needed(self):
        """Wait if we've exceeded the rate limit, otherwise record the request."""
        if self.max_requests_per_minute <= 0:
            return
        
        now = time.time()
        one_minute_ago = now - 60
        self.request_times = [t for t in self.request_times if t > one_minute_ago]
        
        if len(self.request_times) >= self.max_requests_per_minute:
            oldest_request = min(self.request_times)
            wait_time = 60 - (now - oldest_request) + 1
            if wait_time > 0:
                status_placeholder = st.empty()
                remaining = int(wait_time)
                while remaining > 0:
                    status_placeholder.info(f"⏳ Rate limiting: Waiting {remaining}s to stay under {self.max_requests_per_minute} requests/minute...")
                    chunk = min(2, remaining)
                    time.sleep(chunk)
                    remaining -= chunk
                status_placeholder.empty()
                now = time.time()
                one_minute_ago = now - 60
                self.request_times = [t for t in self.request_times if t > one_minute_ago]
        
        self.request_times.append(time.time())


class IndeedScraperAPI:
    """Job scraper using Indeed Scraper API via RapidAPI."""
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://indeed-scraper-api.p.rapidapi.com/api/job"
        self.headers = {
            'Content-Type': 'application/json',
            'x-rapidapi-host': 'indeed-scraper-api.p.rapidapi.com',
            'x-rapidapi-key': api_key
        }
        self.rate_limiter = RateLimiter(RAPIDAPI_MAX_REQUESTS_PER_MINUTE)
    
    def search_jobs(self, query, location="Hong Kong", max_rows=15, job_type="fulltime", country="hk"):
        """Search for jobs using Indeed Scraper API."""
        # Implementation from app.py lines ~2243-2293
        # (Full implementation should be extracted from app.py)
        pass
    
    def _parse_job(self, job_data):
        """Parse job data from API response."""
        # Implementation from app.py lines ~2295-2326
        # (Full implementation should be extracted from app.py)
        pass


class TokenUsageTracker:
    """Tracks token usage and costs for API calls."""
    def __init__(self):
        self.total_tokens = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_embedding_tokens = 0
        self.cost_usd = 0.0
        self.embedding_cost_per_1k = 0.00002
        self.gpt4_mini_prompt_cost_per_1k = 0.00015
        self.gpt4_mini_completion_cost_per_1k = 0.0006
    
    def add_embedding_tokens(self, tokens):
        """Track embedding token usage."""
        self.total_embedding_tokens += tokens
        self.total_tokens += tokens
        self.cost_usd += (tokens / 1000) * self.embedding_cost_per_1k
    
    def add_completion_tokens(self, prompt_tokens, completion_tokens):
        """Track completion token usage."""
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.total_tokens += prompt_tokens + completion_tokens
        self.cost_usd += (prompt_tokens / 1000) * self.gpt4_mini_prompt_cost_per_1k
        self.cost_usd += (completion_tokens / 1000) * self.gpt4_mini_completion_cost_per_1k
    
    def get_summary(self):
        """Get usage summary."""
        return {
            'total_tokens': self.total_tokens,
            'embedding_tokens': self.total_embedding_tokens,
            'prompt_tokens': self.total_prompt_tokens,
            'completion_tokens': self.total_completion_tokens,
            'estimated_cost_usd': self.cost_usd
        }
    
    def reset(self):
        """Reset counters."""
        self.total_tokens = 0
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_embedding_tokens = 0
        self.cost_usd = 0.0


# Factory functions for getting API clients
def get_token_tracker():
    """Get or create token usage tracker."""
    if 'token_tracker' not in st.session_state:
        st.session_state.token_tracker = TokenUsageTracker()
    return st.session_state.token_tracker


@st.cache_resource(show_spinner=False)
def _create_embedding_generator_resource(api_key, endpoint):
    return APIMEmbeddingGenerator(api_key, endpoint)


@st.cache_resource(show_spinner=False)
def _create_text_generator_resource(api_key, endpoint):
    return AzureOpenAITextGenerator(api_key, endpoint)


def get_embedding_generator():
    """Get cached embedding generator instance."""
    try:
        AZURE_OPENAI_API_KEY = st.secrets.get("AZURE_OPENAI_API_KEY")
        AZURE_OPENAI_ENDPOINT = st.secrets.get("AZURE_OPENAI_ENDPOINT")
        
        if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT:
            st.error("⚠️ Azure OpenAI credentials are missing.")
            return None
        
        generator = _create_embedding_generator_resource(AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT)
        return generator
    except KeyError as e:
        st.error(f"⚠️ Missing required secret: {e}")
        return None
    except Exception as e:
        st.error(f"⚠️ Error initializing embedding generator: {e}")
        return None


def get_text_generator():
    """Get cached text generator instance."""
    try:
        AZURE_OPENAI_API_KEY = st.secrets.get("AZURE_OPENAI_API_KEY")
        AZURE_OPENAI_ENDPOINT = st.secrets.get("AZURE_OPENAI_ENDPOINT")
        
        if not AZURE_OPENAI_API_KEY or not AZURE_OPENAI_ENDPOINT:
            st.error("⚠️ Azure OpenAI credentials are missing.")
            return None
        
        generator = _create_text_generator_resource(AZURE_OPENAI_API_KEY, AZURE_OPENAI_ENDPOINT)
        generator.token_tracker = get_token_tracker()
        return generator
    except KeyError as e:
        st.error(f"⚠️ Missing required secret: {e}")
        return None
    except Exception as e:
        st.error(f"⚠️ Error initializing text generator: {e}")
        return None


def get_job_scraper():
    """Get Indeed job scraper."""
    if 'job_scraper' not in st.session_state:
        RAPIDAPI_KEY = st.secrets.get("RAPIDAPI_KEY", "")
        if not RAPIDAPI_KEY:
            st.error("⚠️ RAPIDAPI_KEY is required in secrets.")
            return None
        st.session_state.job_scraper = IndeedScraperAPI(RAPIDAPI_KEY)
    return st.session_state.job_scraper
