import pandas as pd
import sqlite3
import os

# Define the file and database names
file_path = os.path.join('Files', 'data.xlsx')
db_name = 'data.db'

# Connect to the SQLite database
conn = sqlite3.connect(db_name)

# Read the Excel file
xl = pd.ExcelFile(file_path)

# List to hold DataFrames from each sheet
dfs = []

# Loop through each sheet in the Excel file
for sheet_name in xl.sheet_names:
    df = pd.read_excel(xl, sheet_name)
    dfs.append(df)

# Combine all DataFrames into one
combined_df = pd.concat(dfs, ignore_index=True)

# Save the combined DataFrame to the SQLite database
combined_df.to_sql('users', conn, if_exists='replace', index=False)

# Close the database connection
conn.close()

print("Excel file successfully converted to a single SQLite table in xlsx.db.")
