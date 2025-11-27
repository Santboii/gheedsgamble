"""
AI Analyzer Module

Uses OpenAI to analyze Reddit posts and determine:
1. Whether the post is asking for product recommendations
2. What type of products they're interested in
3. User's experience level and budget constraints
"""

import os
import json
from typing import Dict, Optional, List
from openai import OpenAI


class AIAnalyzer:
    """Analyzes Reddit posts using OpenAI to determine relevance and extract intent."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the AI analyzer.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"  # Cost-effective model for analysis
    
    def analyze_post(self, post_title: str, post_body: str, subreddit: str) -> Dict:
        """
        Analyze a Reddit post to determine if it's asking for product recommendations.
        
        Args:
            post_title: The post title
            post_body: The post body/selftext
            subreddit: The subreddit name
            
        Returns:
            Dict with analysis results:
            {
                "is_relevant": bool,
                "confidence": float (0-1),
                "intent": str,
                "experience_level": str (beginner|intermediate|advanced),
                "budget_range": str,
                "keywords": List[str],
                "reasoning": str
            }
        """
        prompt = self._build_analysis_prompt(post_title, post_body, subreddit)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert at analyzing Reddit posts to determine if users are asking for product recommendations. You respond only with valid JSON."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                response_format={"type": "json_object"},
                temperature=0.3
            )
            
            result = json.loads(response.choices[0].message.content)
            return result
            
        except Exception as e:
            print(f"Error analyzing post: {e}")
            return {
                "is_relevant": False,
                "confidence": 0.0,
                "intent": "unknown",
                "experience_level": "unknown",
                "budget_range": "unknown",
                "keywords": [],
                "reasoning": f"Analysis failed: {str(e)}"
            }
    
    def _build_analysis_prompt(self, title: str, body: str, subreddit: str) -> str:
        """Build the prompt for post analysis."""
        return f"""Analyze this Reddit post from r/{subreddit} and determine if the user is asking for product recommendations or advice that could benefit from product suggestions.

POST TITLE: {title}

POST BODY: {body or "(no body text)"}

Provide your analysis as JSON with the following structure:
{{
    "is_relevant": true/false,  // Is this post asking for or would benefit from product recommendations?
    "confidence": 0.0-1.0,  // How confident are you in this assessment?
    "intent": "brief description of what the user wants",
    "experience_level": "beginner|intermediate|advanced|unknown",
    "budget_range": "budget mentioned or implied (e.g., '$100-$200', 'budget-friendly', 'no limit', 'unknown')",
    "keywords": ["list", "of", "relevant", "keywords"],  // Important terms that indicate product needs
    "reasoning": "brief explanation of your assessment"
}}

Guidelines:
- is_relevant should be true if the post is asking for buying advice, product recommendations, or "what should I get"
- is_relevant should be false for troubleshooting, showing off purchases, general questions, or off-topic posts
- Extract experience level from context (e.g., "beginner", "first time", "new to this" = beginner)
- Look for budget mentions in the text
- Keywords should be specific product-related terms (e.g., "telescope", "beginner", "astrophotography", "planetary viewing")
"""

    def should_respond(self, analysis: Dict, confidence_threshold: float = 0.7) -> bool:
        """
        Determine if the bot should respond based on analysis results.
        
        Args:
            analysis: Analysis results from analyze_post()
            confidence_threshold: Minimum confidence to respond (0-1)
            
        Returns:
            True if bot should respond, False otherwise
        """
        return (
            analysis.get("is_relevant", False) and 
            analysis.get("confidence", 0.0) >= confidence_threshold
        )
    
    def extract_constraints(self, analysis: Dict) -> Dict:
        """
        Extract user constraints from analysis for product matching.
        
        Args:
            analysis: Analysis results from analyze_post()
            
        Returns:
            Dict with constraints:
            {
                "experience_level": str,
                "budget_range": str,
                "keywords": List[str]
            }
        """
        return {
            "experience_level": analysis.get("experience_level", "unknown"),
            "budget_range": analysis.get("budget_range", "unknown"),
            "keywords": analysis.get("keywords", [])
        }
