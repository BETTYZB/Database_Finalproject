-- Drop tables if they already exist (optional but helpful during dev)
DROP TABLE IF EXISTS investments;
DROP TABLE IF EXISTS entrepreneurs;
DROP TABLE IF EXISTS investors;

-- Create investors table
CREATE TABLE investors (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    country VARCHAR(100),
    available_funds DECIMAL,
    industry_focus VARCHAR(100),
    investment_stage VARCHAR(50),
    status VARCHAR(50)
);

-- Create entrepreneurs table
CREATE TABLE entrepreneurs (
    id UUID PRIMARY KEY,
    name VARCHAR(255),
    startup_name VARCHAR(255),
    industry VARCHAR(100),
    funding_needed DECIMAL,
    founded_year INT,
    location VARCHAR(100),
    startup_stage VARCHAR(50)
);

-- Create investments table
CREATE TABLE investments (
    id UUID PRIMARY KEY,
    investor_id UUID REFERENCES investors(id),
    entrepreneur_id UUID REFERENCES entrepreneurs(id),
    amount DECIMAL,
    date DATE,
    stage VARCHAR(50)
);
