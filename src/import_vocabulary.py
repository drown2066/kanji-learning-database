import sqlite3
import csv

database_file = "data/kanji_normalized.db"
vocabulary_file = "data/jouyou-kanji-only-words.csv"

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

# Read vocabulary file
vocabulary = []

with open(vocabulary_file, "r", encoding="utf-8") as file:
    reader = csv.reader(file, delimiter=" ", quotechar='"')

    for row in reader:
        word = row[0]
        reading = row[1]
        meaning = " ".join(row[2:]).strip('"')

        vocabulary.append((word, reading, meaning))

# Insert vocabulary
for word, reading, meaning in vocabulary:
    cursor.execute(
        """
        INSERT INTO vocabulary (word, reading, meaning)
        VALUES (?, ?, ?)
        """,
        (word, reading, meaning)
    )

connection.commit()

print(f"Vocabulary imported: {len(vocabulary)}")

connection.close()