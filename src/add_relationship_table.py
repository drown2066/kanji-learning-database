import sqlite3

database_file = "data/kanji_normalized.db"

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE kanji_vocabulary (
        kanji_id INTEGER NOT NULL,
        vocabulary_id INTEGER NOT NULL,

        PRIMARY KEY (kanji_id, vocabulary_id),

        FOREIGN KEY (kanji_id)
            REFERENCES kanji(id),

        FOREIGN KEY (vocabulary_id)
            REFERENCES vocabulary(id)
    )
""")

connection.commit()
connection.close()

print("Kanji-vocabulary relationship table created successfully.")