# Therapy with JellyPearl 🪐

A quirky multi-page web app where users receive cosmic therapy from JellyPearl, an interdimensional therapist, or browse a meme library.  
Powered by **PhoBERT** for emotion prediction, **Quasar Alpha** for witty advice, and **Supabase** for feedback and meme storage.

---

## 🌟 Features

- **Therapy Page**:  
  Share your thoughts in Vietnamese → Predict emotion with PhoBERT → Get 3-sentence advice from JellyPearl with dark/sexual humor → See a matching meme.  
  Rate the advice (👍 Thích / 👎 Không thích) and correct the emotion if necessary.

- **Meme Library**:  
  Browse all stored memes by emotion.

- **Feedback System**:  
  Likes, dislikes, and corrections are saved to **Supabase** for future model improvements.

- **Automated Retraining Pipeline**:  
  GitHub Actions automatically retrains PhoBERT on new feedback every 100 entries, updates the model, and redeploys the app.

---

## 🚀 Setup

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/mother-reaction-app.git
cd mother-reaction-app
```

### 2. Install Dependencies

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
```

### 3. Add Environment Variables

Create a `.env` file:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
OPENROUTER_API_KEY=your_openrouter_api_key
```

### 4. Prepare Required Assets

- `phobert_best/` folder with PhoBERT model files (downloaded & cached for offline use)
- `memes/` folder with meme images
- `train_dataset.csv` — your original training data (Sentence,label)

### 5. Run Locally

```bash
streamlit run app.py
```

- Therapy Page: http://localhost:8501
- Meme Library: http://localhost:8501/meme_library

---

## ☁️ Deployment (Streamlit Community Cloud)

1. Push your repo to GitHub **including**:

   - `app.py`
   - `pages/`
   - `requirements.txt`
   - `phobert_best/` (tracked with Git LFS)
   - `memes/`
   - `.github/workflows/retrain.yml`
   - `train_dataset.csv`

2. On [Streamlit Cloud](https://streamlit.io/cloud):

   - Create a new app linked to your repo.
   - Set `app.py` as the main file.
   - Add secrets: `SUPABASE_URL`, `SUPABASE_KEY`, `OPENROUTER_API_KEY`.

3. Deploy and test!

---

## 🔁 Automated MLCI/CD Pipeline

- **Location:** `.github/workflows/retrain.yml`
- **Runs:** Daily (cron) or manually
- **Process:**
  - Checks Supabase feedback count.
  - If count hits 100, 200, 300, ...:
    - Downloads feedback data.
    - Combines with original data (`train_dataset.csv`).
    - Fine-tunes PhoBERT on CPU.
    - Saves updated model to `phobert_best/`.
    - Commits and pushes model back to repo.
    - Triggers Streamlit Cloud redeploy.

---

## 🗂 Project Structure

```
mother-reaction-app/
├── app.py
├── check_feedbacks.py
├── retrain.py
├── train_dataset.csv
├── phobert_best/           # PhoBERT model files (offline)
├── memes/                  # Meme images
├── pages/
│   └── 1_meme_library.py
├── requirements.txt
├── .env
├── .github/
│   └── workflows/
│       └── retrain.yml
└── README.md
```

---

## ⚙️ Tech Stack

| Layer      | Technology                           |
| ---------- | ------------------------------------ |
| UI         | Streamlit (multi-page)               |
| Emotion    | PhoBERT (offline, Hugging Face)      |
| Chat API   | Quasar Alpha (OpenRouter API)        |
| Storage    | Supabase (Postgres + Storage)        |
| Automation | GitHub Actions (retraining pipeline) |
| Env Mgmt   | python-dotenv                        |

---

## 📝 Notes

- The app **works offline** with the bundled PhoBERT model.
- Feedback is **stored in Supabase** (cloud database).
- The model **retrain pipeline** is **free but slow** (CPU-only).
- You can **disable daily retraining** by commenting out the `schedule` block in `.github/workflows/retrain.yml`.
- You can **trigger retraining manually** from GitHub Actions tab.

---

## 👤 Author

**Nguyễn Ngọc Thạch**  
UMT Machine Learning Project — Spring 2025  
MSSV: 2201700077

---

## 📄 License

MIT License — free to use, modify, and share.

---

Stay cosmic 🪐 and let JellyPearl guide your vibes! 🚀
