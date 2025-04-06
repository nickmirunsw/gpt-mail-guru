import subprocess

# ✏️ Choose the model once
# model_choice = "gpt-4o"  # Or switch to "gpt-3.5-turbo" to save cost
model_choice = "gpt-3.5-turbo"

# Step 1: Clean raw Outlook-exported emails
print("🧼 Cleaning emails...")
cleaner_result = subprocess.run(["python3", "batch-email-cleaner.py"], capture_output=True, text=True)
print(cleaner_result.stdout)
if cleaner_result.stderr:
    print("❗ Email Cleaner Errors:")
    print(cleaner_result.stderr)

# Step 2: Classify & Summarise in one step
print(f"\n🤖 Classifying & Summarising emails with model: {model_choice}")
assistant_result = subprocess.run(
    ["python3", "email-asistant.py", "--model", model_choice],
    capture_output=True,
    text=True
)
print(assistant_result.stdout)
if assistant_result.stderr:
    print("❗ Email Assistant Errors:")
    print(assistant_result.stderr)

# ✅ NEW Step 3: Generate To-Do List from Summaries
print(f"\n📝 Generating professional to-do list with model: {model_choice}")
todo_result = subprocess.run(
    ["python3", "email-todo-generator.py", "--model", model_choice],
    capture_output=True,
    text=True
)
print(todo_result.stdout)
if todo_result.stderr:
    print("❗ To-Do List Generator Errors:")
    print(todo_result.stderr)

print("\n✅ Workflow complete!")
