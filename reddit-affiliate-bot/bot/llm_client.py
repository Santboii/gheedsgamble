"""Unified LLM client supporting multiple providers."""

import os
from typing import Dict, List, Optional
import requests


class LLMClient:
    """Unified client for multiple LLM providers."""
    
    PROVIDERS = {
        'groq': {
            'name': 'Groq',
            'api_base': 'https://api.groq.com/openai/v1',
            'default_model': 'llama-3.3-70b-versatile',
            'env_key': 'GROQ_API_KEY',
            'cost_per_1m_tokens': 0.0  # Free tier
        },
        'openai': {
            'name': 'OpenAI',
            'api_base': 'https://api.openai.com/v1',
            'default_model': 'gpt-4o-mini',
            'env_key': 'OPENAI_API_KEY',
            'cost_per_1m_tokens': 0.15
        },
        'gemini': {
            'name': 'Google Gemini',
            'api_base': 'https://generativelanguage.googleapis.com/v1beta',
            'default_model': 'gemini-1.5-flash',
            'env_key': 'GEMINI_API_KEY',
            'cost_per_1m_tokens': 0.075
        },
        'anthropic': {
            'name': 'Anthropic Claude',
            'api_base': 'https://api.anthropic.com/v1',
            'default_model': 'claude-3-haiku-20240307',
            'env_key': 'ANTHROPIC_API_KEY',
            'cost_per_1m_tokens': 0.25
        }
    }
    
    def __init__(self, provider: str = 'groq', api_key: Optional[str] = None, model: Optional[str] = None):
        """Initialize LLM client.
        
        Args:
            provider: Provider name ('groq', 'openai', 'gemini', 'anthropic')
            api_key: API key (if None, reads from environment)
            model: Model name (if None, uses provider default)
        """
        if provider not in self.PROVIDERS:
            raise ValueError(f"Unknown provider: {provider}. Choose from: {list(self.PROVIDERS.keys())}")
        
        self.provider = provider
        self.config = self.PROVIDERS[provider]
        self.api_key = api_key or os.getenv(self.config['env_key'])
        self.model = model or self.config['default_model']
        
        if not self.api_key:
            raise ValueError(f"API key not found. Set {self.config['env_key']} environment variable.")
    
    def chat(self, messages: List[Dict[str, str]], temperature: float = 0.7, max_tokens: int = 500) -> str:
        """Send a chat completion request.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens to generate
            
        Returns:
            Generated text response
        """
        if self.provider == 'gemini':
            return self._chat_gemini(messages, temperature, max_tokens)
        elif self.provider == 'anthropic':
            return self._chat_anthropic(messages, temperature, max_tokens)
        else:
            # OpenAI-compatible (Groq, OpenAI)
            return self._chat_openai_compatible(messages, temperature, max_tokens)
    
    def _chat_openai_compatible(self, messages: List[Dict], temperature: float, max_tokens: int) -> str:
        """Chat with OpenAI-compatible API (Groq, OpenAI)."""
        url = f"{self.config['api_base']}/chat/completions"
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json'
        }
        data = {
            'model': self.model,
            'messages': messages,
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            error_detail = response.text
            raise Exception(f"API Error ({response.status_code}): {error_detail}")
        
        result = response.json()
        return result['choices'][0]['message']['content']
    
    def _chat_gemini(self, messages: List[Dict], temperature: float, max_tokens: int) -> str:
        """Chat with Google Gemini API."""
        url = f"{self.config['api_base']}/models/{self.model}:generateContent?key={self.api_key}"
        
        # Convert messages to Gemini format
        contents = []
        for msg in messages:
            role = 'user' if msg['role'] in ['user', 'system'] else 'model'
            contents.append({
                'role': role,
                'parts': [{'text': msg['content']}]
            })
        
        data = {
            'contents': contents,
            'generationConfig': {
                'temperature': temperature,
                'maxOutputTokens': max_tokens
            }
        }
        
        response = requests.post(url, json=data, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['candidates'][0]['content']['parts'][0]['text']
    
    def _chat_anthropic(self, messages: List[Dict], temperature: float, max_tokens: int) -> str:
        """Chat with Anthropic Claude API."""
        url = f"{self.config['api_base']}/messages"
        headers = {
            'x-api-key': self.api_key,
            'anthropic-version': '2023-06-01',
            'Content-Type': 'application/json'
        }
        
        # Extract system message if present
        system = None
        claude_messages = []
        for msg in messages:
            if msg['role'] == 'system':
                system = msg['content']
            else:
                claude_messages.append(msg)
        
        data = {
            'model': self.model,
            'messages': claude_messages,
            'temperature': temperature,
            'max_tokens': max_tokens
        }
        
        if system:
            data['system'] = system
        
        response = requests.post(url, json=data, headers=headers, timeout=30)
        response.raise_for_status()
        
        result = response.json()
        return result['content'][0]['text']


if __name__ == "__main__":
    # Test the client
    import sys
    
    provider = sys.argv[1] if len(sys.argv) > 1 else 'groq'
    
    try:
        client = LLMClient(provider=provider)
        print(f"Testing {client.config['name']} ({client.model})...")
        
        messages = [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': 'Say hello in one sentence.'}
        ]
        
        response = client.chat(messages)
        print(f"Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
