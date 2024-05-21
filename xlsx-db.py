import pandas as pd
import sqlite3
import os

file_path = os.path.join('Files', 'data.xlsx')
db_name = 'data.db'

conn = sqlite3.connect(db_name)

xl = pd.ExcelFile(file_path)

dfs = []

for sheet_name in xl.sheet_names:
    df = pd.read_excel(xl, sheet_name)
    dfs.append(df)


combined_df = pd.concat(dfs, ignore_index=True)

combined_df.to_sql('users', conn, if_exists='replace', index=False)

conn.close()

print("Excel file successfully converted to a single SQLite table in xlsx.db.")
