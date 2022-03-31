# File Locker
Command line encryption system for files.  

# Usage

```
locker.py:
  --decrypt: Decrypt file path. Decrypts file. Must specify --key.
  --[no]destroy_original: Delete the unencrypted original when encrypting.
    (default: 'false')
  --encrypt: Encrypt file path. Creates symmetric key and encrypts with that key.
  --key: Fernet key for decryption.
    (default: '')
```
