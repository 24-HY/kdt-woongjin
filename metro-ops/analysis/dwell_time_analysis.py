import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="../.env")

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def analyze_dwell_time(line_name="1호선", station_name="서울역"):
    """
    Analyzes dwell time (time spent at station) for trains.
    Requires capturing both Arrival (0) and Departure (1/2) events for the same train.
    """
    print(f"Analyzing dwell time for {line_name} - {station_name}...")
    
    try:
        # Fetch all events for this station
        response = supabase.table("realtime_subway_positions") \
            .select("*") \
            .eq("line_name", line_name) \
            .eq("station_name", station_name) \
            .order("generated_at", desc=False) \
            .execute()
        
        data = response.data
        if not data:
            print("No data found.")
            return

        df = pd.DataFrame(data)
        df['generated_at'] = pd.to_datetime(df['generated_at'])
        
        # We need to group by train_number and calculate Is there a '0' and a subsequent '1' or '2'?
        # 0: Enter/Arrive, 1: Arrived/Stopped, 2: Depart
        # Dwell time ~ Time(Departure) - Time(Arrival)
        
        results = []
        
        for train_no, group in df.groupby('train_number'):
            # Find arrival time (min time with status 0 or 1)
            # Find departure time (max time with status 2, or max time with status 1 if 2 missing?)
            # This is tricky with snapshots. We estimate by (Last Seen at Station) - (First Seen at Station)
            
            first_seen = group['generated_at'].min()
            last_seen = group['generated_at'].max()
            
            dwell_seconds = (last_seen - first_seen).total_seconds()
            
            # Filter distinct status codes seen
            codes = group['train_status_code'].unique()
            
            if dwell_seconds > 0:
                results.append({
                    'train_number': train_no,
                    'dwell_seconds': dwell_seconds,
                    'arrived_at': first_seen,
                    'status_codes': codes
                })
        
        if not results:
            print("Insufficient data to calculate dwell times.")
            return

        results_df = pd.DataFrame(results)
        
        print("\n--- Dwell Time Statistics (Seconds) ---")
        print(results_df['dwell_seconds'].describe())
        
        # Long stops > 2 minutes (120s)
        long_stops = results_df[results_df['dwell_seconds'] > 120]
        if not long_stops.empty:
            print(f"\n[ALERT] {len(long_stops)} trains stopped for > 2 minutes:")
            print(long_stops.sort_values('dwell_seconds', ascending=False).head(5))
            
    except Exception as e:
        print(f"Error during analysis: {e}")

if __name__ == "__main__":
    analyze_dwell_time()
