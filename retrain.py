import os
import csv
from supabase import create_client
from dotenv import load_dotenv
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSequenceClassification, Trainer, TrainingArguments
from datasets import Dataset, concatenate_datasets, load_dataset

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

emotion_map = {'Enjoyment': 0, 'Sadness': 1, 'Fear': 2, 'Anger': 3,
               'Disgust': 4, 'Surprise': 5, 'Other': 6}

def fetch_feedback_data():
    response = supabase.table("feedback").select("*").execute()
    rows = response.data
    data = []
    for row in rows:
        corrected = row.get("corrected_emotion")
        if corrected:
            label = emotion_map.get(corrected, 6)  # default to 'Other'
            data.append({"Sentence": row["input_text"], "label": label})
    return data

def save_feedback_csv(data, filename="feedback_data.csv"):
    with open(filename, "w", encoding="utf-8", newline='') as f:
        writer = csv.DictWriter(f, fieldnames=["Sentence", "label"])
        writer.writeheader()
        writer.writerows(data)

def main():
    # Fetch feedback data with corrections
    feedback_data = fetch_feedback_data()
    print(f"Fetched {len(feedback_data)} corrected feedback samples.")

    # Save to CSV
    save_feedback_csv(feedback_data)

    # Load original dataset
    original = load_dataset('csv', data_files='train_dataset.csv')['train']

    # Load feedback dataset
    feedback = load_dataset('csv', data_files='feedback_data.csv')['train']

    # Combine datasets
    combined = concatenate_datasets([original, feedback])

    # Load tokenizer and model
    model_path = "./phobert_best"
    tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
    model = AutoModelForSequenceClassification.from_pretrained(model_path, local_files_only=True)

    def preprocess(batch):
        return tokenizer(batch["Sentence"], truncation=True, padding="max_length", max_length=128)

    tokenized = combined.map(preprocess, batched=True)

    # Training arguments
    training_args = TrainingArguments(
        output_dir="./phobert_best",
        overwrite_output_dir=True,
        num_train_epochs=1,
        per_device_train_batch_size=4,
        save_strategy="epoch",
        logging_steps=10,
        learning_rate=2e-5,
        report_to=[],
    )

    trainer = Trainer(
        model=model,
        args=training_args,
        train_dataset=tokenized,
        tokenizer=tokenizer,
    )

    # Train
    trainer.train()

    # Save updated model
    model.save_pretrained("./phobert_best")
    tokenizer.save_pretrained("./phobert_best")
    print("Retraining complete. Model saved to ./phobert_best")

if __name__ == "__main__":
    main()