# Standard Library
import hashlib
from pathlib import Path

# Third Party
import rpyc
from cryptography.fernet import Fernet

# Project
from rsagent.config import params

TEST_FILE = Path(__file__).parent / "test.ios"

if __name__ == "__main__":
    conn = rpyc.connect("localhost", 4848)
    with TEST_FILE.open("r") as f:
        policy = f.read()
        encryption = Fernet(params.key.get_secret_value())
        encrypted = encryption.encrypt(policy.encode())
        decrypted_digest = hashlib.sha256(policy.encode()).hexdigest()
        encrypted_digest = hashlib.sha256(encrypted).hexdigest()
        conn.root.set_digest(encrypted_digest, decrypted_digest)
        conn.root.push_policy(encrypted)
