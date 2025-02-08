-- DROP TABLE IF EXISTS drugs;
-- DROP TABLE IF EXISTS adverse_events;
-- DROP TABLE IF EXISTS recalls;

CREATE TABLE drugs (
    drug_id SERIAL PRIMARY KEY,
    type VARCHAR(255),
    name VARCHAR(255) NOT NULL
);

CREATE TABLE adverse_events (
    event_id SERIAL PRIMARY KEY,
    sender JSON,
    receiver JSON,
    patient JSON,
    receivedate DATE,
    reportduplicate JSON,
    occurcountry VARCHAR(255)
);

CREATE TABLE recalls (
    recall_id SERIAL PRIMARY KEY,
    reason_for_recall TEXT,
    recall_initiation_date DATE,
    country VARCHAR(255)
);



