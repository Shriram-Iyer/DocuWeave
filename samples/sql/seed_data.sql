-- DocuWeave sample seed data
-- Matches the end-to-end scenario described in the README.
-- Load against your data DB:
--   psql "$DATA_DB_URL" -f samples/sql/seed_data.sql

CREATE TABLE IF NOT EXISTS jobs (
    job_id     VARCHAR(50) PRIMARY KEY,
    job_name   VARCHAR(100),
    department VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS users (
    user_id    VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100),
    last_name  VARCHAR(100),
    email      VARCHAR(200),
    salary     NUMERIC(10,2),
    job_id     VARCHAR(50)
);

INSERT INTO jobs (job_id, job_name, department) VALUES
    ('job_eng_senior',  'Senior Engineer',   'Engineering'),
    ('job_eng_junior',  'Junior Engineer',   'Engineering'),
    ('job_design_lead', 'Design Lead',       'Design'),
    ('job_pm',          'Product Manager',   'Product')
ON CONFLICT DO NOTHING;

INSERT INTO users (user_id, first_name, last_name, email, salary, job_id) VALUES
    ('u1', 'Alice',   'Smith',   'alice@example.com',   7500.00, 'job_eng_senior'),
    ('u2', 'Bob',     'Jones',   'bob@example.com',     6800.00, 'job_eng_senior'),
    ('u3', 'Carol',   'Williams','carol@example.com',   5200.00, 'job_eng_junior'),
    ('u4', 'David',   'Brown',   'david@example.com',   8500.00, 'job_design_lead'),
    ('u5', 'Eve',     'Davis',   'eve@example.com',     9100.00, 'job_pm')
ON CONFLICT DO NOTHING;
