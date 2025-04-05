# STEP 2: email-asistant.py (renamed from email-classifier.py)
# ✅ Merges summarisation + classification
# ✅ Only ONE GPT call per email
# ✅ Group summaries by category for cleaner output

import os
import json
import textwrap
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field
from collections import defaultdict

# ---------------------------------------------------------------------
# 🔐 Load OpenAI API Key from .env
# ---------------------------------------------------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------------------------------------------------
# 📅 Handle model selection
# ---------------------------------------------------------------------
parser = argparse.ArgumentParser(description="Run GPT email assistant.")
parser.add_argument("--model", default="gpt-3.5-turbo", help="Model to use (e.g., gpt-4o or gpt-3.5-turbo)")
args = parser.parse_args()
model = args.model

# ---------------------------------------------------------------------
# 📅 Load cleaned emails
# ---------------------------------------------------------------------
input_dir = "email-json-clean"
emails = []
for file in sorted(os.listdir(input_dir)):
    if file.endswith(".json"):
        with open(os.path.join(input_dir, file)) as f:
            emails.extend(json.load(f))

# ---------------------------------------------------------------------
# 📄 Set up output structure
# ---------------------------------------------------------------------
output_file = "email_summaries.txt"
category_buckets = defaultdict(list)

# ---------------------------------------------------------------------
# 🧠 Define summarisation prompt
# ---------------------------------------------------------------------
def summarise_email(subject, body):
    messages = [
        {
            "role": "system",
            "content": (
                "You are an assistant that processes and organises emails.\n\n"
                "For each email, return the following in this format:\n"
                "**Summary:** ...\n"
                "**Importance:** High/Medium/Low\n"
                "**Suggested Reply:** ...\n"
                "**Category:** Action Required / Technical/Project / Internal Announcement / Company FYI / Unclassified"
            )
        },
        {
            "role": "user",
            "content": f"Subject: {subject}\n\nBody: {body}"
        }
    ]

    response = client.chat.completions.create(
        model=model,
        messages=messages
    )

    return response.choices[0].message.content.strip()

# ---------------------------------------------------------------------
# 🔀 Process each email
# ---------------------------------------------------------------------
for email in emails:
    summary_block = summarise_email(email["subject"], email["body"])

    # Extract final category for sorting
    category_line = next((line for line in summary_block.splitlines() if line.startswith("**Category:**")), None)
    category = category_line.split("**Category:**")[-1].strip() if category_line else "Unclassified"

    full_output = (
        "==================================================================\n"
        f"📨 Email from: {email['from']}\n"
        f"📌 Subject: {email['subject']}\n"
        f"🏷️ Category: {category}\n\n"
        f"{textwrap.fill(summary_block, width=100)}\n\n"
        "==================================================================\n\n"
    )

    category_buckets[category].append(full_output)

# ---------------------------------------------------------------------
# 📂 Save grouped output
# ---------------------------------------------------------------------
with open(output_file, "w", encoding="utf-8", errors="replace") as f:
    f.write(f"MODEL USED: {model}\n\n")
    f.write("\ud83d\udcec Email Summary Report (Grouped by Category)\n\n")

    for cat in ["Action Required", "Technical/Project", "Internal Announcement", "Company FYI", "Unclassified"]:
        if category_buckets[cat]:
            f.write(f"\n--- {cat.upper()} ---\n\n")
            for block in category_buckets[cat]:
                f.write(block)

print(f"\n📂 All summaries saved to: {output_file}")