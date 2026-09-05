import sqlite3

database_file = "data/kanji_normalized.db"

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE vocabulary (
        id INTEGER PRIMARY KEY,
        word TEXT NOT NULL,
        reading TEXT,
        meaning TEXT
    )
""")

connection.commit()
connection.close()

print("Vocabulary table created successfully.")