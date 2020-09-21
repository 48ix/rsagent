"""Services Entry."""

# Standard Library
import hashlib
import logging
from typing import Any
from pathlib import Path

# Third Party
from rpyc import Service
from cryptography.fernet import Fernet, InvalidToken

# Project
from rsagent.config import params
from rsagent.frrouting import merge_config, validate_config

log = logging.getLogger(f"{__package__}.{__name__}")

OUTPUT_DIR = Path.home() / "rs-policies"


class Agent(Service):
    """Route Server Agent Service."""

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """Set custom attributes."""
        super().__init__(*args, **kwargs)
        self.digest_encrypted: str = ""
        self.digest_decrypted: str = ""

    def verify_payload(self, encrypted: bytes) -> str:
        """Verify that input data digest matches pre-sent digest."""
        if not all((self.digest_encrypted, self.digest_decrypted)):
            raise UnboundLocalError("No digests have been set.")

        # Validate encrypted data
        encrypted_input_digest = hashlib.sha256(encrypted).hexdigest()
        if encrypted_input_digest != self.digest_encrypted:
            log.error("Invalid digest for encrypted data: %s", encrypted_input_digest)
            raise ValueError("Digest doesn't match encrypted data.")

        # Decompress data & validate digest
        encryption = Fernet(params.key.get_secret_value())

        try:
            decrypted = encryption.decrypt(encrypted)
        except InvalidToken:
            log.critical("Invalid token for data %s", encrypted_input_digest)

        decrypted_input_digest = hashlib.sha256(decrypted).hexdigest()

        if decrypted_input_digest != self.digest_decrypted:
            log.error("Invalid digest for decrypted data: %s", decrypted_input_digest)
            raise ValueError("Digest doesn't match decrypted data.")

        return decrypted.decode()

    def exposed_set_digest(self, encrypted: str, decrypted: str) -> None:
        """Set the digest of incoming data."""
        self.digest_encrypted = encrypted
        self.digest_decrypted = decrypted
        log.info("Set encrypted digest %s", encrypted)
        log.info("Set decrypted digest %s", decrypted)

    def exposed_push_policy(self, policy: bytes) -> str:
        """Ingest new FRR policy & apply."""
        result = "An unknown error occurred."

        try:
            payload = self.verify_payload(policy)

            OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
            policy_file = OUTPUT_DIR / f"{self.digest_decrypted}.ios"

            with policy_file.open("w") as f:
                f.write(payload)

            valid = validate_config(policy_file)

            if not valid:
                raise RuntimeError(f"Config {self.digest_decrypted} failed validation.")

            merged = merge_config(policy_file)

            if not merged:
                raise RuntimeError(
                    f"Merge of config {self.digest_decrypted} failed, check the logs."
                )

            result = f"Successfully Merged Configuration {self.digest_decrypted}"

        except Exception as err:
            result = str(err)

        return result
