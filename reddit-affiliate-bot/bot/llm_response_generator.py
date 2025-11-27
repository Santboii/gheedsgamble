"""LLM-powered response generator."""

import os
from typing import List, Dict
from bot.llm_client import LLMClient


class LLMResponseGenerator:
    """Generates Reddit responses using LLM."""
    
    def __init__(self, provider: str = None, api_key: str = None):
        """Initialize the LLM response generator.
        
        Args:
            provider: LLM provider ('groq', 'openai', 'gemini', 'anthropic')
            api_key: API key (optional, reads from env if not provided)
        """
        provider = provider or os.getenv('LLM_PROVIDER', 'groq')
        self.client = LLMClient(provider=provider, api_key=api_key)
    
    def generate_response(
        self,
        post_title: str,
        post_body: str,
        analysis: Dict,
        products: List[Dict]
    ) -> str:
        """Generate a personalized Reddit response.
        
        Args:
            post_title: Post title
            post_body: Post body
            analysis: Analysis dict from LLMAnalyzer
            products: List of product dicts with 'name' and 'link'
            
        Returns:
            Generated response text
        """
        if not products:
            return None
        
        # Build system prompt
        system_prompt = """You are a helpful Reddit user who gives genuine product recommendations.

Write a casual, friendly response that:
- Sounds natural and conversational (like a real Reddit comment)
- Is brief (2-3 sentences max)
- Directly addresses what they asked
- Recommends specific products with their URLs
- Does NOT use markdown links - just mention the product name and include the plain URL
- Does NOT include affiliate disclosures or disclaimers
- Does NOT sound corporate or salesy
- Uses lowercase sometimes, be casual

The product URLs will be auto-linked by Reddit when posted."""

        # Build user prompt with context
        key_needs = analysis.get('key_needs', [])
        needs_text = f"\nKey needs: {', '.join(key_needs)}" if key_needs else ""
        
        experience = analysis.get('experience_level', 'beginner')
        budget = analysis.get('budget_range', 'unknown')
        
        # Format products with plain URLs (Reddit auto-links them)
        product_links = []
        for product in products[:3]:  # Max 3 products
            name = product.get('name', 'Product')
            link = product.get('affiliate_link', '#')
            # Just include the product name and URL - Reddit will auto-link the URL
            product_links.append(f"{name}: {link}")
        products_text = "\n".join([f"- {p}" for p in product_links])
        
        user_prompt = f"""Post Title: {post_title}
Post Body: {post_body or '(no body)'}

User Info:
- Experience: {experience}
- Budget: {budget}{needs_text}

Recommended Products:
{products_text}

Write a helpful, casual Reddit comment recommending these products:"""

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
    
    generator = LLMResponseGenerator()
    
    test_products = [
        {'name': 'Celestron NexStar 130SLT', 'link': 'https://example.com/1'},
        {'name': 'Orion SkyQuest XT8', 'link': 'https://example.com/2'},
    ]
    
    test_analysis = {
        'experience_level': 'beginner',
        'budget_range': 'budget ($100-$300)',
        'confidence': 0.9,
        'key_needs': ['easy to use', 'portable']
    }
    
    response = generator.generate_response(
        "What telescope should I buy?",
        "I'm new to astronomy with a $300 budget. Want something portable.",
        test_analysis,
        test_products
    )
    
    print("Generated response:")
    print(response)
