import sqlite3

# Connect to existing database
db_path = r"C:\Users\ngoct\Kens_Coding_Stuffs\UMT\SPRING 2024\Machine Learning\mother-reaction-app\emotion_memes.db"
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create feedback table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS feedback (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        input_text TEXT NOT NULL,
        predicted_emotion TEXT NOT NULL,
        rating TEXT NOT NULL,  -- 'like' or 'dislike'
        corrected_emotion TEXT,  -- Optional, NULL if not corrected
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
''')

# Verify
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(cursor.fetchall())  # Should show ['memes', 'feedback']
conn.commit()
conn.close()