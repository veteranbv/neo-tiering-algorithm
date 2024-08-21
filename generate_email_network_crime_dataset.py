from faker import Faker
import random
import datetime
import csv

fake = Faker()

def generate_email_record(sender, recipient, subject, label, timestamp, content=None, tier=None):
    return {
        "email_id": fake.uuid4(),
        "date": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "sender": sender,
        "recipient": recipient,
        "subject": subject,
        "label": label,
        "content": content if content else fake.paragraph(),
        "tier": tier
    }

def generate_dataset(num_records=5000):
    dataset = []
    john_email = "john.doe@personal.com"

    # Criminal network
    criminal_contacts = [fake.email() for _ in range(5)]  # Core criminal group
    criminal_fronts = [fake.company_email() for _ in range(3)]  # Company fronts
    mules = [fake.email() for _ in range(10)]  # Money mules

    # Other contacts
    family = [fake.email() for _ in range(3)]
    friends = [fake.email() for _ in range(10)]
    work_contacts = [fake.company_email() for _ in range(20)]

    # Tier 3 - Unresponded Received Emails (60% of total)
    for _ in range(int(num_records * 0.6)):
        sender = random.choice([fake.email()] * 8 + criminal_contacts + criminal_fronts + mules)
        subject = fake.sentence(nb_words=6)
        label = random.choice(["Spam", "Newsletter", "Notification", "Admin"])
        if sender in criminal_contacts + criminal_fronts + mules:
            label = "Suspicious"
        timestamp = fake.date_time_this_year()
        content = fake.paragraph()
        dataset.append(generate_email_record(sender, john_email, subject, label, timestamp, content, tier=3))

    # Tier 2 - Sent with No Response (30% of total)
    for _ in range(int(num_records * 0.3)):
        recipient = random.choice([fake.email()] * 8 + criminal_contacts + criminal_fronts + mules)
        subject = random.choice([
            f"Job Application - {fake.job()}",
            f"Inquiry Regarding {fake.word().capitalize()}",
            f"Invitation to {fake.company()} Meeting",
            f"Question about {fake.bs()}"
        ])
        label = "Sent"
        if recipient in criminal_contacts + criminal_fronts + mules:
            label = "Suspicious Sent"
            subject = random.choice([
                f"Re: {fake.word().capitalize()} Operation",
                f"Update on {fake.city()}",
                f"New {fake.word().capitalize()} Shipment",
                f"Meeting at {fake.street_name()}",
                f"Code: {fake.random_number(digits=6)}"
            ])
        timestamp = fake.date_time_this_year()
        content = fake.paragraph()
        dataset.append(generate_email_record(john_email, recipient, subject, label, timestamp, content, tier=2))

    # Tier 1 - Mutual Communication (10% of total)
    tier1_contacts = criminal_contacts + criminal_fronts + mules + family + friends + random.sample(work_contacts, 5)
    for _ in range(int(num_records * 0.1)):
        contact = random.choice(tier1_contacts)
        is_criminal = contact in criminal_contacts + criminal_fronts + mules
        
        for i in range(random.randint(2, 5)):  # 2-5 exchanges per conversation
            if i % 2 == 0:
                sender, recipient = john_email, contact
            else:
                sender, recipient = contact, john_email

            if is_criminal:
                subject, content, label = generate_criminal_content(contact, criminal_contacts, criminal_fronts, mules)
            else:
                subject = fake.sentence(nb_words=6)
                content = fake.paragraph()
                label = random.choice(["Family", "Friend", "Colleague", "Personal"])

            timestamp = fake.date_time_this_year() + datetime.timedelta(hours=i)
            dataset.append(generate_email_record(sender, recipient, subject, label, timestamp, content, tier=1))

    random.shuffle(dataset)  # Randomize the order
    return dataset

def generate_criminal_content(contact, criminal_contacts, criminal_fronts, mules):
    if contact in criminal_contacts:
        subject = random.choice([
            f"Re: {fake.word().capitalize()} Operation",
            f"Update on {fake.city()}",
            f"New {fake.word().capitalize()} Shipment",
            f"Meeting at {fake.street_name()}",
            f"Code: {fake.random_number(digits=6)}"
        ])
        content = random.choice([
            f"The package will arrive at {fake.street_address()} on {fake.date_this_month()}. Confirmation code: {fake.random_number(digits=8)}",
            f"Transfer {fake.random_number(digits=6)} to account {fake.iban()}. Use reference: {fake.word().upper()}",
            f"New target acquired. Details: {fake.name()}, {fake.job()}, {fake.address()}",
            f"Change of plans. Meet at {fake.street_name()} instead. Time: {fake.time()}",
            f"Shipment intercepted. Initiate protocol {fake.random_letter().upper()}{fake.random_number(digits=2)}"
        ])
        label = "Criminal"
    elif contact in criminal_fronts:
        subject = random.choice([
            f"Invoice #{fake.random_number(digits=6)}",
            f"Shipment #{fake.random_number(digits=8)} Status",
            f"Contract Renewal for {fake.company()}",
            f"Quarterly Report - {fake.month()} {fake.year()}",
            f"New Client Onboarding - {fake.company()}"
        ])
        content = random.choice([
            f"Please find attached the invoice for services rendered in {fake.month()}. Total amount: ${fake.random_number(digits=6)}",
            f"Shipment #{fake.random_number(digits=8)} has cleared customs and is en route to the warehouse.",
            f"As per our discussion, we've prepared the new contract for {fake.company()}. Please review and sign.",
            f"Q{random.randint(1,4)} report attached. Note the increased activity in sector {fake.random_letter().upper()}.",
            f"New client {fake.company()} has been added to our portfolio. Expected annual revenue: ${fake.random_number(digits=7)}"
        ])
        label = "Front"
    else:  # mules
        subject = random.choice([
            "Quick Favor Needed",
            "Urgent: Account Transfer",
            "Package Pickup Request",
            "New Task Assignment",
            "Confirmation Needed"
        ])
        content = random.choice([
            f"Please transfer ${fake.random_number(digits=5)} to account {fake.iban()}. Use reference: {fake.word().upper()}",
            f"Pick up package from {fake.street_address()} and deliver to {fake.street_address()}. Use code: {fake.random_number(digits=6)}",
            f"New account details: Bank: {fake.company()}, Account: {fake.random_number(digits=10)}, Name: {fake.name()}",
            f"Confirm receipt of ${fake.random_number(digits=5)} in your account. Transfer to provided accounts immediately.",
            f"Your new task: Monitor account {fake.iban()} for incoming transfer of ${fake.random_number(digits=6)}. Report when received."
        ])
        label = "Mule"
    return subject, content, label

if __name__ == "__main__":
    email_data = generate_dataset(5000)

    # Save to CSV
    with open('enhanced_tiered_email_dataset.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['email_id', 'date', 'sender', 'recipient', 'subject', 'label', 'content', 'tier']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(email_data)

    print("Dataset generated and saved to 'enhanced_tiered_email_dataset.csv'")