"""Read config variables from environment."""

# Standard Library
import os
from pathlib import Path

# Third Party
from pydantic import FilePath, SecretBytes, BaseSettings, IPvAnyAddress, validator


class Params(BaseSettings):
    """Application Parameters."""

    listen_address: IPvAnyAddress = "::"
    listen_port: int = 4848
    frr_reload: FilePath = "/usr/lib/frr/frr-reload.py"
    key: SecretBytes

    @validator("frr_reload")
    def validate_frr_reload(cls, value: Path) -> Path:
        """Ensure FRR Reload script is executable."""

        if isinstance(value, Path):
            value = Path(value)

        if not os.access(value, os.X_OK):
            raise ValueError(f"User does not have executable permission to '{value}'")

        return value

    class Config:
        """Pydantic Config."""

        env_prefix = "ix_rsagent_"


params = Params()
