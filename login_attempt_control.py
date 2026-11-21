
import time

# Login Attempt Control System

CORRECT_PASSWORD = "admin123"
MAX_ATTEMPTS = 3
LOCKOUT_TIME = 30

attempts = 0

print("===== LOGIN ATTEMPT CONTROL SYSTEM =====")

while True:

    if attempts >= MAX_ATTEMPTS:
        print("\nToo many incorrect attempts!")
        print(f"Access restricted for {LOCKOUT_TIME} seconds.")

        time.sleep(LOCKOUT_TIME)

        print("\nYou can try logging in again.")
        attempts = 0

    password = input("\nEnter your password: ")

    if password == CORRECT_PASSWORD:
        print("\nLogin successful!")
        print("Welcome to the system.")
        break

    else:
        attempts += 1
        remaining = MAX_ATTEMPTS - attempts

        print("Incorrect password!")

        if remaining > 0:
            print(f"Attempts remaining: {remaining}")
        else:
            print("Maximum attempts reached!")
