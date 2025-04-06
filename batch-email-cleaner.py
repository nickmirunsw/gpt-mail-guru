import json
import re
import os
from bs4 import BeautifulSoup

# Ensure output directory exists
os.makedirs("email-json-clean", exist_ok=True)

# Recursively walk through all subfolders under 'email-json-outlook-raw'
email_files = []
for root, _, files in os.walk("email-json-outlook-raw"):
    for file in files:
        if file.endswith(".json"):
            email_files.append(os.path.join(root, file))

# Sort files for consistency
email_files = sorted(email_files)

for idx, file_path in enumerate(email_files, start=1):
    with open(file_path, "r", encoding="utf-8") as file:
        try:
            raw_data = json.load(file)
            inputs = raw_data.get("inputs", {})
        except Exception as e:
            print(f"⚠️ Skipping {file_path}: {e}")
            continue

    email_from = inputs.get("from", "")
    subject = inputs.get("subject", "")
    html_body = inputs.get("body", "")

    # Clean HTML -> plain text
    soup = BeautifulSoup(html_body, "html.parser")
    text_body = soup.get_text(separator="\n", strip=True)
    clean_body = re.sub(r"\n+", "\n", text_body).strip()

    # Create output structure
    email_id = str(idx).zfill(3)
    email_obj = [{
        "id": email_id,
        "from": email_from,
        "subject": subject,
        "body": clean_body
    }]

    # Save to file
    output_filename = f"email-json-clean/{email_id}.json"
    with open(output_filename, "w", encoding="utf-8") as outfile:
        json.dump(email_obj, outfile, indent=2, ensure_ascii=False)

    print(f"✅ Saved: {output_filename}")

print("\n🎉 All emails processed")


