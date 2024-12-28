CREATE TABLE user_model (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    email VARCHAR(100),
    username VARCHAR(100),
    password VARCHAR(100),
    role VARCHAR(100)
)