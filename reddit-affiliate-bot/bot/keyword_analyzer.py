"""Keyword-based post analyzer (no AI required)."""

import re
from typing import Dict, List


class KeywordAnalyzer:
    """Analyzes Reddit posts using keyword matching instead of AI."""
    
    def __init__(self):
        """Initialize the keyword analyzer."""
        # Keywords that indicate someone is seeking recommendations
        self.seeking_keywords = [
            'recommend', 'suggestion', 'advice', 'help', 'which', 'what',
            'should i', 'looking for', 'need', 'want', 'buy', 'purchase',
            'best', 'good', 'beginner', 'first', 'starting', 'new to',
            'confused', 'deciding', 'choose', 'vs', 'or', 'better'
        ]
        
        # Budget indicators
        self.budget_low = ['budget', 'cheap', 'affordable', 'under 200', 'under 300', 'limited']
        self.budget_mid = ['500', '600', '700', '800', 'mid-range', 'moderate']
        self.budget_high = ['1000', '1500', '2000', 'expensive', 'premium', 'high-end']
        
        # Experience level indicators
        self.beginner_keywords = ['beginner', 'first', 'new', 'starting', 'never', 'novice']
        self.intermediate_keywords = ['intermediate', 'some experience', 'upgrade']
        self.advanced_keywords = ['advanced', 'experienced', 'serious', 'professional']
    
    def analyze_post(self, title: str, body: str, subreddit: str) -> Dict:
        """Analyze a post using keyword matching.
        
        Args:
            title: Post title
            body: Post body text
            subreddit: Subreddit name
            
        Returns:
            Analysis dict with confidence, experience level, and budget
        """
        content = (title + " " + body).lower()
        
        # Check if seeking recommendations
        seeking_score = sum(1 for keyword in self.seeking_keywords if keyword in content)
        
        # Has question mark?
        has_question = '?' in content
        
        # Calculate confidence (0-1)
        confidence = min(1.0, (seeking_score * 0.15) + (0.3 if has_question else 0))
        
        # Determine experience level
        experience_level = "beginner"
        if any(kw in content for kw in self.advanced_keywords):
            experience_level = "advanced"
        elif any(kw in content for kw in self.intermediate_keywords):
            experience_level = "intermediate"
        elif any(kw in content for kw in self.beginner_keywords):
            experience_level = "beginner"
        
        # Determine budget range
        budget_range = "unknown"
        if any(kw in content for kw in self.budget_low):
            budget_range = "budget ($100-$300)"
        elif any(kw in content for kw in self.budget_high):
            budget_range = "premium ($1000+)"
        elif any(kw in content for kw in self.budget_mid):
            budget_range = "mid-range ($500-$800)"
        
        # Extract numbers that might be budget
        numbers = re.findall(r'\$?(\d+)', content)
        if numbers:
            max_num = max(int(n) for n in numbers if int(n) < 10000)
            if max_num < 400:
                budget_range = "budget ($100-$300)"
            elif max_num < 900:
                budget_range = "mid-range ($500-$800)"
            elif max_num >= 1000:
                budget_range = "premium ($1000+)"
        
        return {
            'is_seeking_recommendation': confidence > 0.3,
            'confidence': confidence,
            'experience_level': experience_level,
            'budget_range': budget_range,
            'seeking_score': seeking_score,
            'has_question': has_question
        }
    
    def should_respond(self, analysis: Dict, threshold: float = 0.3) -> bool:
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
        constraints = {
            'experience_level': analysis.get('experience_level', 'beginner'),
            'budget_range': analysis.get('budget_range', 'unknown')
        }
        
        return constraints


if __name__ == "__main__":
    # Test the analyzer
    analyzer = KeywordAnalyzer()
    
    test_posts = [
        ("What's the best beginner telescope under $300?", "I'm new to astronomy and looking for recommendations."),
        ("Just bought my first telescope!", "So excited to start stargazing!"),
        ("Need help choosing between two scopes", "I have a budget of $500-600 and can't decide."),
    ]
    
    for title, body in test_posts:
        analysis = analyzer.analyze_post(title, body, "telescopes")
        print(f"\nTitle: {title}")
        print(f"Analysis: {analysis}")
        print(f"Should respond: {analyzer.should_respond(analysis)}")
