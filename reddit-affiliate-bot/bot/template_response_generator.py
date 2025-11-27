"""Template-based response generator (no AI required)."""

from typing import List, Dict
import random


class TemplateResponseGenerator:
    """Generates responses using templates instead of AI."""
    
    def __init__(self):
        """Initialize the template generator."""
        self.templates = {
            'beginner': [
                "Hey! For a beginner, I'd recommend checking out {products}. They're great starting points!",
                "Welcome to astronomy! {products} are all solid choices for beginners.",
                "These are popular beginner options: {products}. Any would work well for you!",
            ],
            'intermediate': [
                "Based on your experience, I'd suggest {products}. They offer great value.",
                "You might want to look at {products}. Good upgrades from entry-level scopes.",
                "Check out {products} - they're solid mid-range options.",
            ],
            'advanced': [
                "For serious observing, consider {products}. High-quality optics.",
                "These are worth looking at: {products}. Premium performance.",
                "{products} are all excellent choices for experienced observers.",
            ]
        }
    
    def generate_response(
        self,
        post_title: str,
        post_body: str,
        analysis: Dict,
        products: List[Dict]
    ) -> str:
        """Generate a response using templates.
        
        Args:
            post_title: Post title
            post_body: Post body
            analysis: Analysis dict
            products: List of product dicts with 'name' and 'link'
            
        Returns:
            Generated response text
        """
        if not products:
            return None
        
        # Get experience level
        experience = analysis.get('experience_level', 'beginner')
        
        # Select a random template for this experience level
        template_list = self.templates.get(experience, self.templates['beginner'])
        template = random.choice(template_list)
        
        # Format products as markdown links
        product_links = []
        for product in products[:3]:  # Max 3 products
            name = product.get('name', 'Product')
            link = product.get('link', '#')
            product_links.append(f"[{name}]({link})")
        
        products_text = ", ".join(product_links[:-1])
        if len(product_links) > 1:
            products_text += f", and {product_links[-1]}"
        else:
            products_text = product_links[0]
        
        # Generate response
        response = template.format(products=products_text)
        
        # Add budget note if applicable
        budget = analysis.get('budget_range', '')
        if 'budget' in budget.lower():
            response += " These fit your budget nicely."
        elif 'premium' in budget.lower():
            response += " Worth the investment for serious use."
        
        return response


if __name__ == "__main__":
    # Test the generator
    generator = TemplateResponseGenerator()
    
    test_products = [
        {'name': 'Celestron NexStar 130SLT', 'link': 'https://example.com/1'},
        {'name': 'Orion SkyQuest XT8', 'link': 'https://example.com/2'},
        {'name': 'Apertura AD8', 'link': 'https://example.com/3'},
    ]
    
    test_analysis = {
        'experience_level': 'beginner',
        'budget_range': 'budget ($100-$300)',
        'confidence': 0.8
    }
    
    response = generator.generate_response(
        "What telescope should I buy?",
        "I'm new to astronomy with a $300 budget.",
        test_analysis,
        test_products
    )
    
    print("Generated response:")
    print(response)
