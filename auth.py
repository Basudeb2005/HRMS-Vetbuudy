import hashlib

# Pre-defined users with passwords
USERS = {
    'akshat_srivastava': 'password123',
    'rishika': 'pass456',
    'annika': 'pass789',
    'admin': 'adminpassword'
}

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def authenticate_user(username, password):
    hashed_pw = hash_password(password)
    if USERS.get(username) == hashed_pw:
        return True
    return False