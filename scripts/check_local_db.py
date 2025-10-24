import os
import sqlite3
import sys

# locate dev.db relative to project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(project_root, 'dev.db')

if not os.path.exists(db_path):
    print(f"dev.db not found at: {db_path}")
    sys.exit(0)

print(f"Found dev.db at: {db_path}")
conn = sqlite3.connect(db_path)
cur = conn.cursor()
cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = [r[0] for r in cur.fetchall()]
print('Tables:', tables)
for t in tables:
    try:
        cur.execute(f"SELECT COUNT(*) FROM {t}")
        cnt = cur.fetchone()[0]
        print(f"{t}: {cnt} rows")
    except Exception as e:
        print(f"Could not count rows for table {t}: {e}")
conn.close()
