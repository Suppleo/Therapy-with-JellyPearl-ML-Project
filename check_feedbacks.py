import os
from supabase import create_client
from dotenv import load_dotenv
import subprocess

load_dotenv()

supabase_url = os.getenv("SUPABASE_URL")
supabase_key = os.getenv("SUPABASE_KEY")
supabase = create_client(supabase_url, supabase_key)

def main():
    # Count feedback rows
    response = supabase.table("feedback").select("id").execute()
    count = len(response.data)
    print(f"Feedback count: {count}")

    # Check if count is a multiple of 100
    # if count > 0 and count % 100 == 0:
    if count > 0 and count % 5 == 0:
        print("Threshold reached. Starting retraining...")
        # Call retrain.py
        subprocess.run(["python", "retrain.py"], check=True)
    else:
        print("Threshold not reached. Skipping retraining.")

if __name__ == "__main__":
    main()