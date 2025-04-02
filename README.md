# gpt-mail-guru

Automated email summariser pipeline: Cleans and parses Outlook-exported emails, then uses GPT to generate summaries, importance levels, and suggested replies. Ideal for Power Automate workflows.

---

## 📦 Features

- Parses `.json` emails exported from Outlook via Power Automate
- Cleans HTML bodies and extracts readable text
- Uses GPT-3.5-turbo to:
  - Summarise each email
  - Assess importance (High / Medium / Low)
  - Generate a suggested reply
- Outputs all results into a single clean `.txt` file

---

## 🧰 Requirements

- Python 3.8+
- OpenAI Python SDK
- `python-dotenv`
- `beautifulsoup4`

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## 🔐 Setup

Create a `.env` file in the root directory:

```
OPENAI_API_KEY=your_openai_key_here
```

---

## 📁 Folder Structure

```
bots/
├── process-emails.py           # Parses raw JSON emails into a structured format
├── email-assistant.py          # Uses GPT to generate summaries and replies
├── run-all.py                  # Optional: runs both scripts in sequence
├── output/
│   └── Email_*.json            # Raw exported emails (from Power Automate)
├── emails.json                 # Combined clean list used as input to GPT
├── email_summaries_gpt_3.5.txt # Final output file with summaries
```

---

## 🚀 Usage

1. Export your emails as individual `.json` files using Power Automate
2. Drop them into the `output/` folder
3. Run the full pipeline:

```bash
python process-emails.py
python email-assistant.py
```

Alternatively, to run both:

```bash
python run-all.py
```

---

## 📤 Power Automate Format

Each `.json` email file should contain this structure:

```json
{
  "from": "someone@example.com",
  "subject": "Your subject",
  "body": "<html>...full email content...</html>"
}
```

---

## ✅ Output Example

```
==================================================================
📨 Email from: jane.doe@company.com
📌 Subject: Project Status Update

✏️ Option 1:
**Summary:** Jane provided a status update on the infrastructure project. Things are on track, with minor delays due to external vendor issues.

**Importance:** Medium  
**Suggested Reply:** Thanks for the update. Please let us know if the vendor causes any further delays.

==================================================================
```

---

## 🧠 Model Details

- Model: `gpt-3.5-turbo`
- Tool mode: Function calling
- Output format: Summary + Importance + Suggested Reply

---

## 🛠️ Future Improvements

- Add threading support
- Option to group emails by sender or subject
- Switch to GPT-4 for higher-quality summaries

---

## 📄 License

MIT License
