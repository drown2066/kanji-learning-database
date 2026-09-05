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
    ORDER BY accuracy ASC
""")

results = cursor.fetchall()

print("\n=== Learning Progress ===\n")

if not results:
    print("No learning data yet.")

else:
    for character, meaning, reviewed, correct, incorrect, accuracy in results:
        print(
            f"{character} — {meaning} | "
            f"Reviewed: {reviewed} | "
            f"Correct: {correct} | "
            f"Incorrect: {incorrect} | "
            f"Accuracy: {accuracy}%"
        )

connection.close()