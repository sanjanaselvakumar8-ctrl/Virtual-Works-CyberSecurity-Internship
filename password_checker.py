
import string

def check_password_strength(password):

    score = 0
    feedback = []

    # 1. Check password length
    if len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        feedback.append("Use at least 8 characters (12 or more is better).")

    # 2. Check uppercase letters
    if any(char.isupper() for char in password):
        score += 1
    else:
        feedback.append("Add at least one uppercase letter (A-Z).")

    # 3. Check lowercase letters
    if any(char.islower() for char in password):
        score += 1
    else:
        feedback.append("Add at least one lowercase letter (a-z).")

    # 4. Check numbers
    if any(char.isdigit() for char in password):
        score += 1
    else:
        feedback.append("Add at least one number (0-9).")

    # 5. Check special characters
    if any(char in string.punctuation for char in password):
        score += 1
    else:
        feedback.append("Add at least one special character (!, @, #, etc.).")

    # Classify password strength
    if score >= 6:
        strength = "Strong"
    elif score >= 4:
        strength = "Medium"
    else:
        strength = "Weak"

    print("\n----- PASSWORD STRENGTH REPORT -----")
    print("Password Strength:", strength)
    print("Score:", score, "/ 6")

    if feedback:
        print("\nSuggestions to improve your password:")
        for suggestion in feedback:
            print("-", suggestion)
    else:
        print("\nExcellent! Your password meets all the basic checks.")

# Main program
password = input("Enter your password: ")

check_password_strength(password)
