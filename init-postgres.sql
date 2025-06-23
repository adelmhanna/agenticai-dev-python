-- Create a sample table for relational data
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT NOT NULL,
    email TEXT
);

-- Insert sample data
INSERT INTO users (username, email) VALUES ('hanna', 'adel.hanna@gmail.com');
