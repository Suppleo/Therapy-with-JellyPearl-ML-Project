import streamlit as st
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
from openai import OpenAI
import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# Initialize Supabase client
supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

# Load PhoBERT
model_path = 'Suppleo/phobert-finetuned-jellypearl'
try:
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForSequenceClassification.from_pretrained(model_path)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model.to(device)
except Exception as e:
    st.error(f"Lỗi khi tải mô hình: {e}")
    raise

# OpenRouter client
api_key = os.getenv("OPENROUTER_API_KEY")
if not api_key:
    st.error("Thiếu OPENROUTER_API_KEY trong .env!")
    st.stop()
client = OpenAI(base_url="https://openrouter.ai/api/v1", api_key=api_key)

emotion_map_internal = {
    0: "Enjoyment", 1: "Sadness", 2: "Fear", 3: "Anger", 4: "Disgust", 5: "Surprise", 6: "Other"
}

emotion_map_display = {
    "Enjoyment": "Vui vẻ", "Sadness": "Buồn bã", "Fear": "Sợ hãi", "Anger": "Tức giận",
    "Disgust": "Ghê tởm", "Surprise": "Ngạc nhiên", "Other": "Bình thường"
}

# Reverse mapping for saving corrected emotion in English
display_to_english = {v: k for k, v in emotion_map_display.items()}

def predict_generate_and_get_meme(input_text):
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True, max_length=128)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
        pred = torch.argmax(outputs.logits, dim=-1).item()
    emotion_internal = emotion_map_internal[pred]
    emotion_display = emotion_map_display[emotion_internal]

    system_prompt = (
        "You are JellyPearl, an interdimensional therapist with a quirky, cosmic vibe and a taste for dark and sexual humor. "
        "Provide fun, insightful life advice in Vietnamese based on the user's predicted emotion, in exactly 3 sentences. "
        "Keep cursing rare, avoid politics, and make it witty and uplifting, even when diving into the absurd or naughty."
    )
    user_prompt = (
        f"React to '{input_text}' with the predicted emotion {emotion_display} as JellyPearl. "
        "Offer life advice in Vietnamese with a dark or sexual twist, minimal cursing, in 3 sentences. "
        "Make it fun and insightful to guide me!"
    )
    try:
        response = client.chat.completions.create(
            model="openrouter/quasar-alpha",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            max_tokens=300,
            temperature=0.9,
        )
        response_text = response.choices[0].message.content.strip()
    except Exception as e:
        st.error(f"Lỗi khi gọi Quasar Alpha: {e}")
        response_text = "JellyPearl tạm thời mất kết nối vũ trụ, thử lại nhé!"

    try:
        response = supabase.table("memes").select("meme_url").eq("emotion", emotion_internal).execute()
        memes = response.data
        meme_url = memes[0]['meme_url'] if memes else None
    except Exception as e:
        st.error(f"Lỗi khi lấy meme từ Supabase: {e}")
        meme_url = None

    return emotion_display, response_text, meme_url

def store_feedback(input_text, predicted_emotion, rating, corrected_emotion=None):
    try:
        corrected_eng = None
        if corrected_emotion:
            corrected_eng = display_to_english.get(corrected_emotion, corrected_emotion)
        data = {
            "input_text": input_text,
            "predicted_emotion": predicted_emotion,
            "rating": rating,
            "corrected_emotion": corrected_eng
        }
        supabase.table("feedback").insert(data).execute()
        return True
    except Exception as e:
        st.error(f"Lỗi khi lưu phản hồi lên Supabase: {e}")
        return False

# --- Session State ---
st.session_state.setdefault('result', None)
st.session_state.setdefault('feedback_submitted', False)
st.session_state.setdefault('feedback_type', None)
st.session_state.setdefault('show_dislike_form', False)
st.session_state.setdefault('corrected_emotion', "")

# --- UI ---
st.title("Trị liệu với JellyPearl 🪐")
st.markdown("""
Bạn đã lạc vào một khe nứt giữa các chiều không gian, đến với văn phòng kỳ ảo của JellyPearl, một nhà trị liệu lấp lánh từ vũ trụ khác.  
Tại đây, JellyPearl nhìn thấu tâm hồn bạn qua từng lời nói, đưa ra lời khuyên đầy hài hước đen tối và chút nghịch ngợm, nhưng luôn ấm áp và sâu sắc.  
Hãy chia sẻ suy nghĩ của bạn, và để JellyPearl dẫn dắt bạn qua những mê cung cảm xúc với nụ cười từ cõi hư không!
""")

st.write("### Nhập suy nghĩ của bạn để nhận lời khuyên từ JellyPearl!")
user_input = st.text_input("Suy nghĩ của bạn:", "Tôi cảm thấy lạc lối trong đời")

if st.button("Nhận lời khuyên"):
    if user_input.strip():
        with st.spinner("JellyPearl đang phân tích tâm hồn bạn..."):
            emotion, response, meme_url = predict_generate_and_get_meme(user_input)
            st.session_state.result = (emotion, response, meme_url)
            st.session_state.feedback_submitted = False
            st.session_state.feedback_type = None
            st.session_state.show_dislike_form = False
            st.session_state.corrected_emotion = ""
    else:
        st.error("Hãy nhập gì đó đi, JellyPearl không đọc được ý nghĩ đâu!")

# --- Show result ---
if st.session_state.result:
    emotion, response, meme_url = st.session_state.result
    st.subheader("Kết quả:")
    st.write(f"**Cảm xúc của bạn:** {emotion}")
    st.write(f"**Lời khuyên từ JellyPearl:** {response}")
    if meme_url:
        st.image(meme_url, caption=f"Meme dành cho bạn hôm nay (Cảm xúc {emotion})", use_container_width=True)
    else:
        st.write("Không có meme nào phù hợp.")

    # --- Feedback Buttons ---
    st.subheader("Đánh giá của bạn")
    if not st.session_state.feedback_submitted:
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Thích", key="like_btn"):
                if store_feedback(user_input, emotion, "like"):
                    st.session_state.feedback_submitted = True
                    st.session_state.feedback_type = "like"
        with col2:
            if st.button("Không thích", key="dislike_btn"):
                st.session_state.show_dislike_form = True

    # --- Show dislike form if triggered ---
    if st.session_state.show_dislike_form and not st.session_state.feedback_submitted:
        with st.form("dislike_form"):
            st.selectbox(
                "Cảm xúc đúng của bạn là gì?",
                [""] + list(emotion_map_display.values()),
                key="corrected_emotion"
            )
            if st.form_submit_button("Gửi phản hồi không thích"):
                corrected = st.session_state.corrected_emotion
                if store_feedback(user_input, emotion, "dislike", corrected if corrected else None):
                    st.session_state.feedback_submitted = True
                    st.session_state.feedback_type = "dislike"

    # --- Feedback result ---
    elif st.session_state.feedback_submitted:
        if st.session_state.feedback_type == "like":
            st.success("Cảm ơn bạn đã thích lời khuyên của JellyPearl!")
        elif st.session_state.feedback_type == "dislike":
            st.success("Cảm ơn bạn đã gửi phản hồi" + (" và sửa cảm xúc!" if st.session_state.corrected_emotion else "!"))

st.write("Made with ❤️ by Ngoc Thach - UMT Machine Learning Project")