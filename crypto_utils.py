import os
import base64
from cryptography.hazmat.primitives.kdf.argon2 import Argon2id
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

def derive_key(password: str, salt: bytes) -> bytes:
    kdf = Argon2id(
        salt=salt,
        length=32,
        iterations=3,
        lanes=4,
        memory_cost=65536,
    )
    return kdf.derive(password.encode("utf-8"))

def encrypt(plaintext, password):
    salt = os.urandom(16)
    nonce = os.urandom(12)
    data = plaintext.encode("utf-8")
    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, data, None)

    return(base64.b64encode(nonce+ salt + ciphertext).decode("ascii"))

def decrypt(token, password):
    data = base64.b64decode(token)
    nonce = data[:12]
    salt = data[12:28]
    ciphertext = data[28:]

    key = derive_key(password, salt)
    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, None)
    except InvalidTag:
        raise ValueError("Ontsleutelen mislukt: verkeerd wachtwoord of de tekst is aangepast.")
    return plaintext.decode("utf-8")


