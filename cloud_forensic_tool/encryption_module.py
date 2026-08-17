from key_manager import load_key
import os


def encrypt_file(filepath):
    fernet = load_key()

    with open(filepath, "rb") as f:
        data = f.read()

    encrypted = fernet.encrypt(data)

    filename = os.path.basename(filepath)
    encrypted_path = "evidence/" + filename + ".enc"

    with open(encrypted_path, "wb") as f:
        f.write(encrypted)

    print("Evidence encrypted:", encrypted_path)


def decrypt_file(encrypted_path):
    fernet = load_key()

    with open(encrypted_path, "rb") as f:
        encrypted_data = f.read()

    decrypted = fernet.decrypt(encrypted_data)

    output_path = encrypted_path.replace(".enc", "_decrypted.txt")

    with open(output_path, "wb") as f:
        f.write(decrypted)

    print("Evidence decrypted:", output_path)