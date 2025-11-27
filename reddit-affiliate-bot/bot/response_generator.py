"""
Response Generator Module

Uses OpenAI to generate natural, helpful responses that include product recommendations.
"""

import os
import random
from typing import Dict, List, Optional
from openai import OpenAI


class ResponseGenerator:
    """Generates helpful Reddit responses with product recommendations."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize the response generator.
        
        Args:
            api_key: OpenAI API key (defaults to OPENAI_API_KEY env var)
        """
        api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o-mini"
    
    def generate_response(
        self,
        post_title: str,
        post_body: str,
        analysis: Dict,
        products: List[Dict],
        style: str = "helpful"
    ) -> str:
        """
        Generate a helpful response with product recommendations.
        
        Args:
            post_title: Original post title
            post_body: Original post body
            analysis: AI analysis results
            products: List of formatted products to recommend
            style: Response style (helpful, detailed, concise)
            
        Returns:
            Generated response text
        """
        if not products:
            return None
        
        prompt = self._build_response_prompt(
            post_title,
            post_body,
            analysis,
            products,
            style
        )
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": self._get_system_prompt()
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.8,
                max_tokens=200
            )
            
            response_text = response.choices[0].message.content.strip()
            
            # Occasionally add human-like typos/grammar errors
            if random.random() < 0.3:  # 30% chance
                response_text = self._add_human_imperfections(response_text)
            
            return response_text
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for response generation."""
        return """You are a casual Reddit user who's knowledgeable about products and likes helping people out.

Your responses should:
- Be VERY brief - just 1-2 short sentences max
- Sound natural and casual, like texting a friend
- Include specific product recommendations with Amazon links
- Use Reddit markdown (** for bold)
- NO affiliate disclosures or disclaimers
- Only give extra tips/context if the user specifically asked for advice (not just product names)

Important guidelines:
- Don't sound corporate or salesy
- Keep it super casual and brief
- Just answer what they asked, nothing more
- Use lowercase sometimes, be conversational
- Don't overthink it"""
    
    def _build_response_prompt(
        self,
        title: str,
        body: str,
        analysis: Dict,
        products: List[Dict],
        style: str
    ) -> str:
        """Build the prompt for response generation."""
        
        # Format products for the prompt
        products_text = "\n\n".join([
            f"Product {i+1}: {p['name']}\n"
            f"- Category: {p['category']}\n"
            f"- Price Range: {p['price_range']}\n"
            f"- Description: {p['description']}\n"
            f"- Link: {p['affiliate_link']}\n"
            f"- Good for: {', '.join(p['use_cases'])}"
            for i, p in enumerate(products)
        ])
        
        # Determine if user is asking for advice or just product names
        asking_for_advice = any(word in (title + " " + (body or "")).lower() 
                               for word in ["advice", "help", "tips", "recommend", "suggest", "should i", "what do you think"])
        
        advice_instruction = "Include a brief helpful tip or context." if asking_for_advice else "Just list the products, no extra advice."
        
        return f"""Generate a BRIEF Reddit comment (1-2 sentences max) responding to this post:

TITLE: {title}
BODY: {body or "(no body text)"}

USER CONTEXT:
- Experience Level: {analysis.get('experience_level', 'unknown')}
- Budget: {analysis.get('budget_range', 'not specified')}

RECOMMENDED PRODUCTS:
{products_text}

Generate a casual, brief response that:
1. Recommends the products above with Amazon links
2. {advice_instruction}
3. Format product names in **bold**
4. Keep it to 1-2 sentences total
5. NO affiliate disclosure or disclaimer

Be casual and conversational. Keep it SHORT."""

    def _add_human_imperfections(self, text: str) -> str:
        """Add occasional typos or grammar imperfections to seem more human."""
        imperfections = [
            # Common typos
            ("the ", "teh ", 0.1),
            ("you ", "u ", 0.15),
            ("your ", "ur ", 0.15),
            ("really ", "rly ", 0.1),
            ("probably ", "prob ", 0.2),
            ("definitely ", "def ", 0.2),
            ("because ", "bc ", 0.15),
            ("though ", "tho ", 0.2),
            # Missing punctuation at end
            (".", "", 0.1),
            ("!", "", 0.1),
        ]
        
        for original, replacement, probability in imperfections:
            if original in text and random.random() < probability:
                # Only replace first occurrence
                text = text.replace(original, replacement, 1)
                break  # Only one imperfection per response
        
        return text

    def validate_response(self, response: str) -> bool:
        """
        Validate that a response meets quality standards.
        
        Args:
            response: Generated response text
            
        Returns:
            True if response is valid, False otherwise
        """
        if not response:
            return False
        
        # Check minimum length (very short is OK now)
        if len(response) < 20:
            return False
        
        # Check for at least one link
        if "amazon.com" not in response.lower():
            return False
        
        return True
