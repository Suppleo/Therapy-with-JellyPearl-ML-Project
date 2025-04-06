import streamlit as st
import sqlite3

# --- Meme Library Page ---
st.title("Thư Viện Meme của JellyPearl 📚")
st.write("Khám phá tất cả các meme mà JellyPearl sử dụng để làm sáng lên ngày của bạn!")

# Connect to database
try:
    conn = sqlite3.connect('./emotion_memes.db')
    cursor = conn.cursor()
    cursor.execute("SELECT emotion, meme_path FROM memes ORDER BY emotion")
    memes = cursor.fetchall()
    conn.close()
except sqlite3.Error as e:
    st.error(f"Lỗi khi truy cập cơ sở dữ liệu meme: {e}")
    st.stop()

# Group memes by emotion
emotion_groups = {}
for emotion, meme_path in memes:
    if emotion not in emotion_groups:
        emotion_groups[emotion] = []
    emotion_groups[emotion].append(meme_path)

# Display memes
if emotion_groups:
    for emotion, paths in emotion_groups.items():
        st.subheader(f"Cảm xúc: {emotion}")
        cols = st.columns(min(len(paths), 3))  # Up to 3 memes per row
        for i, path in enumerate(paths):
            with cols[i % 3]:
                try:
                    st.image(path, caption=f"Meme {i+1}", use_container_width=True)
                except Exception as e:
                    st.write(f"Không thể tải meme: {path}")
else:
    st.write("Thư viện meme trống rỗng! JellyPearl đang tìm thêm meme cho bạn.")