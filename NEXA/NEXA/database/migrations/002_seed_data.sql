-- NEXA World State Seed Data
-- Insert initial world state

INSERT INTO world_state (
    simulation_day,
    simulation_time,
    mayor_approval,
    food_prices_change,
    unemployment_rate,
    union_anger,
    crime_rate
) VALUES (
    1,
    '00:00:00',
    50.00,
    0.00,
    10.00,
    50.00,
    20.00
);

-- Insert a default city
INSERT INTO cities (name) VALUES ('Nexa City');

-- Insert initial economy metrics
INSERT INTO economy (metric_name, metric_value) VALUES
    ('gdp', 1000000.00),
    ('inflation_rate', 2.50),
    ('interest_rate', 3.00);

-- Insert initial politics metrics
INSERT INTO politics (metric_name, metric_value) VALUES
    ('government_approval', 50.00),
    ('corruption_index', 30.00);
