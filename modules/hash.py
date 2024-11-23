from argon2 import PasswordHasher

def hashPassword(password):
    ph = PasswordHasher()
    return ph.hash(password)