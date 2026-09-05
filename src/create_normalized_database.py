import sqlite3
import pandas as pd

csv_file = "data/jouyou-kanji-clean.csv"
database_file = "data/kanji_normalized.db"

df = pd.read_csv(csv_file)

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

# Create the kanji table
cursor.execute("""
    CREATE TABLE kanji (
        id INTEGER PRIMARY KEY,
        character TEXT NOT NULL,
        meaning TEXT NOT NULL
    )
""")

# Create the readings table
cursor.execute("""
    CREATE TABLE readings (
        id INTEGER PRIMARY KEY,
        kanji_id INTEGER NOT NULL,
        reading TEXT NOT NULL,
        FOREIGN KEY (kanji_id) REFERENCES kanji(id)
    )
""")

# Insert kanji
for index, row in df.iterrows():
    cursor.execute(
        "INSERT INTO kanji (id, character, meaning) VALUES (?, ?, ?)",
        (index + 1, row["kanji"], row["meaning"])
    )

    # Insert each reading
    readings = row["readings"].split(", ")

    for reading in readings:
        cursor.execute(
            "INSERT INTO readings (kanji_id, reading) VALUES (?, ?)",
            (index + 1, reading)
        )

connection.commit()
connection.close()

print("Normalized database created successfully.")
print(f"Total kanji: {len(df)}")