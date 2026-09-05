import sqlite3
import sys

database_file = "data/kanji_normalized.db"

# Get kanji from the command line
if len(sys.argv) < 2:
    print("Usage: python src/query_vocabulary.py <kanji>")
    sys.exit()

search_kanji = sys.argv[1]

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

cursor.execute("""
    SELECT
        kanji.character,
        vocabulary.word,
        vocabulary.reading,
        vocabulary.meaning
    FROM kanji
    JOIN kanji_vocabulary
        ON kanji.id = kanji_vocabulary.kanji_id
    JOIN vocabulary
        ON vocabulary.id = kanji_vocabulary.vocabulary_id
    WHERE kanji.character = ?
    LIMIT 20
""", (search_kanji,))

results = cursor.fetchall()

if not results:
    print(f"No vocabulary found for {search_kanji}")
else:
    print(f"\nVocabulary containing {search_kanji}:\n")

    for character, word, reading, meaning in results:
        print(f"{word} ({reading}) — {meaning}")

connection.close()