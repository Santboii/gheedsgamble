"""
Product Matcher Module

Matches user needs (from AI analysis) with products from the catalog.
Uses keyword matching and constraint filtering to find the best recommendations.
"""

import json
import os
from typing import Dict, List, Optional
from pathlib import Path


class ProductMatcher:
    """Matches user needs with products from JSON catalogs."""
    
    def __init__(self, products_dir: str = "products"):
        """
        Initialize the product matcher.
        
        Args:
            products_dir: Directory containing product JSON files
        """
        self.products_dir = Path(products_dir)
        self.catalogs = self._load_catalogs()
    
    def _load_catalogs(self) -> Dict[str, Dict]:
        """Load all product catalogs from the products directory."""
        catalogs = {}
        
        if not self.products_dir.exists():
            print(f"Warning: Products directory {self.products_dir} does not exist")
            return catalogs
        
        for json_file in self.products_dir.glob("*.json"):
            try:
                with open(json_file, 'r') as f:
                    catalog = json.load(f)
                    niche = catalog.get('niche', json_file.stem)
                    catalogs[niche] = catalog
                    print(f"Loaded {len(catalog.get('products', []))} products from {json_file.name}")
            except Exception as e:
                print(f"Error loading {json_file}: {e}")
        
        return catalogs
    
    def get_catalog_for_subreddit(self, subreddit: str) -> Optional[Dict]:
        """
        Find the product catalog for a given subreddit.
        
        Args:
            subreddit: Subreddit name (without r/)
            
        Returns:
            Product catalog dict or None if not found
        """
        for catalog in self.catalogs.values():
            if subreddit.lower() in [s.lower() for s in catalog.get('subreddits', [])]:
                return catalog
        return None
    
    def find_matching_products(
        self,
        subreddit: str,
        constraints: Dict,
        max_results: int = 3
    ) -> List[Dict]:
        """
        Find products matching user constraints.
        
        Args:
            subreddit: The subreddit name
            constraints: User constraints from AI analysis
                {
                    "experience_level": str,
                    "budget_range": str,
                    "keywords": List[str]
                }
            max_results: Maximum number of products to return
            
        Returns:
            List of matching products, sorted by relevance
        """
        catalog = self.get_catalog_for_subreddit(subreddit)
        if not catalog:
            print(f"No catalog found for r/{subreddit}")
            return []
        
        products = catalog.get('products', [])
        if not products:
            return []
        
        # Score each product
        scored_products = []
        for product in products:
            score = self._score_product(product, constraints)
            if score > 0:
                scored_products.append({
                    'product': product,
                    'score': score
                })
        
        # Sort by score and return top matches
        scored_products.sort(key=lambda x: x['score'], reverse=True)
        return [item['product'] for item in scored_products[:max_results]]
    
    def _score_product(self, product: Dict, constraints: Dict) -> float:
        """
        Score a product based on how well it matches user constraints.
        
        Args:
            product: Product dict from catalog
            constraints: User constraints
            
        Returns:
            Score (higher is better, 0 means no match)
        """
        score = 0.0
        
        # Experience level match (high weight)
        experience_level = constraints.get('experience_level', 'unknown')
        if experience_level != 'unknown':
            product_category = product.get('category', '').lower()
            if experience_level.lower() == product_category:
                score += 10.0
            elif experience_level == 'beginner' and product_category == 'intermediate':
                score += 5.0  # Intermediate can work for beginners
        
        # Keyword matching (medium weight)
        keywords = [k.lower() for k in constraints.get('keywords', [])]
        product_use_cases = [u.lower() for u in product.get('use_cases', [])]
        product_name = product.get('name', '').lower()
        product_desc = product.get('description', '').lower()
        
        for keyword in keywords:
            # Check use cases
            if any(keyword in use_case for use_case in product_use_cases):
                score += 3.0
            # Check name
            if keyword in product_name:
                score += 2.0
            # Check description
            if keyword in product_desc:
                score += 1.0
        
        # Budget matching (low weight, since budget parsing is complex)
        budget_range = constraints.get('budget_range', 'unknown')
        if budget_range != 'unknown' and 'budget' in budget_range.lower():
            # If user mentioned "budget", prefer lower-priced items
            price_range = product.get('price_range', '')
            if any(term in price_range.lower() for term in ['$', 'under', 'budget']):
                score += 2.0
        
        return score
    
    def format_product_for_response(self, product: Dict, affiliate_tag: str) -> Dict:
        """
        Format a product for inclusion in a response.
        
        Args:
            product: Product dict from catalog
            affiliate_tag: Amazon affiliate tag
            
        Returns:
            Formatted product dict with affiliate link
        """
        asin = product.get('amazon_asin', '')
        affiliate_link = f"https://www.amazon.com/dp/{asin}?tag={affiliate_tag}" if asin else None
        
        return {
            'name': product.get('name', 'Unknown Product'),
            'description': product.get('description', ''),
            'price_range': product.get('price_range', 'Price varies'),
            'category': product.get('category', 'general'),
            'affiliate_link': affiliate_link,
            'use_cases': product.get('use_cases', [])
        }
