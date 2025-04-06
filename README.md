Got it! Here's the entire rewritten `README.md` in **one single copiable markdown code block**:

````markdown
# Therapy with JellyPearl 🪐

A quirky multi-page web app where users can receive cosmic therapy from JellyPearl, an interdimensional therapist, or browse a meme library. Powered by **PhoBERT** for emotion prediction, **Quasar Alpha** for witty advice, and a **SQLite-backed meme collection**.

---

## 🌟 Features

- **Therapy Page**:  
  Share your thoughts in Vietnamese → Predict emotion with PhoBERT → Get 3-sentence advice from JellyPearl with dark/sexual humor (minimal cursing, no politics) → See a matching meme.  
  Rate the advice (👍 Thích / 👎 Không thích) and correct the emotion if necessary.

- **Meme Library**:  
  Browse all stored memes by emotion from the database.

- **Feedback System**:  
  Likes, dislikes, and corrections are stored in SQLite for future model improvements.

---

## 🚀 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mother-reaction-app.git
cd mother-reaction-app
```
````

### 2. Install Dependencies

```bash
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add Environment Variable

Create a `.env` file in the root directory:

```env
OPENROUTER_API_KEY=your-key-here
```

### 4. Ensure Required Assets Are Present

Make sure the following are in the root directory:

```
phobert_best/         # PhoBERT model files
emotion_memes.db      # SQLite DB (includes memes + feedback)
memes/                # Folder with meme images
```

### 5. Run Locally

```bash
streamlit run app.py
```

- Therapy Page: http://localhost:8501
- Meme Library: http://localhost:8501/meme_library

---

## ☁️ Deployment (Streamlit Community Cloud)

1. Push your repo to GitHub with these files/folders:

   - `app.py`
   - `pages/meme_library.py`
   - `requirements.txt`
   - `phobert_best/`, `emotion_memes.db`, `memes/`

2. Log in to [Streamlit Cloud](https://streamlit.io/cloud)

3. Create a new app:

   - Select your GitHub repo and branch (usually `main`)
   - Set `app.py` as the main file
   - Add `OPENROUTER_API_KEY` under Advanced Settings → Secrets

4. Deploy and visit your app URL

> ⚠️ Note: Feedback storage won't persist on the cloud due to the read-only file system. It works fully **only when run locally**.

---

## 🗂 Project Structure

```
mother-reaction-app/
├── app.py                # Main Therapy Page
├── pages/
│   └── meme_library.py   # Meme Library Page
├── phobert_best/         # PhoBERT model folder
├── emotion_memes.db      # SQLite DB (memes + feedback)
├── memes/                # Meme image folder
├── requirements.txt      # Python dependencies
├── .env                  # API key (not tracked)
├── .github/workflows/
│   └── ci.yml            # CI/CD pipeline (lint/test simulation)
└── README.md             # This file
```

---

## 🧠 Usage Guide

### 🪐 Therapy Page

1. Enter your thoughts in Vietnamese (e.g., "Tôi cảm thấy lạc lối trong đời").
2. Click **"Nhận lời khuyên"**.
3. See:
   - Emotion prediction (Vietnamese)
   - A 3-sentence cosmic response
   - A matching meme
4. Click:
   - 👍 **Thích** if satisfied
   - 👎 **Không thích** to provide feedback or correct the emotion

### 🖼 Meme Library Page

- Navigate to **Meme Library** via the sidebar
- View all memes sorted by emotion

---

## ⚙️ Tech Stack

| Layer    | Technology                         |
| -------- | ---------------------------------- |
| UI       | Streamlit (multi-page support)     |
| Emotion  | PhoBERT (via Hugging Face)         |
| Chat API | Quasar Alpha (via OpenRouter API)  |
| Storage  | SQLite (emotions, feedback, memes) |
| Env Mgmt | python-dotenv                      |
| DevOps   | GitHub Actions (CI/CD simulation)  |

---

## 🔁 CI/CD (Linting & Test Simulation)

Located in `.github/workflows/ci.yml`

- Runs `flake8` for code linting
- Simulates tests (real tests require local model and assets)

---

## 👤 Author

**Nguyễn Ngọc Thạch**  
MSSV: 2201700077  
UMT Machine Learning Project — Spring 2025

---

## 📝 License

**MIT License** — free to use, modify, and share.

---

## 📌 Notes

- Replace `yourusername` with your GitHub username in the repo URL
- SQLite DB feedback writes **only** when running locally
- Supports Streamlit’s new multi-page format (`pages/` folder)

---

## ✅ Next Steps

1. Save this file as `README.md` in your project root
2. Test locally:
   ```bash
   streamlit run app.py
   ```
3. Push to GitHub:
   ```bash
   git add README.md
   git commit -m "Add complete README for multi-page app"
   git push
   ```
4. Deploy on Streamlit Community Cloud as outlined above

---

Stay cosmic 🪐 and let JellyPearl guide your vibes 💫

```

Let me know if you'd like me to generate this as a downloadable file or local preview!
```
