# snowflake/ingestion/svg_scraper.py
import requests
from bs4 import BeautifulSoup
import re
import json
import hashlib
from typing import List, Dict, Any
import asyncio
import aiohttp
from pathlib import Path
import xml.etree.ElementTree as ET

class SVGScraper:
    def __init__(self):
        self.base_urls = {
            'svgrepo': 'https://www.svgrepo.com',
            'undraw': 'https://undraw.co'
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    async def scrape_svgrepo_category(self, category: str, limit: int = 100) -> List[Dict]:
        """Scrape SVGs from SVGRepo by category"""
        url = f"{self.base_urls['svgrepo']}/vectors/{category}"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                svg_links = soup.find_all('a', href=re.compile(r'/svg/\d+/'))
                results = []
                
                for link in svg_links[:limit]:
                    svg_url = self.base_urls['svgrepo'] + link['href']
                    svg_data = await self.fetch_svg_details(session, svg_url)
                    if svg_data:
                        results.append(svg_data)
                
                return results
    
    async def fetch_svg_details(self, session: aiohttp.ClientSession, url: str) -> Dict:
        """Fetch individual SVG details"""
        try:
            async with session.get(url, headers=self.headers) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # Extract SVG metadata
                title = soup.find('h1').text.strip() if soup.find('h1') else 'Unknown'
                description = soup.find('meta', attrs={'name': 'description'})
                description = description['content'] if description else ''
                
                # Find SVG download link
                download_link = soup.find('a', href=re.compile(r'\.svg$'))
                if not download_link:
                    return None
                
                svg_url = download_link['href']
                if not svg_url.startswith('http'):
                    svg_url = self.base_urls['svgrepo'] + svg_url
                
                # Download SVG content
                async with session.get(svg_url) as svg_response:
                    svg_content = await svg_response.text()
                
                # Parse SVG for metadata
                svg_metadata = self.parse_svg_metadata(svg_content)
                
                return {
                    'asset_id': hashlib.md5(url.encode()).hexdigest(),
                    'title': title,
                    'description': description,
                    'source_url': url,
                    'download_url': svg_url,
                    'svg_content': svg_content,
                    'metadata': svg_metadata,
                    'source': 'svgrepo'
                }
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None
    
    def parse_svg_metadata(self, svg_content: str) -> Dict:
        """Extract metadata from SVG content"""
        try:
            root = ET.fromstring(svg_content)
            
            # Extract dimensions
            width = root.get('width', '100')
            height = root.get('height', '100')
            viewbox = root.get('viewBox', '0 0 100 100')
            
            # Extract colors
            colors = set()
            for elem in root.iter():
                for attr in ['fill', 'stroke', 'color']:
                    if attr in elem.attrib:
                        color = elem.attrib[attr]
                        if color not in ['none', 'transparent']:
                            colors.add(color)
            
            # Count elements
            element_count = len(list(root.iter()))
            
            return {
                'dimensions': {
                    'width': width,
                    'height': height,
                    'viewBox': viewbox
                },
                'colors': list(colors),
                'element_count': element_count,
                'has_text': any(elem.text for elem in root.iter() if elem.text and elem.text.strip())
            }
        except Exception as e:
            print(f"Error parsing SVG metadata: {e}")
            return {}
    
    async def scrape_undraw_illustrations(self, search_term: str = '', limit: int = 50) -> List[Dict]:
        """Scrape illustrations from unDraw"""
        url = f"{self.base_urls['undraw']}/search/{search_term}" if search_term else f"{self.base_urls['undraw']}/illustrations"
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')
                
                # unDraw has a different structure - adapt as needed
                illustration_divs = soup.find_all('div', class_='illustration')
                results = []
                
                for div in illustration_divs[:limit]:
                    # Extract unDraw specific data
                    # This will need to be adapted based on actual unDraw structure
                    pass
                
                return results

# Usage example
async def main():
    scraper = SVGScraper()
    
    # Scrape different categories
    categories = ['icons', 'business', 'technology', 'education', 'medical']
    all_svgs = []
    
    for category in categories:
        print(f"Scraping {category}...")
        svgs = await scraper.scrape_svgrepo_category(category, limit=20)
        all_svgs.extend(svgs)
    
    print(f"Scraped {len(all_svgs)} SVGs total")
    return all_svgs

if __name__ == "__main__":
    asyncio.run(main())