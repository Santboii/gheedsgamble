"""
Test script to verify bot components work without needing full Reddit credentials.
Tests the AI analyzer, product matcher, and response generator in isolation.
"""

import os
import sys
from dotenv import load_dotenv

# Add bot directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from bot.ai_analyzer import AIAnalyzer
from bot.product_matcher import ProductMatcher
from bot.response_generator import ResponseGenerator


def test_product_matcher():
    """Test the product matcher with the telescope catalog."""
    print("\n" + "="*70)
    print("TEST 1: Product Matcher")
    print("="*70)
    
    matcher = ProductMatcher()
    
    # Test finding products for a beginner
    constraints = {
        "experience_level": "beginner",
        "budget_range": "$100-$200",
        "keywords": ["telescope", "beginner", "planets"]
    }
    
    products = matcher.find_matching_products("telescopes", constraints, max_results=3)
    
    print(f"\n✅ Found {len(products)} products for beginner looking at planets:")
    for i, product in enumerate(products, 1):
        print(f"\n  {i}. {product['name']}")
        print(f"     Category: {product['category']}")
        print(f"     Price: {product['price_range']}")
        print(f"     Use cases: {', '.join(product['use_cases'][:3])}")
    
    return len(products) > 0


def test_ai_analyzer():
    """Test the AI analyzer (requires OpenAI API key)."""
    print("\n" + "="*70)
    print("TEST 2: AI Analyzer")
    print("="*70)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("\n⚠️  Skipping AI analyzer test - OPENAI_API_KEY not set")
        print("   Set OPENAI_API_KEY in .env to test this component")
        return None
    
    analyzer = AIAnalyzer()
    
    # Test post
    test_title = "First telescope for a beginner?"
    test_body = "I want to look at planets and the moon. Budget is around $150. What should I get?"
    
    print(f"\n📝 Test Post:")
    print(f"   Title: {test_title}")
    print(f"   Body: {test_body}")
    
    print("\n🔍 Analyzing...")
    analysis = analyzer.analyze_post(test_title, test_body, "telescopes")
    
    print(f"\n✅ Analysis Results:")
    print(f"   Relevant: {analysis['is_relevant']}")
    print(f"   Confidence: {analysis['confidence']:.2f}")
    print(f"   Experience Level: {analysis['experience_level']}")
    print(f"   Budget: {analysis['budget_range']}")
    print(f"   Keywords: {', '.join(analysis['keywords'])}")
    print(f"   Reasoning: {analysis['reasoning']}")
    
    return analysis['is_relevant']


def test_response_generator():
    """Test the response generator (requires OpenAI API key)."""
    print("\n" + "="*70)
    print("TEST 3: Response Generator")
    print("="*70)
    
    if not os.getenv('OPENAI_API_KEY'):
        print("\n⚠️  Skipping response generator test - OPENAI_API_KEY not set")
        print("   Set OPENAI_API_KEY in .env to test this component")
        return None
    
    generator = ResponseGenerator()
    matcher = ProductMatcher()
    
    # Mock analysis
    analysis = {
        "experience_level": "beginner",
        "budget_range": "$100-$200",
        "intent": "Looking for first telescope to view planets"
    }
    
    # Get products
    constraints = {
        "experience_level": "beginner",
        "budget_range": "$100-$200",
        "keywords": ["telescope", "beginner", "planets"]
    }
    products = matcher.find_matching_products("telescopes", constraints, max_results=2)
    
    # Format products
    formatted_products = [
        matcher.format_product_for_response(p, "stargazer019-20")
        for p in products
    ]
    
    print("\n✍️  Generating response...")
    response = generator.generate_response(
        "First telescope for a beginner?",
        "I want to look at planets and the moon. Budget is around $150.",
        analysis,
        formatted_products
    )
    
    if response:
        print(f"\n✅ Generated Response:")
        print("   " + "-"*66)
        print("   " + response.replace("\n", "\n   "))
        print("   " + "-"*66)
        
        is_valid = generator.validate_response(response)
        print(f"\n   Valid: {is_valid}")
        print(f"   Length: {len(response)} characters")
        
        return is_valid
    else:
        print("\n❌ Failed to generate response")
        return False


def main():
    """Run all tests."""
    load_dotenv()
    
    print("\n🧪 Reddit Affiliate Bot - Component Tests")
    print("="*70)
    
    results = {}
    
    # Test 1: Product Matcher (no API key needed)
    try:
        results['product_matcher'] = test_product_matcher()
    except Exception as e:
        print(f"\n❌ Product matcher test failed: {e}")
        results['product_matcher'] = False
    
    # Test 2: AI Analyzer (needs OpenAI key)
    try:
        results['ai_analyzer'] = test_ai_analyzer()
    except Exception as e:
        print(f"\n❌ AI analyzer test failed: {e}")
        results['ai_analyzer'] = False
    
    # Test 3: Response Generator (needs OpenAI key)
    try:
        results['response_generator'] = test_response_generator()
    except Exception as e:
        print(f"\n❌ Response generator test failed: {e}")
        results['response_generator'] = False
    
    # Summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    
    for test_name, result in results.items():
        if result is None:
            status = "⏭️  SKIPPED"
        elif result:
            status = "✅ PASSED"
        else:
            status = "❌ FAILED"
        print(f"{status} - {test_name.replace('_', ' ').title()}")
    
    print("\n" + "="*70)
    
    # Check if OpenAI key is needed
    if not os.getenv('OPENAI_API_KEY'):
        print("\n💡 To test AI components:")
        print("   1. Copy env.template to .env")
        print("   2. Add your OPENAI_API_KEY")
        print("   3. Run this test again")
        print("\n   Get an API key at: https://platform.openai.com/api-keys")
    
    print()


if __name__ == '__main__':
    main()
