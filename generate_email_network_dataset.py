import csv
import random
from datetime import datetime, timedelta
from faker import Faker
import os
import uuid

# Initialize Faker
faker = Faker()

# Define possible labels
labels = ["Work", "Personal", "Spam"]

# Function to generate a random email subject
def generate_subject(label):
    subject_dict = {
        "Work": [
            "Project Update - {}".format(faker.company()),
            "Meeting Request: {}".format(faker.sentence(nb_words=4)),
            "Task Status: {}".format(faker.job()),
            "Client Feedback: {}".format(faker.company())
        ],
        "Personal": [
            "Weekend plans?",
            "Catching up",
            "How are you?",
            "{}: {}".format(faker.sentence(nb_words=2), faker.sentence(nb_words=4))
        ],
        "Spam": [
            "Exclusive Offer: {}".format(faker.catch_phrase()),
            "Limited Time Deal: {}".format(faker.bs()),
            "Win a Prize: {}".format(faker.company()),
            "Free Gift: {}".format(faker.word())
        ]
    }
    return random.choice(subject_dict[label])

# Generate email lists for each category
email_lists = {label: [faker.email() for _ in range(100)] for label in labels}

# Function to determine sender and recipient based on desired distribution and category
def determine_sender_and_recipient(label):
    distribution = {
        "Work": [0.3, 0.7],  # 30% John Doe, 70% others
        "Personal": [0.5, 0.5],  # 50% John Doe, 50% others
        "Spam": [0, 1]  # 0% John Doe, 100% others
    }
    sender_choice = random.choices(["John Doe", "Other"], weights=distribution[label])[0]
    sender = "john.doe@personal.com" if sender_choice == "John Doe" else random.choice(email_lists[label])
    recipient = "john.doe@personal.com" if sender_choice == "Other" else random.choice(email_lists[label])
    return sender, recipient

# Generate email data with controlled distribution and email lists
emails = []
for _ in range(1000):
    email_id = str(uuid.uuid4())  # Generate a unique UUID for each email
    date = datetime.today() - timedelta(days=random.randint(0, 30))
    label = random.choice(labels)
    sender, recipient = determine_sender_and_recipient(label)
    subject = generate_subject(label)
    emails.append({
        "email": email_id,
        "date": date.strftime("%Y-%m-%d %H:%M:%S"),
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "labels": label
    })

# Create directory if it doesn't exist
directory = "data"
if not os.path.exists(directory):
    os.makedirs(directory)

# Write data to CSV file
csv_file = os.path.join(directory, "john_doe_emails_network.csv")
with open(csv_file, "w", newline="") as csvfile:
    fieldnames = ["email", "date", "sender", "recipient", "subject", "labels"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(emails)

print("CSV file generated successfully!")
