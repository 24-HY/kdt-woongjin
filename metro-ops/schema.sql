-- Create the table for real-time subway positions
CREATE TABLE IF NOT EXISTS realtime_subway_positions (
    id BIGSERIAL PRIMARY KEY,
    subway_id VARCHAR(10) NOT NULL,
    line_name VARCHAR(50) NOT NULL,
    train_number VARCHAR(20) NOT NULL,
    station_id VARCHAR(20) NOT NULL,
    station_name VARCHAR(100) NOT NULL,
    updown_line VARCHAR(10) NOT NULL, -- 0: 상행/내선, 1: 하행/외선
    destination_station_id VARCHAR(20),
    destination_station_name VARCHAR(100),
    train_status_code VARCHAR(2) NOT NULL, -- 0:진입, 1:도착, 2:출발, 3:전역출발
    is_express BOOLEAN DEFAULT FALSE,
    is_last_train BOOLEAN DEFAULT FALSE,
    generated_at TIMESTAMP NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexing for performance
CREATE INDEX IF NOT EXISTS idx_subway_generated_at ON realtime_subway_positions (generated_at DESC);
CREATE INDEX IF NOT EXISTS idx_train_number ON realtime_subway_positions (train_number);
CREATE INDEX IF NOT EXISTS idx_station_id ON realtime_subway_positions (station_id);

-- Commentary for the table
COMMENT ON TABLE realtime_subway_positions IS 'Real-time subway train position data from Seoul Metro API';
COMMENT ON COLUMN realtime_subway_positions.updown_line IS '0: Up/Inner, 1: Down/Outer';
COMMENT ON COLUMN realtime_subway_positions.train_status_code IS '0: Arriving, 1: Arrived, 2: Departing, 3: Departed from previous station';
