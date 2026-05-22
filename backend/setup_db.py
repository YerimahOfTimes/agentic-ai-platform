import sqlite3


conn = sqlite3.connect("database/company.db")

cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY,
    name TEXT,
    role TEXT,
    salary INTEGER
)
""")

cursor.execute("""
INSERT INTO employees (name, role, salary)
VALUES
('John', 'ML Engineer', 5000),
('Sarah', 'Backend Engineer', 4500),
('David', 'Data Scientist', 6000)
""")

conn.commit()
conn.close()

print("Database created successfully.")
