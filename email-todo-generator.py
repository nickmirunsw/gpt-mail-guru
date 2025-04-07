import os
import argparse
from dotenv import load_dotenv
import openai

# ---------------------------------------------------------------------
# 🔐 Load OpenAI API Key from .env
# ---------------------------------------------------------------------
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ---------------------------------------------------------------------
# Handle model selection
# ---------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Generate a professional to-do list from email summaries.")
parser.add_argument("--model", default="gpt-3.5-turbo", help="Model to use (e.g., gpt-4o or gpt-3.5-turbo)")
args = parser.parse_args()
model = args.model

# ---------------------------------------------------------------------
# Load the summary text
# ---------------------------------------------------------------------
summary_file = "C:/Users/AUNM510822/Desktop/email_summaries.txt"
with open(summary_file, "r", encoding="utf-8") as f:
    summaries = f.read()

# ---------------------------------------------------------------------
# Send to GPT for To-Do list generation
# ---------------------------------------------------------------------
messages = [
    {
        "role": "system",
        "content": (
            "You are a professional assistant that reads through email summaries and generates a clean, "
            "structured, and actionable to-do list. Prioritise clarity, conciseness, and group similar items."
        )
    },
    {
        "role": "user",
        "content": f"Here are the email summaries:\n\n{summaries}\n\nGenerate the to-do list."
    }
]

response = openai.ChatCompletion.create(
    model=model,
    messages=messages
)

todo_list = response["choices"][0]["message"]["content"].strip()

# ---------------------------------------------------------------------
# Save the output
# ---------------------------------------------------------------------
outfile = "C:/Users/AUNM510822/Desktop/email_todo_list.txt"
with open(outfile, "w", encoding="utf-8") as f:
    f.write(f"MODEL USED: {model}\n\n")
    f.write("Professional To-Do List\n\n")
    f.write(todo_list)

print(f"\n To-do list saved to: {outfile}")
