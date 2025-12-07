"""Helper functions for API retries, memory management, and utilities"""
import os
import gc
import time
import math
import json
import re
import base64
import streamlit as st
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
import requests


def _cleanup_session_state():
    """Clean up old/stale data from session state to prevent memory bloat."""
    MAX_CACHE_ENTRIES = 10
    MAX_SKILL_CACHE_SIZE = 500
    
    if 'jobs_cache' in st.session_state and isinstance(st.session_state.jobs_cache, dict):
        cache = st.session_state.jobs_cache
        if len(cache) > MAX_CACHE_ENTRIES:
            sorted_keys = sorted(
                cache.keys(),
                key=lambda k: cache[k].get('timestamp', ''),
                reverse=True
            )
            keys_to_remove = sorted_keys[MAX_CACHE_ENTRIES:]
            for key in keys_to_remove:
                del cache[key]
    
    if 'skill_embeddings_cache' in st.session_state:
        cache = st.session_state.skill_embeddings_cache
        if len(cache) > MAX_SKILL_CACHE_SIZE:
            keys_to_remove = list(cache.keys())[:-MAX_SKILL_CACHE_SIZE//2]
            for key in keys_to_remove:
                del cache[key]
    
    if 'user_skills_embeddings_cache' in st.session_state:
        cache = st.session_state.user_skills_embeddings_cache
        if len(cache) > MAX_SKILL_CACHE_SIZE:
            keys_to_remove = list(cache.keys())[:-MAX_SKILL_CACHE_SIZE//2]
            for key in keys_to_remove:
                del cache[key]
    
    gc.collect()


def get_img_as_base64(file):
    """Convert an image file to base64 string for embedding in HTML"""
    with open(file, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()


def _parse_retry_after_value(value):
    """Convert Retry-After style header values into seconds."""
    if not value:
        return None
    value = value.strip()
    if not value:
        return None
    try:
        seconds = float(value)
        if seconds >= 0:
            return int(math.ceil(seconds))
    except (ValueError, TypeError):
        pass
    if value.count(':') == 2:
        try:
            hours, minutes, seconds = value.split(':')
            total_seconds = int(hours) * 3600 + int(minutes) * 60 + int(float(seconds))
            if total_seconds >= 0:
                return total_seconds
        except (ValueError, TypeError):
            pass
    try:
        retry_time = parsedate_to_datetime(value)
        if retry_time:
            if retry_time.tzinfo is None:
                retry_time = retry_time.replace(tzinfo=timezone.utc)
            now = datetime.now(timezone.utc)
            delta = (retry_time - now).total_seconds()
            if delta > 0:
                return int(math.ceil(delta))
    except (TypeError, ValueError, OverflowError):
        pass
    return None


def _extract_delay_from_body(response):
    """Attempt to read retry hints from JSON/text error bodies."""
    if response is None:
        return None
    message = None
    try:
        data = response.json()
        if isinstance(data, dict):
            error = data.get('error') or {}
            if isinstance(error, dict):
                message = error.get('message') or error.get('code')
            if not message:
                message = data.get('message')
    except (ValueError, json.JSONDecodeError):
        pass
    if not message:
        message = response.text or ""
    if not message:
        return None
    match = re.search(r'after\s+(\d+)\s+seconds?', message, re.IGNORECASE)
    if match:
        try:
            seconds = int(match.group(1))
            if seconds >= 0:
                return seconds
        except ValueError:
            pass
    return None


def _determine_retry_delay(response, fallback_delay, max_delay):
    """Use headers/body hints to determine how long to wait before retrying."""
    if response is not None:
        headers = response.headers or {}
        header_candidates = [
            'Retry-After',
            'x-ms-retry-after-ms',
            'x-ms-retry-after',
            'x-ratelimit-reset-requests',
            'x-ratelimit-reset-tokens',
            'x-ratelimit-reset',
        ]
        for header in header_candidates:
            raw_value = headers.get(header)
            if not raw_value:
                continue
            if header.endswith('-ms'):
                try:
                    ms = float(raw_value)
                    if ms >= 0:
                        seconds = int(math.ceil(ms / 1000.0))
                        return max(1, min(seconds, max_delay)), f"header:{header}"
                except (ValueError, TypeError):
                    continue
            else:
                parsed = _parse_retry_after_value(raw_value)
                if parsed is not None:
                    return max(1, min(parsed, max_delay)), f"header:{header}"
        body_delay = _extract_delay_from_body(response)
        if body_delay is not None:
            return max(1, min(body_delay, max_delay)), "body"
    return max(1, min(fallback_delay, max_delay)), "fallback"


def _calculate_exponential_delay(initial_delay, attempt, max_delay):
    """Calculate exponential backoff delay for the current retry attempt."""
    return max(1, min(initial_delay * (2 ** attempt), max_delay))


def _chunked_sleep(delay, message_prefix=""):
    """Sleep in small chunks to prevent WebSocket timeout on Streamlit Cloud."""
    if delay <= 2:
        time.sleep(delay)
        return
    
    status_placeholder = st.empty()
    remaining = int(delay)
    while remaining > 0:
        if message_prefix:
            status_placeholder.caption(f"{message_prefix} ({remaining}s remaining...)")
        else:
            status_placeholder.caption(f"⏳ Processing... ({remaining}s)")
        chunk = min(2, remaining)
        time.sleep(chunk)
        remaining -= chunk
    status_placeholder.empty()


def _websocket_keepalive(message=None):
    """Send a lightweight UI update to keep WebSocket connection alive."""
    placeholder = st.empty()
    if message:
        placeholder.caption(f"⏳ {message}")
        time.sleep(0.1)
    placeholder.empty()


def api_call_with_retry(func, max_retries=3, initial_delay=1, max_delay=60):
    """Execute an API call with exponential backoff retry logic for rate limit errors (429)."""
    for attempt in range(max_retries):
        try:
            response = func()
            
            if response.status_code in [200, 201]:
                return response
            
            elif response.status_code == 429:
                if attempt < max_retries - 1:
                    fallback_delay = _calculate_exponential_delay(initial_delay, attempt, max_delay)
                    delay, delay_source = _determine_retry_delay(response, fallback_delay, max_delay)
                    source_note = ""
                    if delay_source != "fallback":
                        source_note = f" (server hint: {delay_source})"
                    if attempt == 0:
                        st.warning(
                            f"⏳ Rate limit reached. Retrying in {delay} seconds{source_note}... "
                            f"(Attempt {attempt + 1}/{max_retries})"
                        )
                    else:
                        st.caption(f"⏳ Retrying... ({attempt + 1}/{max_retries})")
                    _chunked_sleep(delay, f"⏳ Retry {attempt + 1}/{max_retries}")
                    continue
                else:
                    error_msg = (
                        "🚫 **Rate Limit Exceeded**\n\n"
                        "The API rate limit has been reached. Please:\n"
                        "1. Wait a few minutes and try again\n"
                        "2. Reduce the number of jobs you're searching for\n"
                        "3. Check your API quota/limits\n\n"
                        f"Status: {response.status_code}"
                    )
                    st.error(error_msg)
                    return None
            
            else:
                return response
                
        except requests.exceptions.Timeout:
            if attempt < max_retries - 1:
                delay = _calculate_exponential_delay(initial_delay, attempt, max_delay)
                st.warning(f"⏳ Request timed out. Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                _chunked_sleep(delay)
                continue
            else:
                st.error("❌ Request timed out after multiple attempts. Please try again later.")
                return None
        
        except requests.exceptions.RequestException as e:
            if attempt < max_retries - 1:
                delay = _calculate_exponential_delay(initial_delay, attempt, max_delay)
                st.warning(f"⏳ Network error. Retrying in {delay} seconds... (Attempt {attempt + 1}/{max_retries})")
                _chunked_sleep(delay)
                continue
            else:
                st.error(f"❌ Network error after multiple attempts: {e}")
                return None
        
        except Exception as e:
            st.error(f"❌ Unexpected error: {e}")
            return None
    
    return None


def _is_streamlit_cloud():
    """Detect if running on Streamlit Cloud (ephemeral filesystem)."""
    return (
        os.environ.get('STREAMLIT_SHARING_MODE') is not None or
        os.environ.get('STREAMLIT_SERVER_PORT') is not None or
        os.path.exists('/mount/src') or
        'streamlit.app' in os.environ.get('HOSTNAME', '')
    )
