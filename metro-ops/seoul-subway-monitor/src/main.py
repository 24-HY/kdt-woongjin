import time
from datetime import datetime
import schedule
from config import Config
from api_client import SeoulMetroClient
from db_client import SupabaseClient

def job():
    """The main collection job."""
    print(f"[{datetime.now()}] Starting data collection job...")
    
    api_client = SeoulMetroClient()
    db_client = SupabaseClient()
    
    all_data = []
    
    # Iterate over all target lines
    for line in Config.TARGET_LINES:
        print(f"Fetching data for {line}...")
        raw_data = api_client.fetch_realtime_position(line)
        if raw_data:
            transformed_data = db_client.transform_data(raw_data)
            all_data.extend(transformed_data)
        
        # Gentle delay between requests
        time.sleep(0.5)
    
    # Batch insert all collected data
    if all_data:
        print(f"Inserting {len(all_data)} total records...")
        db_client.insert_data(all_data)
    else:
        print("No data collected this cycle.")
        
    print(f"[{datetime.now()}] Job finished.")

def main():
    print("Initializing Seoul Subway Monitor...")
    
    # Validate configuration
    try:
        Config.validate()
    except ValueError as e:
        print(f"Configuration Error: {e}")
        return

    # Run immediately once
    job()
    
    # Schedule to run every 1 minute
    schedule.every(1).minutes.do(job)
    
    print("Scheduler started. Running every 1 minute. Press Ctrl+C to exit.")
    
    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nStopping scheduler...")

if __name__ == "__main__":
    main()
