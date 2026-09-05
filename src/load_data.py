import csv
import pandas as pd

input_file = "data/jouyou-kanji.csv"
output_file = "data/jouyou-kanji-clean.csv"

kanji_data = []

with open(input_file, "r", encoding="utf-8") as file:
    for line in file:
        parts = line.strip().split()

        kanji = parts[0]
        meaning = parts[1]
        readings = parts[2].split("/")

        kanji_data.append({
            "kanji": kanji,
            "meaning": meaning,
            "readings": ", ".join(readings)
        })

with open(output_file, "w", encoding="utf-8", newline="") as file:
    writer = csv.DictWriter(
        file,
        fieldnames=["kanji", "meaning", "readings"]
    )

    writer.writeheader()
    writer.writerows(kanji_data)

# Load the cleaned data with Pandas
df = pd.read_csv(output_file)

print("\nDataset preview:")
print(df.head())

print("\nDataset information:")
print(df.info())

print(f"\nTotal kanji: {len(df)}")

# Basic analysis

df["reading_count"] = df["readings"].str.split(", ").str.len()

print("\nBasic statistics:")
print(f"Total kanji: {len(df)}")
print(f"Average readings per kanji: {df['reading_count'].mean():.2f}")
print(f"Most readings for one kanji: {df['reading_count'].max()}")

print("\nKanji with the most readings:")
print(
    df.nlargest(10, "reading_count")[["kanji", "meaning", "readings", "reading_count"]]
)