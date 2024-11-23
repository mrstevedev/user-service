from argon2 import PasswordHasher

def decodePassword(digest, password):
    ph = PasswordHasher()
    return ph.verify(digest, password)