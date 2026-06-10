import sqlite3

conn = sqlite3.connect('database/users.db')

cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS interview_results(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    interview_type TEXT,
    score INTEGER
)
''')

conn.commit()
conn.close()

print("Interview Results Table Created Successfully")