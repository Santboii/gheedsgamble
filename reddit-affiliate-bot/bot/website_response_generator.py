"""Website-based response generator (telescoped.space)."""

import os
from typing import Dict
from bot.llm_client import LLMClient


class WebsiteResponseGenerator:
    """Generates Reddit responses recommending telescoped.space pages."""
    
    # Route mapping based on user needs
    ROUTE_MAP = {
        'budget': 'https://www.telescoped.space/telescopes/budget',
        'premium': 'https://www.telescoped.space/telescopes/premium',
        'telescopes_general': 'https://www.telescoped.space/telescopes',
        'eyepieces': 'https://www.telescoped.space/eyepieces-accessories',
        'astrophotography': 'https://www.telescoped.space/astrophotography-101',
        'stargazing_guide': 'https://www.telescoped.space/stargazing-guide',
        'collimation': 'https://www.telescoped.space/collimation-calibration',
        'mounts': 'https://www.telescoped.space/mounts-tripods',
    }
    
    def __init__(self, provider: str = None, api_key: str = None):
        """Initialize the website response generator.
        
        Args:
            provider: LLM provider ('groq', 'openai', 'gemini', 'anthropic')
            api_key: API key (optional, reads from env if not provided)
        """
        provider = provider or os.getenv('LLM_PROVIDER', 'groq')
        self.client = LLMClient(provider=provider, api_key=api_key)
    
    def get_recommended_routes(self, analysis: Dict) -> list:
        """Determine which telescoped.space routes to recommend.
        
        Args:
            analysis: Analysis dict from LLMAnalyzer
            
        Returns:
            List of recommended route URLs
        """
        routes = []
        
        budget = analysis.get('budget_range', '').lower()
        experience = analysis.get('experience_level', '').lower()
        key_needs = [need.lower() for need in analysis.get('key_needs', [])]
        
        # Budget-based routing
        if 'budget' in budget or any('$' in budget and int(budget.split('$')[1].split('-')[0].replace(',', '')) < 400 for _ in [1]):
            routes.append(self.ROUTE_MAP['budget'])
        elif 'premium' in budget or '1000' in budget:
            routes.append(self.ROUTE_MAP['premium'])
        
        # Need-based routing
        if any(word in ' '.join(key_needs) for word in ['eyepiece', 'lens', 'filter', 'accessory']):
            routes.append(self.ROUTE_MAP['eyepieces'])
        if any(word in ' '.join(key_needs) for word in ['photo', 'camera', 'imaging', 'astrophotography']):
            routes.append(self.ROUTE_MAP['astrophotography'])
        if any(word in ' '.join(key_needs) for word in ['mount', 'tripod', 'eq', 'tracking']):
            routes.append(self.ROUTE_MAP['mounts'])
        if any(word in ' '.join(key_needs) for word in ['collimate', 'align', 'calibrate', 'setup']):
            routes.append(self.ROUTE_MAP['collimation'])
        
        # Experience-based routing
        if experience == 'beginner' and not routes:
            routes.append(self.ROUTE_MAP['stargazing_guide'])
        
        # Default to general telescopes page
        if not routes:
            routes.append(self.ROUTE_MAP['telescopes_general'])
        
        # Limit to 2 routes max
        return routes[:2]
    
    def generate_response(
        self,
        post_title: str,
        post_body: str,
        analysis: Dict
    ) -> str:
        """Generate a personalized Reddit response with telescoped.space links.
        
        Args:
            post_title: Post title
            post_body: Post body
            analysis: Analysis dict from LLMAnalyzer
            
        Returns:
            Generated response text with website links
        """
        # Get recommended routes
        routes = self.get_recommended_routes(analysis)
        
        # Build system prompt
        system_prompt = """You are a helpful Reddit user who gives genuine astronomy/telescope advice.

Write a casual, friendly response that:
- Sounds natural and conversational (like a real Reddit comment)
- Is brief (2-3 sentences max)
- Directly addresses what they asked
- Recommends checking out telescoped.space pages (provide the URLs)
- Does NOT sound corporate or salesy
- Uses lowercase sometimes, be casual
- Does NOT include disclaimers or "I'm not affiliated" statements

The URLs will be plain text that Reddit will auto-link."""

        # Build user prompt with context
        key_needs = analysis.get('key_needs', [])
        needs_text = f"\nKey needs: {', '.join(key_needs)}" if key_needs else ""
        
        experience = analysis.get('experience_level', 'beginner')
        budget = analysis.get('budget_range', 'unknown')
        
        # Format routes
        routes_text = "\n".join([f"- {route}" for route in routes])
        
        user_prompt = f"""Post Title: {post_title}
Post Body: {post_body or '(no body)'}

User Info:
- Experience: {experience}
- Budget: {budget}{needs_text}

Recommended Pages (include these URLs in your response):
{routes_text}

Write a helpful, casual Reddit comment recommending these telescoped.space pages:"""

        messages = [
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_prompt}
        ]
        
        try:
            response = self.client.chat(messages, temperature=0.8, max_tokens=200)
            return response.strip()
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return None


if __name__ == "__main__":
    # Test the generator
    from dotenv import load_dotenv
    load_dotenv()
    
    generator = WebsiteResponseGenerator()
    
    test_analysis = {
        'experience_level': 'beginner',
        'budget_range': 'budget ($100-$300)',
        'confidence': 0.9,
        'key_needs': ['easy to use', 'portable']
    }
    
    response = generator.generate_response(
        "What telescope should I buy?",
        "I'm new to astronomy with a $200 budget. Want something portable.",
        test_analysis
    )
    
    print("Generated response:")
    print(response)
    print("\nRecommended routes:")
    print(generator.get_recommended_routes(test_analysis))
