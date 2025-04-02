import subprocess

# Step 1: Run the email cleaner
print("🧼 Cleaning emails...")
cleaner_result = subprocess.run(["python3", "batch-email-cleaner.py"], capture_output=True, text=True)
print(cleaner_result.stdout)
if cleaner_result.stderr:
    print("❗ Email Cleaner Errors:")
    print(cleaner_result.stderr)

# Step 2: Run the email summariser
print("\n🤖 Summarising emails...")
summary_result = subprocess.run(["python3", "email-asistant.py"], capture_output=True, text=True)
print(summary_result.stdout)
if summary_result.stderr:
    print("❗ Email Assistant Errors:")
    print(summary_result.stderr)

print("\n✅ Workflow complete!")
