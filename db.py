import sqlite3

# Connect and clear old data
db_path = r"C:\Users\ngoct\Kens_Coding_Stuffs\UMT\SPRING 2024\Machine Learning\mother-reaction-app\emotion_memes.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS memes")
cursor.execute('''
    CREATE TABLE memes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        emotion TEXT NOT NULL,
        meme_path TEXT NOT NULL
    )
''')

# Updated meme data with relative paths
meme_data = [
    ("Anger", "./memes/anger_1.jpg"),
    ("Anger", "./memes/anger_2.jpg"),
    ("Anger", "./memes/anger_3.jpg"),
    ("Disgust", "./memes/disgust_1.jpg"),
    ("Disgust", "./memes/disgust_2.jpg"),
    ("Enjoyment", "./memes/enjoyment_1.jpg"),
    ("Enjoyment", "./memes/enjoyment_2.jpg"),
    ("Enjoyment", "./memes/enjoyment_3.jpg"),
    ("Sadness", "./memes/sadness_1.jpg"),
    ("Sadness", "./memes/sadness_2.jpg"),
    ("Sadness", "./memes/sadness_3.jpg"),
    ("Fear", "./memes/fear_1.jpg"),
    ("Fear", "./memes/fear_2.jpg"),
    ("Surprise", "./memes/surprise_1.jpg"),
    ("Surprise", "./memes/surprise_2.jpg"),
    ("Other", "./memes/other_1.jpg"),
    ("Other", "./memes/other_2.jpg"),
]
cursor.executemany("INSERT INTO memes (emotion, meme_path) VALUES (?, ?)", meme_data)
conn.commit()

# Verify
cursor.execute("SELECT * FROM memes")
print(cursor.fetchall())
conn.close()