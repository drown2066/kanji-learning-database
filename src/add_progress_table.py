import sqlite3

database_file = "data/kanji_normalized.db"

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS user_progress (
        kanji_id INTEGER PRIMARY KEY,
        times_reviewed INTEGER DEFAULT 0,
        correct_count INTEGER DEFAULT 0,
        incorrect_count INTEGER DEFAULT 0,
        last_reviewed TEXT,
        
        FOREIGN KEY (kanji_id)
            REFERENCES kanji(id)
    )
""")

connection.commit()
connection.close()

print("User progress table created successfully.")