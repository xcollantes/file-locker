"""File encryption and decryption system."""

import datetime
import os
from typing import List
from absl import app
from absl import flags
from absl import logging
from cryptography.fernet import Fernet

FLAGS = flags.FLAGS
flags.DEFINE_string("key", "", "Fernet key for decryption.")
flags.DEFINE_bool("destroy_original", False,
                  "Delete the unencrypted original when encrypting.")
flags.DEFINE_string("encrypt", None, "Encrypt file path.")
flags.DEFINE_string("decrypt", None, "Decrypt file path.")


def outputFernetKey(key: str) -> None:
    """Write out Fernet symmetric key to file."""
    now = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    with open(now, "wb") as keyFile:
        keyFile.write(key)


def readFernetKey(keyPath: str) -> bytes:
    """Read Fernet symmetric key from file and return key."""
    with open(keyPath, "rb") as keyFile:
        key: bytes = keyFile.read()
    return key


def encrypt(targetFile: str, fernet: Fernet) -> None:
    """Encrypt a file."""
    unencryptedFullPath: str = os.path.abspath(targetFile)
    filename: str = os.path.basename(unencryptedFullPath)
    dir: str = os.path.dirname(unencryptedFullPath)
    print(f"[ENCRYPT] Encrypting {filename}... ", end="")
    with open(targetFile, "rb") as target:
        targetContent: bytes = target.read()

    fileEncrypted: bytes = fernet.encrypt(targetContent)

    with open(os.path.join(dir, f"(encrypted) {filename}"), "wb") as encryptedFile:
        encryptedFile.write(fileEncrypted)

    print(f"{filename} encrypted")
    if FLAGS.destroy_original:
        os.remove(unencryptedFullPath)
        print(f"Removing unencrypted original {filename}")


def decrypt(encryptedFile: str, fernet: Fernet) -> None:
    fullPath: str = os.path.abspath(encryptedFile)
    filename: str = os.path.basename(fullPath).replace("(encrypted) ", "")
    dir: str = os.path.dirname(fullPath)
    print(f"[DECRYPT] Decrypting {filename}... ", end="")
    with open(encryptedFile, "rb") as encrypted:
        encryptedContent: bytes = encrypted.read()

    decryptedContent: bytes = fernet.decrypt(encryptedContent)

    with open(os.path.join(dir, filename), "wb") as decryptedFile:
        decryptedFile.write(decryptedContent)

    print(f"{filename} decrypted")
    os.remove(fullPath)


def main(argv: List[str]):
    if FLAGS.encrypt.startswith("(encrypted)"):
        logging.fatal("File is already encrypted.")

    if FLAGS.encrypt:
        key: bytes = Fernet.generate_key()
        fernet: Fernet = Fernet(key)
        encrypt(FLAGS.encrypt, fernet)
        outputFernetKey(key)
    elif FLAGS.decrypt:
        fernet: Fernet = Fernet(readFernetKey(FLAGS.key))
        decrypt(FLAGS.decrypt, fernet)
    else:
        logging.fatal("Specify --encrypt or --decrypt flag.")


if __name__ == "__main__":
    app.run(main)
