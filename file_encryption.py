
import os
import base64
import hashlib
import secrets
from getpass import getpass
from cryptography.fernet import Fernet, InvalidToken

# Generate encryption key from password
def generate_key(password, salt):
    key = hashlib.pbkdf2_hmac(
        'sha256',
        password.encode(),
        salt,
        600000
    )
    return base64.urlsafe_b64encode(key)


# Encrypt file
def encrypt_file():

    file_path = input("Enter file path: ")
    password = getpass("Enter encryption password: ")

    if not os.path.isfile(file_path):
        print("File not found!")
        return

    if not password:
        print("Password cannot be empty!")
        return

    try:
        with open(file_path, "rb") as file:
            data = file.read()

        salt = secrets.token_bytes(16)
        key = generate_key(password, salt)
        fernet = Fernet(key)

        encrypted_data = fernet.encrypt(data)

        output_file = file_path + ".enc"

        with open(output_file, "wb") as file:
            file.write(salt + encrypted_data)

        print("\nFile encrypted successfully!")
        print("Encrypted file:", output_file)

    except OSError as error:
        print("File error:", error)


# Decrypt file
def decrypt_file():

    file_path = input("Enter encrypted file path: ")
    password = getpass("Enter decryption password: ")

    if not os.path.isfile(file_path):
        print("Encrypted file not found!")
        return

    if not password:
        print("Password cannot be empty!")
        return

    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()

        if len(encrypted_data) < 17:
            print("Invalid encrypted file!")
            return

        salt = encrypted_data[:16]
        encrypted_content = encrypted_data[16:]

        key = generate_key(password, salt)
        fernet = Fernet(key)

        decrypted_data = fernet.decrypt(encrypted_content)

        output_file = file_path[:-4] + "_restored"

        with open(output_file, "wb") as file:
            file.write(decrypted_data)

        print("\nFile decrypted successfully!")
        print("Restored file:", output_file)

    except InvalidToken:
        print("Incorrect password or corrupted encrypted file!")

    except OSError as error:
        print("File error:", error)


# Main menu
while True:

    print("\n===== FILE ENCRYPTION AND DECRYPTION =====")
    print("1. Encrypt a File")
    print("2. Decrypt a File")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        encrypt_file()

    elif choice == "2":
        decrypt_file()

    elif choice == "3":
        print("Exiting program. Thank you!")
        break

    else:
        print("Invalid choice! Please try again.")
