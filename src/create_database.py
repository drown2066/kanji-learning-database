import sqlite3
import pandas as pd

# File locations
csv_file = "data/jouyou-kanji-clean.csv"
database_file = "data/kanji.db"

# Load the cleaned CSV
df = pd.read_csv(csv_file)

# Connect to SQLite
connection = sqlite3.connect(database_file)

# Write the DataFrame to a database table
df.to_sql(
    "kanji",
    connection,
    if_exists="replace",
    index=False
)

connection.close()

print("Database created successfully.")
print(f"Total kanji added: {len(df)}")