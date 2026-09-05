import sqlite3

DATABASE_FILE = "data/kanji_normalized.db"

connection = sqlite3.connect(DATABASE_FILE)
cursor = connection.cursor()

cursor.execute("""
    SELECT
        kanji.character,
        kanji.meaning,
        user_progress.times_reviewed,
        user_progress.correct_count,
        user_progress.incorrect_count,
        ROUND(
            CAST(user_progress.correct_count AS FLOAT)
            / user_progress.times_reviewed * 100,
            1
        ) AS accuracy
    FROM user_progress
    JOIN kanji
        ON user_progress.kanji_id = kanji.id
    WHERE user_progress.times_reviewed >= 2
    ORDER BY accuracy ASC, times_reviewed DESC
    LIMIT 5
""")

results = cursor.fetchall()

print("\n=== Recommended Kanji to Review ===\n")

if not results:
    print("Not enough learning data yet.")

else:
    for character, meaning, reviewed, correct, incorrect, accuracy in results:
        print(
            f"{character} — {meaning} | "
            f"Accuracy: {accuracy}% | "
            f"Reviews: {reviewed}"
        )

connection.close()