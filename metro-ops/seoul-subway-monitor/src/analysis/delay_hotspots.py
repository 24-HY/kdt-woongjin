from datetime import datetime
import sys
import os

# Ensure src is in path for imports
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from db_client import SupabaseClient

def analyze_delays():
    print("Fetching data for Delay Hotspot Analysis...")
    db = SupabaseClient()
    data = db.fetch_data(limit=2000)
    
    if not data:
        print("No data found or DB error.")
        return

    # Organize by train_number
    trains = {}
    for row in data:
        t_num = row.get('train_number')
        if not t_num:
            continue
            
        ts_str = row.get('last_rec_time')
        try:
            ts = datetime.strptime(ts_str, "%Y-%m-%d %H:%M:%S")
        except:
            continue
            
        if t_num not in trains:
            trains[t_num] = []
        
        trains[t_num].append({
            'time': ts,
            'station': row.get('station_name'),
            'status': row.get('train_status') # 0:Enter, 1:Arrive, 2:Depart
        })

    print(f"\nAnalyzed {len(trains)} trains.")
    print("\n--- Potential Long Dwell Times (Delays) ---")
    
    detected_delays = []

    for t_num, events in trains.items():
        # Sort events by time
        events.sort(key=lambda x: x['time'])
        
        # Look for Arrival (1) -> Departure (2) at SAME station
        for i in range(len(events) - 1):
            e1 = events[i]
            e2 = events[i+1]
            
            # Check strictly consecutive events for now, or search forward
            # If e1 is Arrive and e2 is Depart at same station
            if e1['status'] == '1' and e2['status'] == '2' and e1['station'] == e2['station']:
                dwell_seconds = (e2['time'] - e1['time']).total_seconds()
                
                # Threshold: e.g., > 60 seconds might be long for some lines, or > 120
                if dwell_seconds > 60:
                    detected_delays.append({
                        'train': t_num,
                        'station': e1['station'],
                        'dwell': dwell_seconds,
                        'time': e1['time']
                    })

    if not detected_delays:
        print("No significant delays detected in the sample (or insufficient data).")
    else:
        # Sort by dwell time desc
        detected_delays.sort(key=lambda x: x['dwell'], reverse=True)
        for d in detected_delays[:10]:
            print(f"Train {d['train']} at {d['station']}: {d['dwell']:.0f} sec dwell (at {d['time']})")

if __name__ == "__main__":
    analyze_delays()
