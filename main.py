import argparse
import os
import hashlib
import getpass
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from base64 import urlsafe_b64encode, urlsafe_b64decode

# === Constantes ===
BACKEND = default_backend()
SALT_SIZE = 16
KEY_SIZE = 32
IV_SIZE = 16



def derive_key(password: str, salt: bytes) -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=100000,
        backend=BACKEND
    )
    return kdf.derive(password.encode())
 
def sha256sum(filename):
    h = hashlib.sha256()
    with open(filename, "rb") as f:
        while chunk := f.read(4096):
            h.update(chunk)
    return h.hexdigest()

def encrypt_file(filepath, password, delete_source=False):
    salt = os.urandom(SALT_SIZE)
    iv = os.urandom(IV_SIZE)
    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=BACKEND) 
    encryptor = cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder() 

    with open(filepath, 'rb') as f:
        data = f.read()
        sha256_hash = sha256sum(filepath)

    padded_data = padder.update(data) + padder.finalize()
    encrypted = encryptor.update(padded_data) + encryptor.finalize()

    with open(filepath + ".enc", 'wb') as f:
        f.write(salt + iv + encrypted)
        f.flush() 
        os.fsync(f.fileno())

    if delete_source:
        os.remove(filepath)
        print(f"[INFO] Fichier source supprimé : {filepath}")    

    print(f"[OK] Fichier chiffré : {filepath}.enc")

def decrypt_file(filepath, password, delete_source=False):
    with open(filepath, 'rb') as f:
        content = f.read()
        salt = content[:SALT_SIZE] 
        iv = content[SALT_SIZE:SALT_SIZE + IV_SIZE]
        encrypted = content[SALT_SIZE + IV_SIZE:] 

    key = derive_key(password, salt)

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=BACKEND)
    decryptor = cipher.decryptor()
    decrypted_padded = decryptor.update(encrypted) + decryptor.finalize()


    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()

    try:
        decrypted = unpadder.update(decrypted_padded) + unpadder.finalize()
    except ValueError:
        print("[ERREUR] Mot de passe incorrect ou fichier corrompu.")
        return


    if filepath.endswith(".enc"):
        output_path = filepath[:-4]
    else:
        output_path = filepath + ".decrypted"
    with open(output_path, 'wb') as f:
        f.write(decrypted)

    if delete_source:
        os.remove(filepath)
        print(f"[INFO] Fichier chiffré supprimé : {filepath}")

    print(f"[OK] Fichier déchiffré : {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Chiffrement/Déchiffrement AES + SHA256")
    parser.add_argument('-e', '--encrypt', type=str, help="Fichier à chiffrer")
    parser.add_argument('-d', '--decrypt', type=str, help="Fichier à déchiffrer")
    parser.add_argument('--delete', action='store_true', help="Supprimer le fichier source après l'opération")
    args = parser.parse_args()

    if args.encrypt:
        password = getpass.getpass("Mot de passe pour chiffrer : ") 
        encrypt_file(args.encrypt, password, delete_source=args.delete)
    elif args.decrypt:
        password = getpass.getpass("Mot de passe pour déchiffrer : ")
        decrypt_file(args.decrypt, password, delete_source=args.delete)
    else:
        print("Utilisez -e pour chiffrer ou -d pour déchiffrer un fichier.")

if __name__ == "__main__":
    main()
