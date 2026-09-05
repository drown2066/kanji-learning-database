import sqlite3

database_file = "data/kanji_normalized.db"

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

# Get all Jōyō kanji
cursor.execute("SELECT id, character FROM kanji")

kanji_lookup = {
    character: kanji_id
    for kanji_id, character in cursor.fetchall()
}

# Get all vocabulary
cursor.execute("SELECT id, word FROM vocabulary")

vocabulary = cursor.fetchall()

relationship_count = 0

for vocabulary_id, word in vocabulary:

    for character in word:

        if character in kanji_lookup:

            kanji_id = kanji_lookup[character]

            cursor.execute(
                """
                INSERT OR IGNORE INTO kanji_vocabulary
                (kanji_id, vocabulary_id)
                VALUES (?, ?)
                """,
                (kanji_id, vocabulary_id)
            )

            relationship_count += 1

connection.commit()
connection.close()

print(f"Kanji-vocabulary relationships created: {relationship_count}")