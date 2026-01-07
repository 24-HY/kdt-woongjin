import requests
import json
from datetime import datetime
from config import Config

class SupabaseClient:
    """Client for interacting with Supabase Database."""
    
    def __init__(self):
        self.url = Config.SUPABASE_URL
        self.key = Config.SUPABASE_KEY
        self.headers = {
            "apikey": self.key,
            "Authorization": f"Bearer {self.key}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        self.table_name = "realtime_subway_positions"

    def transform_data(self, raw_data: list) -> list:
        """
        Transform raw API data into the DB schema format.
        
        Args:
            raw_data (list): List of dictionaries from the API.
            
        Returns:
            list: List of dictionaries matching the DB schema.
        """
        transformed = []
        for item in raw_data:
            try:
                row = {
                    "line_id": item.get("subwayId"),
                    "line_name": item.get("subwayNm"),
                    "station_id": item.get("statnId"),
                    "station_name": item.get("statnNm"),
                    "train_number": item.get("trainNo"),
                    "last_rec_date": item.get("lastRecptnDt"),
                    "last_rec_time": item.get("recptnDt"),
                    "direction_type": int(item.get("updnLine")) if item.get("updnLine") and item.get("updnLine").isdigit() else None,
                    "dest_station_id": item.get("statnTid"),
                    "dest_station_name": item.get("statnTnm"),
                    "train_status": item.get("trainSttus"), # Keep as string or map if needed. Schema says 0,1,2,3 which are codes.
                    "is_express": item.get("directAt"), # Often '0' or '1'
                    "is_last_train": True if item.get("lstcarAt") == "1" else False,
                    # created_at is handled by DB default
                }
                
                # Handling 'directAt' usually being '0' or '1' string
                # If exact mapping needed: 1:급행, 0:아님, 7:특급. DB expects relevant type.
                # Assuming DB column is text or int. Let's keep it as is, or cast to int if numeric.
                # Just passing through what we get, or safely casting if needed.
                # item['directAt'] comes as string "0" or "1".
                
                transformed.append(row)
            except Exception as e:
                print(f"Error transforming item {item}: {e}")
                continue
                
        return transformed

    def insert_data(self, data: list):
        """
        Insert transformed data into Supabase.
        
        Args:
            data (list): List of transformed data dictionaries.
        """
        if not data:
            return

        insert_url = f"{self.url}/rest/v1/{self.table_name}"
        
        try:
            response = requests.post(insert_url, headers=self.headers, data=json.dumps(data), timeout=15)
            response.raise_for_status()
            print(f"Successfully inserted {len(data)} records.")
        except requests.exceptions.RequestException as e:
            print(f"Error inserting to Supabase: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response Status: {e.response.status_code}")
                print(f"Response Body: {e.response.text}")

    def fetch_data(self, limit=1000) -> list:
        """
        Fetch latest data from Supabase.
        
        Args:
            limit (int): Number of records to fetch.
            
        Returns:
            list: List of records.
        """
        url = f"{self.url}/rest/v1/{self.table_name}?select=*&order=created_at.desc&limit={limit}"
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []
