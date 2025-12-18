
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import re
import xml.etree.ElementTree as ET

SITEMAP_INDEX = "https://www.shl.com/sitemap.xml"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def get_product_urls():
    print("Fetching Sitemap Index...")
    try:
        resp = requests.get(SITEMAP_INDEX, headers=HEADERS)
        root = ET.fromstring(resp.content)
        
        # XML Namespace
        ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        sub_sitemaps = []
        for sitemap in root.findall('sm:sitemap', ns):
            loc = sitemap.find('sm:loc', ns).text
            # Filter for English US sitemaps to get distinct content
            if 'en_US' in loc:
                sub_sitemaps.append(loc)
                
        print(f"Found {len(sub_sitemaps)} sub-sitemaps for en_US.")
        
        product_urls = set()
        
        for idx, sub_map in enumerate(sub_sitemaps):
            print(f"Parsing sub-sitemap {idx+1}/{len(sub_sitemaps)}: {sub_map}")
            try:
                r = requests.get(sub_map, headers=HEADERS)
                sub_root = ET.fromstring(r.content)
                
                for url in sub_root.findall('sm:url', ns):
                    loc = url.find('sm:loc', ns).text
                    if '/product-catalog/view/' in loc:
                        product_urls.add(loc)
                        
            except Exception as e:
                print(f"Error parsing sub-sitemap {sub_map}: {e}")
                
        print(f"Total Unique Product URLs found: {len(product_urls)}")
        return list(product_urls)
        
    except Exception as e:
        print(f"Critical Sitemap Error: {e}")
        return []

def scrape_details(urls):
    data = []
    print("Scraping product details...")
    
    for i, url in enumerate(urls):
        if i % 10 == 0: print(f"Progress: {i}/{len(urls)}")
        
        try:
            r = requests.get(url, headers=HEADERS, timeout=10)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                
                # Title
                title = soup.title.string.replace('| SHL', '').strip() if soup.title else ""
                
                # Description
                desc_tag = soup.find('meta', attrs={'name': 'description'}) or soup.find('meta', attrs={'property': 'og:description'})
                desc = desc_tag['content'] if desc_tag else ""
                
                # Extract Duration & Type (Heuristics)
                # Looking for text patterns "Duration: X minutes" or inside specific divs
                full_text = soup.get_text(" ", strip=True)
                
                duration = "N/A"
                # Search for "Duration: XX"
                dur_match = re.search(r'Duration[:\s]+(\d+)', full_text, re.IGNORECASE)
                if dur_match:
                    duration = dur_match.group(1)
                    
                # Test Type
                # Often listed as "Test Type: Ability", "Personality", etc.
                # Assuming generic classification for now based on keywords in description/title
                test_types = []
                if "personality" in full_text.lower(): test_types.append("Personality & Behavior")
                if "ability" in full_text.lower() or "aptitude" in full_text.lower(): test_types.append("Ability & Aptitude")
                if "skill" in full_text.lower() or "knowledge" in full_text.lower(): test_types.append("Knowledge & Skills")
                
                if not test_types: test_types = ["General Assessment"]
                
                # Clean URL (shl.com/x/y -> URL)
                data.append({
                    'Assessment_Name': title,
                    'Assessment_url': url,
                    'Description': desc,
                    'Duration': duration,
                    'Test_Type': json.dumps(list(set(test_types))),
                    'Adaptive': "Yes" if "adaptive" in full_text.lower() else "No"
                })
            else:
                print(f"Failed to fetch {url}: {r.status_code}")
                
        except Exception as e:
            print(f"Error scraping {url}: {e}")
            
    return pd.DataFrame(data)

if __name__ == "__main__":
    urls = get_product_urls()
    if urls:
        df = scrape_details(urls)
        df.to_csv('data/shl_catalogue.csv', index=False)
        print(f"Successfully saved {len(df)} products to data/shl_catalogue.csv")
    else:
        print("No URLs found.")
