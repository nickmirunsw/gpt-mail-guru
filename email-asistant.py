import os
import json
import textwrap
from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------
# 🔐 Load OpenAI API Key from .env
# ---------------------------------------------------------------------
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------------------------------------------------
# 📥 Load Emails from emails.json
# ---------------------------------------------------------------------
# Instead of one file, we now loop through all JSON files in 'output' folder
email_dir = "email-json-clean"
emails = []


for file in os.listdir(email_dir):
    if file.endswith(".json"):
        with open(os.path.join(email_dir, file)) as f:
            data = json.load(f)

            # If it's a list of emails
            if isinstance(data, list):
                emails.extend(data)
            # If it's a single email dict
            elif isinstance(data, dict):
                emails.append(data)



# ---------------------------------------------------------------------
# 📄 Set up output file (overwrite every run)
# ---------------------------------------------------------------------
# output_file = "email_summaries_gpt_4.txt"
output_file = "email_summaries_gpt_3.5.txt"
with open(output_file, "w") as f:
    f.write("📬 Email Summary Report\n\n")

# ---------------------------------------------------------------------
# 🧠 Define Pydantic Schema for Tool Output (Optional in v1)
# ---------------------------------------------------------------------
class SummaryResponse(BaseModel):
    summary: str = Field(description="A concise summary of the email's content")

# ---------------------------------------------------------------------
# 🛠️ Define GPT Tool Schema
# ---------------------------------------------------------------------
tools = [
    {
        "type": "function",
        "function": {
            "name": "summarise_email",
            "description": "Summarises the email content.",
            "parameters": {
                "type": "object",
                "properties": {
                    "subject": {"type": "string"},
                    "body": {"type": "string"}
                },
                "required": ["subject", "body"],
                "additionalProperties": False
            },
            "strict": True
        }
    }
]

# ---------------------------------------------------------------------
# 🔁 Loop through all emails and process them one by one
# ---------------------------------------------------------------------
for email in emails:
    subject = email["subject"]
    body = email["body"]

    # Step 1: Construct system + user messages
    messages = [
        {
            "role": "system",
            "content": "You are an assistant that summarises emails."
        },
        {
            "role": "user",
            "content": f"Please summarise this email:\nSubject: {subject}\nBody: {body}"
        }
    ]

    # Step 2: Ask GPT if it wants to use the summarise_email tool
    completion = client.chat.completions.create(
        # model="gpt-4o",
        model="gpt-3.5-turbo",
        messages=messages,
        tools=tools
    )

    # Step 3: Extract tool call + arguments
    tool_call = completion.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)

    # Step 4: Define your tool logic (calls GPT again to summarise)
    def summarise_email(subject, body):
        summary_messages = [
            {
                "role": "system",
                "content": (
                    "You are an assistant that processes emails.\n\n"
                    "For each email, the following is a must:\n"
                    "1. Summarise the email clearly and concisely.\n"
                    "2. Indicate the importance level: High, Medium, or Low.\n"
                    "3. Generate a short response to the sender. "
                    "This could be an acknowledgement or an answer to their question.\n\n"
                    "Format your response like this:\n"
                    "**Summary:** ...\n"
                    "**Importance:** High/Medium/Low\n"
                    "**Suggested Reply:** ...\n"
                )
            },
            {
                "role": "user",
                "content": f"Subject: {subject}\n\nBody: {body}"
            }
        ]

        response = client.chat.completions.create(
            # model="gpt-4o",
            model="gpt-3.5-turbo",
            messages=summary_messages
        )

        return {"summary": response.choices[0].message.content.strip()}

    # Step 5: Run your tool
    tool_result = summarise_email(**args)

    # Step 6: Update the message history with the tool call and response
    messages.append({
        "role": "assistant",
        "tool_calls": completion.choices[0].message.tool_calls
    })

    messages.append({
        "role": "tool",
        "tool_call_id": tool_call.id,
        "content": json.dumps(tool_result)
    })

    # Step 7: Ask GPT for the final user-facing message
    completion_2 = client.chat.completions.create(
        # model="gpt-4o",
        model="gpt-3.5-turbo",
        messages=messages
    )

    final_response = completion_2.choices[0].message.content.strip()

    # Step 8: Save formatted result to output file
    with open(output_file, "a") as f:
        f.write("==================================================================\n")
        f.write(f"📨 Email from: {email['from']}\n")
        f.write(f"📌 Subject: {subject}\n\n")

        for i, choice in enumerate(completion_2.choices):
            # f.write(f"✏️ Option {i + 1}:\n")
            wrapped = textwrap.fill(choice.message.content.strip(), width=100)
            f.write(wrapped + "\n\n")

        f.write("==================================================================\n\n")

# ---------------------------------------------------------------------
# ✅ Done
# ---------------------------------------------------------------------
print(f"✅ All email summaries saved to: {output_file}")
