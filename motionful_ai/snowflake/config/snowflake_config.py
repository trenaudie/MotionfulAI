# snowflake/config/snowflake_config.py
import snowflake.connector
from snowflake.connector import DictCursor
from typing import Dict, Any, List, Optional
import streamlit as st

class SnowflakeConfig:
    def __init__(self):
        # Use the working credentials directly
        self.connection_params = {
            'user': 'YIKESAXE',
            'account': 'HIVHNPF-CDC54457',
            'password': 'Javier@3094491',  # Replace with actual password
            'warehouse': 'COMPUTE_WH',
            'role': 'ACCOUNTADMIN',
            'database': 'MOTIONFUL_AI',
            'schema': 'SVG_ASSETS'
        }
    
    def get_connection(self):
        return snowflake.connector.connect(**self.connection_params)
    
    def execute_query(self, query: str, params: Optional[List] = None) -> List[Dict]:
        """Execute a query and return results"""
        with self.get_connection() as conn:
            with conn.cursor(DictCursor) as cursor:
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                return cursor.fetchall()
    
    def execute_many(self, query: str, data: List[List]) -> int:
        """Execute query with multiple parameter sets"""
        with self.get_connection() as conn:
            with conn.cursor() as cursor:
                cursor.executemany(query, data)
                return cursor.rowcount
    
    def insert_svg_asset(self, asset_data: Dict) -> bool:
        """Insert SVG asset into database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                import json
                
                # Convert complex data types to JSON strings
                # Convert to JSON strings for storage
                tags_json = json.dumps(asset_data.get('tags', []))
                colors_json = json.dumps(asset_data.get('colors', []))
                metadata_json = json.dumps(asset_data.get('metadata', {}))
                
                # Insert into SVG_ASSETS using subquery to convert JSON to VARIANT
                asset_query = """
                INSERT INTO SVG_ASSETS (
                    ASSET_ID, TITLE, DESCRIPTION, CATEGORY, SOURCE_URL,
                    TAGS, COLOR_PALETTE, DIMENSIONS, CREATED_AT
                ) 
                SELECT %s, %s, %s, %s, %s, 
                       PARSE_JSON(%s), PARSE_JSON(%s), PARSE_JSON(%s), CURRENT_TIMESTAMP()
                """
                
                cursor.execute(asset_query, [
                    asset_data['asset_id'],
                    asset_data['title'],
                    asset_data['description'],
                    asset_data.get('category', 'icons'),
                    asset_data['source_url'],
                    tags_json,
                    colors_json,
                    metadata_json
                ])
                
                # Insert into SVG_CONTENT using subquery to convert JSON to VARIANT
                content_query = """
                INSERT INTO SVG_CONTENT (
                    ASSET_ID, SVG_DATA, SVG_TEXT, SVG_METADATA
                ) 
                SELECT %s, PARSE_JSON(%s), %s, PARSE_JSON(%s)
                """
                
                svg_json = json.dumps({
                    'svg_content': asset_data['svg_content'],
                    'download_url': asset_data['download_url']
                })
                
                content_metadata_json = json.dumps(asset_data.get('metadata', {}))
                
                cursor.execute(content_query, [
                    asset_data['asset_id'],
                    svg_json,
                    asset_data['title'] + ' ' + asset_data['description'],
                    content_metadata_json
                ])
                
                cursor.close()
                return True
                
        except Exception as e:
            print(f"❌ Error inserting asset {asset_data['asset_id']}: {e}")
            return False
    
    def insert_embedding(self, asset_id: str, embedding: List[float], model_name: str) -> bool:
        """Insert embedding for an asset"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()
                
                import json
                
                # Convert embedding vector to JSON array format for Snowflake
                embedding_json = json.dumps(embedding)
                
                query = """
                INSERT INTO SVG_EMBEDDINGS (
                    ASSET_ID, EMBEDDING_VECTOR, EMBEDDING_MODEL, CREATED_AT
                ) 
                SELECT %s, PARSE_JSON(%s), %s, CURRENT_TIMESTAMP()
                """
                
                cursor.execute(query, [asset_id, embedding_json, model_name])
                cursor.close()
                return True
                
        except Exception as e:
            print(f"❌ Error inserting embedding for {asset_id}: {e}")
            return False

    def search_assets(self, query_embedding: List[float], limit: int = 10) -> List[Dict]:
        """Search assets using semantic similarity"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(DictCursor)
                
                import json
                query_embedding_json = json.dumps(query_embedding)
                
                # Calculate cosine similarity using Snowflake's VECTOR_COSINE_SIMILARITY
                search_query = """
                SELECT 
                    a.ASSET_ID,
                    a.TITLE,
                    a.DESCRIPTION,
                    a.CATEGORY,
                    a.SOURCE_URL,
                    a.TAGS,
                    a.COLOR_PALETTE,
                    c.SVG_DATA,
                    e.EMBEDDING_VECTOR,
                    VECTOR_COSINE_SIMILARITY(e.EMBEDDING_VECTOR, PARSE_JSON(%s)) as SIMILARITY_SCORE
                FROM SVG_ASSETS a
                JOIN SVG_CONTENT c ON a.ASSET_ID = c.ASSET_ID
                JOIN SVG_EMBEDDINGS e ON a.ASSET_ID = e.ASSET_ID
                ORDER BY SIMILARITY_SCORE DESC
                LIMIT %s
                """
                
                cursor.execute(search_query, [query_embedding_json, limit])
                results = cursor.fetchall()
                cursor.close()
                return results
                
        except Exception as e:
            print(f"❌ Error searching assets: {e}")
            return []

    def get_analytics_data(self) -> Dict:
        """Get analytics data for dashboard"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor(DictCursor)
                
                # Get basic statistics
                stats_query = """
                SELECT 
                    COUNT(*) as total_assets,
                    COUNT(DISTINCT CATEGORY) as total_categories,
                    COUNT(DISTINCT ASSET_ID) as unique_assets
                FROM SVG_ASSETS
                """
                
                cursor.execute(stats_query)
                stats = cursor.fetchone()
                
                # Get category distribution
                category_query = """
                SELECT CATEGORY, COUNT(*) as count
                FROM SVG_ASSETS
                GROUP BY CATEGORY
                ORDER BY count DESC
                """
                
                cursor.execute(category_query)
                categories = cursor.fetchall()
                
                cursor.close()
                
                return {
                    'total_assets': stats['TOTAL_ASSETS'] if stats else 0,
                    'total_categories': stats['TOTAL_CATEGORIES'] if stats else 0,
                    'unique_assets': stats['UNIQUE_ASSETS'] if stats else 0,
                    'category_distribution': categories
                }
                
        except Exception as e:
            print(f"❌ Error getting analytics data: {e}")
            return {}

# Streamlit connection (cached)
@st.cache_resource
def get_snowflake_connection():
    return SnowflakeConfig()