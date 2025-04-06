import sqlite3
conn = sqlite3.connect('./emotion_memes.db')
cursor = conn.cursor()
cursor.execute("SELECT * FROM feedback")
print(cursor.fetchall())
conn.close()