
import imaplib
import email
import re
from email.header import decode_header
from urllib.parse import urlparse
from getpass import getpass
imap_server = "imap.world4you.com"
urgent_words = [
    "urgent",
    "act immediately",
    "account blocked",
    "account suspended",
    "immediate action",
    "within 24 hours",
    "limited time"
]

sensitive_words = [
    "enter your password",
    "share your otp",
    "bank details",
    "credit card number",
    "verify your password",
    "send your pin"
]

suspicious_words = [
    "you won a prize",
    "claim your reward",
    "free money",
    "verify your account",
    "click here"
]

trusted_domains = [
    "google.com",
    "microsoft.com",
    "amazon.com"
]

def decode_text(value):

    if not value:
        return "Not Available"

    decoded_parts = decode_header(value)
    result = ""

    for part, encoding in decoded_parts:

        if isinstance(part, bytes):
            result += part.decode(
                encoding or "utf-8",
                errors="replace"
            )
        else:
            result += part

    return result

def get_email_content(message):

    content = ""

    if message.is_multipart():

        for part in message.walk():

            if part.get_content_type() == "text/plain":

                if part.get_content_disposition() != "attachment":

                    try:
                        content += part.get_content()
                    except Exception:
                        pass

    else:

        try:
            if message.get_content_type() == "text/plain":
                content = message.get_content()
        except Exception:
            pass

    return content

def scan_email(content):

    score = 0
    warnings = []

    text = content.lower()

    # Check urgent requests
    for word in urgent_words:

        if word in text:
            warnings.append(
                "Urgent request detected: " + word
            )
            score += 2
    for word in sensitive_words:

        if word in text:
            warnings.append(
                "Sensitive information request: " + word
            )
            score += 3
    for word in suspicious_words:

        if word in text:
            warnings.append(
                "Suspicious phrase detected: " + word
            )
            score += 2


    urls = re.findall(
        r'https?://[^\s<>"\']+',
        content,
        re.IGNORECASE
    )

    for url in urls:

        domain = urlparse(url.rstrip(".,;!?)")).hostname

        if domain:

            domain = domain.lower()

            trusted = any(
                domain == item or
                domain.endswith("." + item)
                for item in trusted_domains
            )

            if not trusted:

                warnings.append(
                    "Unknown link detected: " + url
                )
                score += 3

    return score, warnings

def display_email(message, number):

    sender = decode_text(message.get("From"))
    receiver = decode_text(message.get("To"))
    bcc = decode_text(message.get("Bcc"))
    subject = decode_text(message.get("Subject"))
    date = message.get("Date", "Not Available")

    content = get_email_content(message)

    print("\n" + "=" * 50)

    print("Message Number:", number)
    print("From:", sender)
    print("To:", receiver)
    print("BCC:", bcc)
    print("Date:", date)
    print("Subject:", subject)

    print("\nContent:")
    print(content)
    score, warnings = scan_email(content)

    print("\n========== EMAIL RISK ANALYSIS ==========")

    if score >= 5:
        print("STATUS: HIGH RISK - Potentially Unsafe Email")

    elif score >= 2:
        print("STATUS: SUSPICIOUS EMAIL")

    else:
        print("STATUS: LOW RISK - No Major Issues Detected")

    print("Risk Score:", score)

    if warnings:

        print("\nDetected Threats:")

        for warning in warnings:
            print("-", warning)

    else:
        print("\nNo suspicious patterns detected.")

    print("=" * 50)

def sample_mode():

    sample_email = """
    Hello Customer,

    Your account will be blocked within 24 hours.

    Act immediately!

    Click here to verify your account:
    http://unknown-example.com/login

    Enter your password and share your OTP.

    Thank you.
    """

    print("\nEMAIL RISK ANALYZER - SAMPLE MODE")

    print("\nContent:")
    print(sample_email)

    score, warnings = scan_email(sample_email)

    print("\n========== EMAIL RISK ANALYSIS ==========")

    if score >= 5:
        print("STATUS: HIGH RISK - Potentially Unsafe Email")

    elif score >= 2:
        print("STATUS: SUSPICIOUS EMAIL")

    else:
        print("STATUS: LOW RISK - No Major Issues Detected")

    print("Risk Score:", score)

    print("\nDetected Threats:")

    for warning in warnings:
        print("-", warning)

    print("=" * 50)

def imap_mode():

    email_address = input("\nEnter email address: ")
    password = getpass("Enter email password/app password: ")

    imap = None

    try:

        print("\nConnecting to email server...")

        imap = imaplib.IMAP4_SSL(imap_server)

        imap.login(email_address, password)

        print("Login successful!")

        status, data = imap.select("INBOX", readonly=True)

        if status != "OK":
            raise Exception("Could not open INBOX")

        status, messages = imap.search(None, "ALL")

        if status != "OK":
            raise Exception("Could not retrieve emails")

        email_ids = messages[0].split()

        print("\nTotal Emails Found:", len(email_ids))

        if not email_ids:
            print("No emails found.")
            return
        for number, email_id in enumerate(email_ids[-10:], start=1):

            status, data = imap.fetch(email_id, "(RFC822)")

            if status != "OK":
                print("Could not fetch email:", email_id)
                continue

            raw_email = next(
                (item[1] for item in data if isinstance(item, tuple)),
                None
            )

            if raw_email is None:
                continue

            message = email.message_from_bytes(raw_email)

            display_email(message, number)

        print("\nEmail scanning completed!")

    except imaplib.IMAP4.error as e:
        print("Email login or IMAP error:", e)

    except Exception as e:
        print("Error:", e)

    finally:

        if imap is not None:
            try:
                imap.logout()
            except Exception:
                pass

def main():

    print("\n===================================")
    print("       EMAIL RISK ANALYZER")
    print("===================================")

    print("1. Sample Testing")
    print("2. Scan Real Emails using IMAP")

    choice = input("\nEnter your choice (1 or 2): ")

    if choice == "1":

        sample_mode()

    elif choice == "2":

        imap_mode()

    else:

        print("Invalid choice! Please enter 1 or 2.")


if __name__ == "__main__":
    main()
