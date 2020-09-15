"""Read config variables from environment."""

# Third Party
from pydantic import FilePath, SecretBytes, BaseSettings, IPvAnyAddress


class Params(BaseSettings):
    """Application Parameters."""

    listen_address: IPvAnyAddress = "::"
    listen_port: int = 4848
    frr_reload: FilePath = "/usr/lib/frr/frr-reload.py"
    key: SecretBytes

    class Config:
        """Pydantic Config."""

        env_prefix = "ix_rsagent_"


params = Params()
