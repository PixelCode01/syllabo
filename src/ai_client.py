import os
import requests
from typing import Optional

class AIClient:
    def __init__(self):
        self.gemini_key = os.getenv('GEMINI_API_KEY')
        self.use_gemini = bool(self.gemini_key)
        
        if self.use_gemini:
            self.base_url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        else:
            self.base_url = "https://ai.hackclub.com/chat/completions"
    
    async def get_completion(self, prompt: str) -> str:
        if self.use_gemini:
            return await self._get_gemini_completion(prompt)
        else:
            return await self._get_hackclub_completion(prompt)
    
    async def _get_hackclub_completion(self, prompt: str) -> str:
        payload = {
            "messages": [{"role": "user", "content": prompt}]
        }
        
        try:
            response = requests.post(self.base_url, json=payload)
            response.raise_for_status()
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"
    
    async def _get_gemini_completion(self, prompt: str) -> str:
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{"text": prompt}]
            }]
        }
        
        try:
            url = f"{self.base_url}?key={self.gemini_key}"
            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        except Exception as e:
            return f"Error: {str(e)}"