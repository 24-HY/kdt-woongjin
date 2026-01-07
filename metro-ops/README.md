# Metro Ops: Seoul Subway Monitoring

This project collects real-time subway train locations from the Seoul Open Data Plaza API and analyzes them to monitor operations, specifically focusing on headway (dispatch intervals) and dwell times.

## Setup

1.  **Environment Variables**:
    Copy `.env.example` to `.env` and fill in your Supabase credentials and Seoul Data API key.
    ```bash
    cp .env.example .env
    ```

2.  **Dependencies**:
    Install the required Python packages:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Database**:
    Run the SQL in `schema.sql` in your Supabase SQL Editor to create the necessary table and indexes.

## Usage

### Data Collection
To start collecting data (this currently runs one cycle for all lines):
```bash
python collector.py
```
*Note: For continuous monitoring, set this up as a scheduled task (cron job) or wrap it in a `while True` loop.*

### Data Analysis

#### 1. Headway Monitor (배차 간격 모니터링)
Analyzes the time interval between trains arriving at a specific station.
```bash
cd analysis
python headway_monitor.py
```
*Goal: Detect delays > 10 minutes.*

#### 2. Dwell Time Analysis (정차 시간 분석)
Estimates how long trains stay at a station based on snapshot data.
```bash
cd analysis
python dwell_time_analysis.py
```
*Goal: Identify bottleneck stations where dwelling exceeds 2 minutes.*

## Folder Structure
- `collector.py`: Main script to fetch API data and push to DB.
- `schema.sql`: Database definition.
- `analysis/`: Contains specific analysis scripts.
