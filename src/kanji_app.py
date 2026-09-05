import sqlite3
from datetime import datetime

DATABASE_FILE = "data/kanji_normalized.db"


def search_kanji(character):
    connection = sqlite3.connect(DATABASE_FILE)
    cursor = connection.cursor()

    # Get basic kanji information
    cursor.execute("""
        SELECT id, character, meaning
        FROM kanji
        WHERE character = ?
    """, (character,))

    kanji = cursor.fetchone()

    if not kanji:
        print(f"\nKanji '{character}' not found.")
        connection.close()
        return

    kanji_id, character, meaning = kanji

    print("\n" + "=" * 40)
    print(f"Kanji: {character}")
    print(f"Meaning: {meaning}")

    # Get readings
    cursor.execute("""
        SELECT reading
        FROM readings
        WHERE kanji_id = ?
    """, (kanji_id,))

    readings = cursor.fetchall()

    print("\nReadings:")
    for reading in readings:
        print(f"  • {reading[0]}")

    # Get vocabulary
    cursor.execute("""
        SELECT
            vocabulary.word,
            vocabulary.reading,
            vocabulary.meaning
        FROM vocabulary
        JOIN kanji_vocabulary
            ON vocabulary.id = kanji_vocabulary.vocabulary_id
        WHERE kanji_vocabulary.kanji_id = ?
        LIMIT 10
    """, (kanji_id,))

    vocabulary = cursor.fetchall()

    print("\nVocabulary:")

    if vocabulary:
        for word, reading, meaning in vocabulary:
            print(f"  • {word} ({reading}) — {meaning}")
    else:
        print("  No vocabulary found.")

    # Record review
    result = input("\nDid you get this kanji correct? (y/n): ").strip().lower()

    if result in ("y", "n"):

        # Check whether progress already exists
        cursor.execute("""
            SELECT kanji_id
            FROM user_progress
            WHERE kanji_id = ?
        """, (kanji_id,))

        existing = cursor.fetchone()

        if existing:

            if result == "y":
                cursor.execute("""
                    UPDATE user_progress
                    SET
                        times_reviewed = times_reviewed + 1,
                        correct_count = correct_count + 1,
                        last_reviewed = ?
                    WHERE kanji_id = ?
                """, (datetime.now().isoformat(), kanji_id))

            else:
                cursor.execute("""
                    UPDATE user_progress
                    SET
                        times_reviewed = times_reviewed + 1,
                        incorrect_count = incorrect_count + 1,
                        last_reviewed = ?
                    WHERE kanji_id = ?
                """, (datetime.now().isoformat(), kanji_id))

        else:

            if result == "y":
                cursor.execute("""
                    INSERT INTO user_progress
                    (kanji_id, times_reviewed, correct_count, incorrect_count, last_reviewed)
                    VALUES (?, 1, 1, 0, ?)
                """, (kanji_id, datetime.now().isoformat()))

            else:
                cursor.execute("""
                    INSERT INTO user_progress
                    (kanji_id, times_reviewed, correct_count, incorrect_count, last_reviewed)
                    VALUES (?, 1, 0, 1, ?)
                """, (kanji_id, datetime.now().isoformat()))

        connection.commit()

        print("\nProgress saved!")

    else:
        print("\nReview not recorded.")

    connection.close()


while True:

    character = input(
        "\nEnter a kanji (or 'q' to quit): "
    ).strip()

    if character.lower() == "q":
        print("Goodbye!")
        break

    if not character:
        continue

    search_kanji(character)