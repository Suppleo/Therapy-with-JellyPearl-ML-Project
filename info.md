# Therapy with JellyPearl 🪐 - Project Summary

## App Info Summary

**Therapy with JellyPearl** is a multi-page web app built for a UMT Machine Learning project by Nguyễn Ngọc Thạch (MSSV: 2201700077). It connects users with JellyPearl, an interdimensional therapist, offering emotion-based advice in Vietnamese with dark/sexual humor (minimal cursing, no politics) and memes. The app uses AI to predict emotions, generate responses, and collect feedback, with a vision for MLCI/CD (Machine Learning Continuous Integration/Continuous Deployment) to retrain its model using user feedback.

- **Pages**:
  - **Therapy**: Users input thoughts, receive emotion predictions, advice, and memes, then rate with "Thích" (Like) or "Không thích" (Dislike) with optional emotion correction.
  - **Meme Library**: Displays all memes from the database, grouped by emotion.
- **Tech Stack**:
  - Frontend: Streamlit (multi-page)
  - ML: PhoBERT (Hugging Face Transformers, PyTorch)
  - NLP: Quasar Alpha (OpenRouter API)
  - DB: SQLite (local), planned Supabase (cloud)
  - Env: python-dotenv
- **Current Status**: Fully functional locally, preparing for cloud deployment with feedback persistence and MLCI/CD.

## Model

- **PhoBERT**: A Vietnamese BERT model fine-tuned on the UIT-VSMEC dataset for emotion classification (7 classes: Enjoyment, Sadness, Fear, Anger, Disgust, Surprise, Other).
  - Input: User text (e.g., "Tôi cảm thấy lạc lối trong đời").
  - Output: Predicted emotion (e.g., "Buồn bã").
  - Performance Goal: >70% accuracy/F1-score.
  - Stored in: `phobert_best/`.
- **Quasar Alpha**: Generates 3-sentence advice via OpenRouter API, prompted with JellyPearl’s quirky persona and the predicted emotion.
  - Goal: >50% positive user feedback.

## What’s Been Done

- **Day 1-5**: Initial setup, PhoBERT integration, Quasar Alpha advice generation, SQLite for memes, Streamlit UI with therapy functionality and meme display.
- **Day 6**: Added feedback feature (like/dislike, emotion correction) with SQLite storage, fixed UI issues (page refresh, button spacing), and tested end-to-end locally.
- **Pre-Day 7**: Restructured into a multi-page app with "Therapy" (`app.py`) and "Meme Library" (`pages/meme_library.py`), updated README, and planned deployment.

## Current Problems

1. **SQLite Write Limitation on Streamlit Cloud**:
   - **Issue**: Streamlit Community Cloud’s read-only filesystem prevents SQLite writes, so feedback doesn’t persist after deployment (works locally).
   - **Impact**: Users can submit feedback, but it fails silently or errors out in the cloud.
2. **MLCI/CD Retraining Not Implemented**:
   - **Issue**: No automated retraining pipeline exists yet to use feedback (e.g., 100 entries) to fine-tune PhoBERT.
   - **Impact**: Model remains static; feedback collects but isn’t leveraged for improvement.
3. **Deployment Readiness**:
   - **Issue**: Local SQLite and meme paths need adjustment for cloud compatibility (e.g., Supabase Storage URLs).
   - **Impact**: Current setup works locally but requires tweaks for full cloud functionality.

## Proposed Solutions

1. **SQLite Write Limitation**:
   - **Solution**: Switch to **Supabase** (PostgreSQL cloud DB):
     - Migrate `feedback` and `memes` tables to Supabase.
     - Use `supabase-py` for persistent writes and reads.
     - Store meme images in Supabase Storage, update paths to URLs.
   - **Alternative (Demo)**: Disable feedback writes in cloud with a notice (`if "STREAMLIT_CLOUD" in os.environ`), keeping SQLite read-only for memes.
2. **MLCI/CD Retraining**:
   - **Solution**: Implement with **GitHub Actions** and Supabase:
     - Monitor feedback count in Supabase (e.g., 100 entries).
     - Trigger a workflow to pull data, retrain PhoBERT (CPU on GitHub runners or external GPU), update `phobert_best/`, and push to repo.
     - Streamlit Cloud redeploys with the new model.
   - **Steps**: Add `retrain.py` script, update `.github/workflows/ci.yml` with scheduled or threshold-based runs.
   - **Challenge**: GitHub Actions lacks GPU; consider self-hosted runners or external services (e.g., Colab) for full retraining.
3. **Deployment Readiness**:
   - **Solution**: Deploy with Streamlit Cloud and Supabase:
     - Update `app.py` and `meme_library.py` for Supabase integration.
     - Push repo with `requirements.txt` (add `supabase`), `phobert_best/`, and secrets (`SUPABASE_URL`, `SUPABASE_KEY`, `OPENROUTER_API_KEY`).
     - Deploy via Streamlit Cloud dashboard, test URL.
   - **Timeline**: Day 7—polish, add CI/CD simulation, deploy.

## Next Steps

- Finalize Day 7:
  - Implement Supabase for feedback and memes.
  - Simulate MLCI/CD with GitHub Actions (basic feedback check).
  - Deploy on Streamlit Cloud with updated README.
- Test locally and in cloud, then celebrate a cosmic success! 🚀

**Author**: Nguyễn Ngọc Thạch - UMT Machine Learning Project (Spring 2025)
