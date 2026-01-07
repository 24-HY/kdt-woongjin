import os
import pandas as pd
from supabase import create_client, Client
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path="../.env")

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

def analyze_headway(line_name="1호선", station_name="서울역", direction="0"):
    """
    Analyzes headway (time interval between trains) for a specific station and direction.
    direction: '0' for Up/Inner, '1' for Down/Outer
    """
    print(f"Analyzing headway for {line_name} - {station_name} (Direction: {direction})...")
    
    # Fetch data: arriving trains (status 0) or arriving (1) at the specific station
    # We look at '1' (Arrival/Departure) for more stable timing or '0' (Approach)
    # Using '1' (Arrived/Stopped) is usually better for "time at station"
    try:
        response = supabase.table("realtime_subway_positions") \
            .select("*") \
            .eq("line_name", line_name) \
            .eq("station_name", station_name) \
            .eq("updown_line", direction) \
            .eq("train_status_code", "1") \
            .order("generated_at", desc=False) \
            .execute()
        
        data = response.data
        if not data:
            print("No data found for this criteria.")
            return

        df = pd.DataFrame(data)
        df['generated_at'] = pd.to_datetime(df['generated_at'])
        
        # Calculate time difference between consecutive trains
        df['prev_arrival'] = df['generated_at'].shift(1)
        df['headway_minutes'] = (df['generated_at'] - df['prev_arrival']).dt.total_seconds() / 60
        
        # Filter for reasonable headways (e.g., < 60 mins to exclude long gaps/night breaks)
        df_filtered = df[df['headway_minutes'] < 60]
        
        print("\n--- Headway Statistics (Minutes) ---")
        print(df_filtered['headway_minutes'].describe())
        
        # Check for delays (> 10 mins)
        delays = df_filtered[df_filtered['headway_minutes'] > 10]
        if not delays.empty:
            print(f"\n[ALERT] Found {len(delays)} instances of >10min headway:")
            print(delays[['train_number', 'generated_at', 'headway_minutes']])
        else:
            print("\nNo significant delays detected (>10 mins).")
            
    except Exception as e:
        print(f"Error executing analysis: {e}")

if __name__ == "__main__":
    analyze_headway()
