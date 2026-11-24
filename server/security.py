from pwdlib import PasswordHash

hasher = PasswordHash.recommended()

def hash_password(raw_password: str) -> str:
    return hasher.hash(raw_password)

def verify_password(raw_password: str, password_hash: str) -> bool:
    return hasher.verify(raw_password, password_hash)