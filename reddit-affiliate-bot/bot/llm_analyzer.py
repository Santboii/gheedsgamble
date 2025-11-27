"""LLM-powered post analyzer."""

import os
import json
from typing import Dict
from bot.llm_client import LLMClient


class LLMAnalyzer:
    """Analyzes Reddit posts using LLM."""
    
    def __init__(self, provider: str = None, api_key: str = None):
        """Initialize the LLM analyzer.
        
        Args:
            provider: LLM provider ('groq', 'openai', 'gemini', 'anthropic')
            api_key: API key (optional, reads from env if not provided)
        """
        provider = provider or os.getenv('LLM_PROVIDER', 'groq')
        self.client = LLMClient(provider=provider, api_key=api_key)
    
    def analyze_post(self, title: str, body: str, subreddit: str, comments: str = "") -> Dict:
        """Analyze a post using LLM.
        
        Args:
            title: Post title
            body: Post body text
            subreddit: Subreddit name
            comments: Top comments from the post (optional)
            
        Returns:
            Analysis dict with confidence, experience level, and budget
        """
        system_prompt = """You are an expert at analyzing Reddit posts to determine if someone is seeking product recommendations.

Analyze the post and return a JSON object with:
- is_seeking_recommendation (boolean): true if they're asking for product advice
- confidence (float 0-1): how confident you are
- experience_level (string): "beginner", "intermediate", or "advanced"
- budget_range (string): e.g., "budget ($100-$300)", "mid-range ($500-$800)", "premium ($1000+)", or "unknown"
- key_needs (list): main requirements mentioned (max 3 items)

Only return the JSON, no other text."""

        comments_section = f"\n\nTop Comments:\n{comments}" if comments else ""
        
        user_prompt = f"""Subreddit: r/{subreddit}
Title: {title}
Body: {body or '(no body text)'}{comments_section}

Analyze this post:"""

        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        
        try:
            response = self.client.chat(messages, temperature=0.3, max_tokens=300)
            
            # Parse JSON response
            # Sometimes LLMs wrap JSON in markdown code blocks
            response = response.strip()
            if response.startswith('```'):
                response = response.split('```')[1]
                if response.startswith('json'):
                    response = response[4:]
            
            analysis = json.loads(response.strip())
            
            # Ensure all required fields exist
            analysis.setdefault('is_seeking_recommendation', False)
            analysis.setdefault('confidence', 0.0)
            analysis.setdefault('experience_level', 'beginner')
            analysis.setdefault('budget_range', 'unknown')
            analysis.setdefault('key_needs', [])
            
            return analysis
            
        except Exception as e:
            print(f"Error analyzing post: {e}")
            # Return default low-confidence analysis
            return {
                'is_seeking_recommendation': False,
                'confidence': 0.0,
                'experience_level': 'beginner',
                'budget_range': 'unknown',
                'key_needs': [],
                'error': str(e)
            }
    
    def should_respond(self, analysis: Dict, threshold: float = 0.6) -> bool:
        """Determine if we should respond to this post.
        
        Args:
            analysis: Analysis dict from analyze_post
            threshold: Minimum confidence threshold
            
        Returns:
            True if we should respond
        """
        return analysis.get('confidence', 0) >= threshold
    
    def extract_constraints(self, analysis: Dict) -> Dict:
        """Extract constraints from analysis for product matching.
        
        Args:
            analysis: Analysis dict from analyze_post
            
        Returns:
            Constraints dict for ProductMatcher
        """
        return {
            'experience_level': analysis.get('experience_level', 'beginner'),
            'budget_range': analysis.get('budget_range', 'unknown'),
            'key_needs': analysis.get('key_needs', [])
        }


if __name__ == "__main__":
    # Test the analyzer
    from dotenv import load_dotenv
    load_dotenv()
    
    analyzer = LLMAnalyzer()
    
    test_posts = [
        ("What's the best beginner telescope under $300?", "I'm new to astronomy and looking for recommendations."),
        ("Just bought my first telescope!", "So excited to start stargazing!"),
        ("Need help choosing between two scopes", "I have a budget of $500-600 and can't decide."),
    ]
    
    for title, body in test_posts:
        print(f"\n{'='*60}")
        print(f"Title: {title}")
        analysis = analyzer.analyze_post(title, body, "telescopes")
        print(f"Analysis: {json.dumps(analysis, indent=2)}")
        print(f"Should respond: {analyzer.should_respond(analysis)}")
