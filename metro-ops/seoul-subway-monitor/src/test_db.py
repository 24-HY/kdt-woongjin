from config import Config
from db_client import SupabaseClient
import json

def test_insert():
    db = SupabaseClient()
    
    # Sample data matching the transformation logic
    sample_data = [{
        "line_id": "1001",
        "line_name": "1호선",
        "station_id": "1001000133",
        "station_name": "서울역",
        "train_number": "K1234",
        "last_rec_date": "20240107",
        "last_rec_time": "143000",
        "direction_type": 0,
        "dest_station_id": "1001000100",
        "dest_station_name": "소요산",
        "train_status": "1",
        "is_express": "0",
        "is_last_train": False
    }]
    
    print("Attempting to insert sample data...")
    try:
        db.insert_data(sample_data)
        print("Success!")
    except Exception as e:
        print(f"Failed via client: {e}")
        # Manual attempt to see raw response if client didn't print it
        import requests
        headers = {
            "apikey": Config.SUPABASE_KEY,
            "Authorization": f"Bearer {Config.SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=minimal"
        }
        url = f"{Config.SUPABASE_URL}/rest/v1/{db.table_name}"
        resp = requests.post(url, headers=headers, data=json.dumps(sample_data))
        print(f"Status: {resp.status_code}")
        print(f"Body: {resp.text}")

if __name__ == "__main__":
    test_insert()
