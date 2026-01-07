import os
import time
import requests
import json
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SEOUL_API_KEY = os.getenv("SEOUL_API_KEY", "sample") # Default to 'sample'

# Mapping API fields to database columns
FIELD_MAP = {
    "subwayId": "subway_id",
    "subwayNm": "line_name",
    "trainNo": "train_number",
    "statnId": "station_id",
    "statnNm": "station_name",
    "updnLine": "updown_line",
    "statnTid": "destination_station_id",
    "statnTnm": "destination_station_name",
    "trainSttus": "train_status_code",
    "directAt": "is_express",
    "lstcarAt": "is_last_train",
    "recptnDt": "generated_at"
}

def fetch_metro_data(line_name="1호선"):
    """Fetch real-time position data for a specific line."""
    url = f"http://swopenapi.seoul.go.kr/api/subway/{SEOUL_API_KEY}/json/realtimePosition/0/100/{line_name}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if "realtimePositionList" in data:
            return data["realtimePositionList"]
        else:
            print(f"No data for line {line_name}: {data.get('errorMessage', {}).get('message')}")
            return []
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def transform_data(raw_list):
    """Transform API data to match database schema."""
    transformed = []
    for item in raw_list:
        row = {}
        for api_field, db_col in FIELD_MAP.items():
            val = item.get(api_field)
            
            # Type conversions
            if db_col in ["is_express", "is_last_train"]:
                val = True if val == "1" else False
            
            row[db_col] = val
        transformed.append(row)
    return transformed

def insert_to_supabase(data_list):
    """Insert data into Supabase via REST API."""
    if not data_list:
        return
    
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json",
        "Prefer": "return=minimal"
    }
    
    url = f"{SUPABASE_URL}/rest/v1/realtime_subway_positions"
    
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data_list))
        response.raise_for_status()
        print(f"Successfully inserted {len(data_list)} records.")
    except Exception as e:
        print(f"Error inserting to Supabase: {e}")
        if hasattr(e, 'response') and e.response:
            print(f"Response: {e.response.text}")

def run_collector():
    """Main loop to collect data for major lines."""
    target_lines = ["1호선", "2호선", "3호선", "4호선", "5호선", "6호선", "7호선", "8호선", "9호선"]
    
    print(f"Starting collection at {datetime.now()}...")
    
    all_data = []
    for line in target_lines:
        print(f"Fetching {line}...")
        raw_data = fetch_metro_data(line)
        transformed = transform_data(raw_data)
        all_data.extend(transformed)
        time.sleep(1) # Be polite to the API
        
    insert_to_supabase(all_data)
    print(f"Finished collection cycle at {datetime.now()}.")

if __name__ == "__main__":
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("Error: SUPABASE_URL and SUPABASE_KEY must be set in .env file.")
    else:
        # Run once for demonstration; in production, use a scheduler or loop
        run_collector()
