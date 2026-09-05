import sqlite3

database_file = "data/kanji.db"

connection = sqlite3.connect(database_file)
cursor = connection.cursor()

cursor.execute("""
    SELECT kanji, meaning, readings
    FROM kanji
""")

results = cursor.fetchall()

for kanji, meaning, readings in results:
    reading_count = len(readings.split(", "))

    print(kanji, meaning, reading_count)

connection.close()