#!/usr/bin/env python3
"""
SVG Asset Pipeline Runner
Scrapes SVGs from various sources and stores them in Snowflake with embeddings.
"""

import asyncio
import sys
import os
import time
from pathlib import Path

# Add the project root to the path
sys.path.append(str(Path(__file__).parent.parent))

from config.snowflake_config import SnowflakeConfig
from ingestion.svg_scraper import SVGScraper
from ingestion.embedding_generator import EmbeddingGenerator

class SVGPipeline:
    def __init__(self):
        self.db = SnowflakeConfig()
        self.scraper = SVGScraper()
        self.embedder = EmbeddingGenerator()
        
    def setup_database(self):
        """Initialize database schema"""
        print("🔧 Setting up database schema...")
        
        try:
            # Create database and schema
            self.db.execute_query("CREATE DATABASE IF NOT EXISTS MOTIONFUL_AI")
            self.db.execute_query("USE DATABASE MOTIONFUL_AI")
            self.db.execute_query("CREATE SCHEMA IF NOT EXISTS SVG_ASSETS")
            self.db.execute_query("USE SCHEMA SVG_ASSETS")
            
            # Read and execute schema setup
            schema_path = Path(__file__).parent / "sql" / "schema_setup.sql"
            if schema_path.exists():
                with open(schema_path, 'r') as f:
                    schema_sql = f.read()
                
                # Execute each statement separately
                statements = schema_sql.split(';')
                for stmt in statements:
                    stmt = stmt.strip()
                    if stmt and not stmt.startswith('--'):
                        try:
                            self.db.execute_query(stmt)
                        except Exception as e:
                            if "already exists" not in str(e).lower():
                                print(f"⚠️  SQL Warning: {e}")
            
            print("✅ Database schema setup complete!")
            return True
            
        except Exception as e:
            print(f"❌ Database setup failed: {e}")
            return False
    
    async def scrape_svgs(self, categories=['icons', 'business', 'technology'], limit_per_category=10):
        """Scrape SVGs from various sources"""
        print(f"🔍 Scraping SVGs from {len(categories)} categories...")
        
        all_svgs = []
        
        for category in categories:
            print(f"  📁 Scraping {category}...")
            try:
                svgs = await self.scraper.scrape_svgrepo_category(category, limit=limit_per_category)
                all_svgs.extend(svgs)
                print(f"  ✅ Found {len(svgs)} SVGs in {category}")
            except Exception as e:
                print(f"  ❌ Failed to scrape {category}: {e}")
        
        print(f"📊 Total SVGs scraped: {len(all_svgs)}")
        return all_svgs
    
    def store_assets(self, svg_assets):
        """Store SVG assets in Snowflake"""
        print(f"💾 Storing {len(svg_assets)} assets in Snowflake...")
        
        successful = 0
        failed = 0
        
        for asset in svg_assets:
            try:
                # Store the asset
                if self.db.insert_svg_asset(asset):
                    successful += 1
                    print(f"  ✅ Stored: {asset['title']}")
                else:
                    failed += 1
                    print(f"  ❌ Failed to store: {asset['title']}")
                    
            except Exception as e:
                failed += 1
                print(f"  ❌ Error storing {asset.get('title', 'unknown')}: {e}")
        
        print(f"📈 Storage complete: {successful} successful, {failed} failed")
        return successful, failed
    
    def generate_embeddings(self, svg_assets):
        """Generate and store embeddings for SVG assets"""
        print(f"🧠 Generating embeddings for {len(svg_assets)} assets...")
        
        successful = 0
        failed = 0
        
        for asset in svg_assets:
            try:
                # Generate embedding
                embedding = self.embedder.create_svg_embedding(asset)
                
                # Store embedding
                if self.db.insert_embedding(
                    asset['asset_id'], 
                    embedding, 
                    self.embedder.model_name
                ):
                    successful += 1
                    print(f"  🧠 Embedded: {asset['title']}")
                else:
                    failed += 1
                    print(f"  ❌ Failed embedding: {asset['title']}")
                    
            except Exception as e:
                failed += 1
                print(f"  ❌ Error embedding {asset.get('title', 'unknown')}: {e}")
        
        print(f"🎯 Embeddings complete: {successful} successful, {failed} failed")
        return successful, failed
    
    def get_statistics(self):
        """Get database statistics"""
        try:
            stats = {}
            
            # Asset count
            result = self.db.execute_query("SELECT COUNT(*) as count FROM SVG_ASSETS")
            stats['total_assets'] = result[0]['COUNT'] if result else 0
            
            # Category breakdown
            result = self.db.execute_query("""
                SELECT CATEGORY, COUNT(*) as count 
                FROM SVG_ASSETS 
                GROUP BY CATEGORY 
                ORDER BY count DESC
            """)
            stats['categories'] = {row['CATEGORY']: row['COUNT'] for row in result}
            
            # Embedding count
            result = self.db.execute_query("SELECT COUNT(*) as count FROM SVG_EMBEDDINGS")
            stats['total_embeddings'] = result[0]['COUNT'] if result else 0
            
            return stats
            
        except Exception as e:
            print(f"❌ Error getting statistics: {e}")
            return {}
    
    def search_assets(self, query, limit=5):
        """Search for assets using text similarity"""
        print(f"🔍 Searching for: '{query}'")
        
        try:
            # Generate query embedding
            query_embedding = self.embedder.create_text_embedding(query)
            
            # Get all embeddings (for small dataset)
            embeddings = self.db.execute_query("""
                SELECT e.ASSET_ID, e.EMBEDDING_VECTOR, a.TITLE, a.DESCRIPTION, a.SOURCE_URL
                FROM SVG_EMBEDDINGS e
                JOIN SVG_ASSETS a ON e.ASSET_ID = a.ASSET_ID
            """)
            
            # Find similar assets
            import json
            similar_assets = self.embedder.find_similar_assets(
                query_embedding, 
                [{'asset_id': e['ASSET_ID'], 'embedding': json.loads(e['EMBEDDING_VECTOR'])} for e in embeddings],
                top_k=limit
            )
            
            # Get full asset details
            results = []
            for similar in similar_assets:
                asset_data = next(
                    (e for e in embeddings if e['ASSET_ID'] == similar['asset_id']), 
                    None
                )
                if asset_data:
                    results.append({
                        'title': asset_data['TITLE'],
                        'description': asset_data['DESCRIPTION'],
                        'source_url': asset_data['SOURCE_URL'],
                        'similarity': similar['similarity']
                    })
            
            return results
            
        except Exception as e:
            print(f"❌ Search error: {e}")
            return []

async def main():
    """Main pipeline execution"""
    print("🚀 Starting SVG Asset Pipeline...")
    start_time = time.time()
    
    pipeline = SVGPipeline()
    
    # Step 1: Setup database
    if not pipeline.setup_database():
        print("❌ Database setup failed. Exiting.")
        return
    
    # Step 2: Scrape SVGs
    svg_assets = await pipeline.scrape_svgs(
        categories=['icons', 'business', 'technology', 'education'], 
        limit_per_category=5  # Small batch for testing
    )
    
    if not svg_assets:
        print("❌ No SVGs scraped. Exiting.")
        return
    
    # Step 3: Store assets
    stored_count, failed_count = pipeline.store_assets(svg_assets)
    
    # Step 4: Generate embeddings
    embedded_count, embed_failed = pipeline.generate_embeddings(svg_assets)
    
    # Step 5: Show statistics
    print("\n📊 Pipeline Statistics:")
    stats = pipeline.get_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Step 6: Test search
    print("\n🔍 Testing search functionality:")
    search_results = pipeline.search_assets("business icon", limit=3)
    for i, result in enumerate(search_results[:3], 1):
        print(f"  {i}. {result['title']} (similarity: {result['similarity']:.3f})")
    
    elapsed_time = time.time() - start_time
    print(f"\n🎉 Pipeline completed in {elapsed_time:.2f} seconds")
    print(f"✅ Successfully processed {stored_count} assets with {embedded_count} embeddings")

if __name__ == "__main__":
    # Run the pipeline
    asyncio.run(main()) 