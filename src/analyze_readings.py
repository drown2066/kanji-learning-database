import sqlite3

database_file = "data/kanji_normalized.db"

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

cursor.execute("""
    SELECT
        kanji.character,
        kanji.meaning,
        COUNT(readings.id) AS reading_count
    FROM kanji
    JOIN readings
        ON kanji.id = readings.kanji_id
    GROUP BY kanji.id
    ORDER BY reading_count DESC
    LIMIT 10
""")

results = cursor.fetchall()

print("Top 10 kanji by number of readings:\n")

for character, meaning, reading_count in results:
    print(f"{character} — {meaning} — {reading_count} readings")

connection.close()