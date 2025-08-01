import os
import requests
import hashlib
import json
import time
from typing import Optional, Dict
from .logger import SyllaboLogger

class AIClient:
    def __init__(self):
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.use_gemini = bool(self.gemini_key and self.gemini_key != "your_gemini_api_key_here_optional")
        self.logger = SyllaboLogger("ai_client")
        self.cache = {}
        self.cache_ttl = 3600  # 1 hour cache
        self.use_mock = False
        
        if self.use_gemini:
            self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
            self.logger.info("Using Gemini API")
        else:
            self.base_url = "https://ai.hackclub.com/chat/completions"
            self.logger.info("Using Hack Club AI API")
    
    async def get_completion(self, prompt: str, use_cache: bool = True) -> str:
        if use_cache:
            cache_key = self._get_cache_key(prompt)
            cached_result = self._get_from_cache(cache_key)
            if cached_result:
                self.logger.debug("Using cached AI response")
                return cached_result
        
        try:
            if self.use_gemini:
                result = await self._get_gemini_completion(prompt)
            else:
                result = await self._get_hackclub_completion(prompt)
            
            if use_cache and not result.startswith("Error:"):
                self._save_to_cache(cache_key, result)
            
            return result
        except Exception as e:
            self.logger.error(f"AI completion failed: {e}")
            return self._get_mock_completion(prompt)
    
    def _get_cache_key(self, prompt: str) -> str:
        """Generate cache key from prompt"""
        return hashlib.md5(prompt.encode()).hexdigest()
    
    def _get_from_cache(self, cache_key: str) -> Optional[str]:
        """Get result from cache if not expired"""
        if cache_key in self.cache:
            cached_data = self.cache[cache_key]
            if time.time() - cached_data['timestamp'] < self.cache_ttl:
                return cached_data['result']
            else:
                del self.cache[cache_key]
        return None
    
    def _save_to_cache(self, cache_key: str, result: str):
        """Save result to cache"""
        self.cache[cache_key] = {
            'result': result,
            'timestamp': time.time()
        }
    
    def _get_mock_completion(self, prompt: str) -> str:
        """Generate mock AI responses when APIs are unavailable"""
        prompt_lower = prompt.lower()
        
        if "rate relevance" in prompt_lower or "relevance" in prompt_lower:
            if "python" in prompt_lower:
                return "8.5"
            elif "data structure" in prompt_lower:
                return "9.2"
            elif "machine learning" in prompt_lower:
                return "8.8"
            else:
                return "7.5"
        
        elif "sentiment" in prompt_lower or "comments" in prompt_lower:
            return "8.0"
        
        elif "extract" in prompt_lower and "topics" in prompt_lower:
            return '''[
                {"name": "Introduction to Programming", "subtopics": ["Variables", "Data Types", "Basic Syntax"]},
                {"name": "Control Structures", "subtopics": ["Loops", "Conditionals", "Functions"]},
                {"name": "Data Structures", "subtopics": ["Arrays", "Lists", "Dictionaries"]},
                {"name": "Object-Oriented Programming", "subtopics": ["Classes", "Objects", "Inheritance"]}
            ]'''
        
        elif "missing topics" in prompt_lower:
            return "None"
        
        else:
            return "Mock response for testing purposes."
    
    async def _get_hackclub_completion(self, prompt: str) -> str:
        payload = {
            "messages": [{"role": "user", "content": prompt}]
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.logger.debug(f"Making Hack Club AI request (attempt {attempt + 1})")
                response = requests.post(self.base_url, json=payload, timeout=30)
                response.raise_for_status()
                result = response.json()['choices'][0]['message']['content']
                self.logger.debug("Hack Club AI request successful")
                return result
            except requests.exceptions.Timeout:
                self.logger.warning(f"Hack Club AI timeout (attempt {attempt + 1})")
                if attempt == max_retries - 1:
                    return "Error: Request timeout"
                time.sleep(2 ** attempt)  # Exponential backoff
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Hack Club AI request failed: {e}")
                if attempt == max_retries - 1:
                    return f"Error: {str(e)}"
                time.sleep(2 ** attempt)
            except (KeyError, IndexError) as e:
                self.logger.error(f"Unexpected Hack Club AI response format: {e}")
                return "Error: Unexpected response format"
    
    async def _get_gemini_completion(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                self.logger.debug(f"Making Gemini API request (attempt {attempt + 1})")
                url = f"{self.base_url}?key={self.gemini_key}"
                response = requests.post(url, json=payload, headers=headers, timeout=30)
                response.raise_for_status()
                result = response.json()['candidates'][0]['content']['parts'][0]['text']
                self.logger.debug("Gemini API request successful")
                return result
            except requests.exceptions.Timeout:
                self.logger.warning(f"Gemini API timeout (attempt {attempt + 1})")
                if attempt == max_retries - 1:
                    return "Error: Request timeout"
                time.sleep(2 ** attempt)
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Gemini API request failed: {e}")
                if attempt == max_retries - 1:
                    return f"Error: {str(e)}"
                time.sleep(2 ** attempt)
            except (KeyError, IndexError) as e:
                self.logger.error(f"Unexpected Gemini response format: {e}")
                return "Error: Unexpected response format"