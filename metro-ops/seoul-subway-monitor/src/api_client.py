import requests
import urllib.parse
from config import Config

class SeoulMetroClient:
    """Client for interacting with Seoul Open Data API."""
    
    BASE_URL = "http://swopenapi.seoul.go.kr/api/subway"

    def __init__(self):
        self.api_key = Config.SEOUL_API_KEY

    def fetch_realtime_position(self, line_name: str) -> list:
        """
        Fetch real-time train positions for a specific line.
        
        Args:
            line_name (str): The name of the subway line (e.g., '1호선').
        
        Returns:
            list: A list of raw dictionaries containing train position data.
        """
        # Encode line name for URL
        encoded_line_name = urllib.parse.quote(line_name)
        
        # Construct URL: /api/subway/{KEY}/json/realtimePosition/{START}/{END}/{LINE}
        url = f"{self.BASE_URL}/{self.api_key}/json/realtimePosition/0/100/{encoded_line_name}"
        
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if "realtimePositionList" in data:
                return data["realtimePositionList"]
            
            # Handle API specific error messages within 200 OK
            error_msg = data.get('errorMessage', {}).get('message')
            if error_msg:
                print(f"API Error for {line_name}: {error_msg}")
            
            return []
            
        except requests.exceptions.RequestException as e:
            print(f"Network error fetching data for {line_name}: {e}")
            return []
        except Exception as e:
            print(f"Unexpected error fetching data for {line_name}: {e}")
            return []
