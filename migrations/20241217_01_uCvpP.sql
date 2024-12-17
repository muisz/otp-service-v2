-- 
-- depends: 

CREATE TABLE otps (
    id SERIAL PRIMARY KEY,
    code VARCHAR(6) NOT NULL,
    session_code VARCHAR(10) NOT NULL,
    destination VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NULL
);
