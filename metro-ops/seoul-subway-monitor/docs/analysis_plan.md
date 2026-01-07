# Data Analysis Plan: Seoul Subway Monitoring

This document outlines the priority analysis projects for the Seoul Subway Monitoring System.

## 1. Interval Regularity Analysis (배차 간격 정기성 분석)
**Objective**: Detect bunching (trains too close) or gapping (trains too far) to evaluate service reliability.
- **Method**: 
  - Group data by `station_name` and `direction_type`.
  - Calculate the time difference (`delta_t`) between consecutive `last_rec_time` (or `created_at` arrival times).
  - Identify outliers where `delta_t` deviates significantly from the scheduled headway.
- **Goal**: Identify chronic bottleneck stations or times.

## 2. Delay Hotspot Detection (지연 발생구간 탐지)
**Objective**: Visualize stations where trains spend excessive time dwelling.
- **Method**:
  - Track a specific `train_number` as it moves.
  - Measure the duration between `train_status` 1 (Arrival) and 2 (Departure) at the same station.
  - Compare against average dwell times.
- **Goal**: Real-time dashboard showing "Red Zones" where trains are currently stuck.

## 3. Turnaround Efficiency Analysis (회차 효율성 분석)
**Objective**: Analyze the performance at terminal stations.
- **Method**:
  - Identify trains arriving at `dest_station_name`.
  - Track when the same physical train (likely inferred or if `train_number` changes predictably) re-enters service in the opposite direction.
  - Measure the "Turnaround Time".
- **Goal**: Optimize terminal operations to insert trains back into service faster.

## 4. Congestion/Overtake Analysis (급행/일반 열차 간섭 분석)
**Objective**: specific to lines with express service (e.g., Line 9).
- **Method**:
  - Compare the speed/progress of `is_express=1` vs `is_express=0` trains.
  - Identify segments where express trains significantly slow down behind local trains.
- **Goal**: Suggest timing adjustments to minimize interference.
