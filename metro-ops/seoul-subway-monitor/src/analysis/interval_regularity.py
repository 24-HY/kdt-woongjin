from datetime import datetime
import sys
import os

# Ensure src is in path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from db_client import SupabaseClient

def analyze_intervals():
    print("Fetching data for Interval Regularity Analysis...")
    db = SupabaseClient()
    data = db.fetch_data(limit=2000)
    
    if not data:
        print("No data found.")
        return

    print(f"Analyzed {len(data)} records.")
    
    # Group by (station_name, direction_type)
    # Filter only trains that have arrived? Or just use last_rec_time updates at a station.
    # Logic: For a given station, list all train arrivals.
    # However, 'realtimePosition' is a snapshot of where trains ARE.
    # To measure detailed interval at a station, we need historical data of when trains were AT that station.
    # With a snapshot, we might only see current positions.
    # But if we accumulate data (which we did into DB), we have history.
    
    # Grouping
    station_arrivals = {}
    
    for row in data:
        station = row.get('station_name')
        direction = row.get('direction_type') # 0 or 1
        key = (station, direction)
        
        # We need a timestamp. 'recptnDt' (last_rec_time) is when the train reported.
        # Format: 2024-01-07 14:00:00 (Example)
        ts_str = row.get('last_rec_time')
        try:
            # Flexible parsing
            ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            # Fallback if just time or other format?
            continue
            
        if key not in station_arrivals:
            station_arrivals[key] = []
        station_arrivals[key].append(ts)
        
    print("\n--- Interval Analysis Results (Top 5 Stations with multiple trains) ---")
    
    count = 0
    for key, times in station_arrivals.items():
        if len(times) < 2:
            continue
            
        times.sort()
        intervals = []
        for i in range(1, len(times)):
            delta = (times[i] - times[i-1]).total_seconds()
            # Filter out very small intervals (duplicates or same train updates)
            if delta > 30: 
                intervals.append(delta / 60.0) # Minutes
        
        if not intervals:
            continue
            
        avg_interval = sum(intervals) / len(intervals)
        station, direction = key
        dir_str = "Up/Inner" if direction == 0 else "Down/Outer"
        
        print(f"Station: {station} ({dir_str})")
        print(f"  - Count: {len(intervals)}")
        print(f"  - Avg Interval: {avg_interval:.1f} min")
        print(f"  - Min: {min(intervals):.1f} min, Max: {max(intervals):.1f} min")
        
        count += 1
        if count >= 5:
            break

if __name__ == "__main__":
    analyze_intervals()
