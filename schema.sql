CREATE TABLE expenses (
    id SERIAL PRIMARY KEY,
    date DATE NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    amount INTEGER NOT NULL CHECK (amount > 0)
); 