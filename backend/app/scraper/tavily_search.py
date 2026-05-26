import os
from tavily import TavilyClient

class TavilySearcher:
    def __init__(self):
        # API key should be loaded via python-dotenv in main.py
        self.api_key = os.getenv("TAVILY_API_KEY")
        self.client = TavilyClient(api_key=self.api_key) if self.api_key else None

    def fetch_model_validation(self, model_name: str, asset_category: str) -> dict:
        """
        Takes a predicted model name from Gemini and uses Tavily to fetch an official 
        product image and a trustworthy source link.
        """
        if not self.client:
            print("Warning: TAVILY_API_KEY not set. Cannot validate models.")
            return {"image_url": None, "source": "API Key Missing"}
            
        targeted_query = f"{model_name} {asset_category} official product image"
        
        try:
            # We want search depth = advanced to get good results and images if possible
            res = self.client.search(query=targeted_query, search_depth="advanced", max_results=3, include_images=True)
            
            images = res.get("images", [])
            best_image = images[0] if images else None
            
            source_url = ""
            if res.get("results"):
                # Prefer trusted domains if possible, else take the first valid result
                trusted_domains = ["samsung.com", "apple.com", "gsmarena.com", "amazon", "bestbuy"]
                for result in res["results"]:
                    if any(domain in result.get("url", "").lower() for domain in trusted_domains):
                        source_url = result.get("url", "")
                        break
                
                # Fallback to first result if no trusted domain matched
                if not source_url:
                    source_url = res["results"][0].get("url", "")
                    
            return {
                "image_url": best_image,
                "source": source_url
            }
            
        except Exception as e:
            print(f"Tavily search failed for {model_name}: {e}")
            return {"image_url": None, "source": "Search Failed"}

tavily_searcher = TavilySearcher()
