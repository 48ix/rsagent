"""Agent Server Entrypoint."""

# Standard Library
import logging

# Third Party
from rpyc.utils.server import ThreadedServer

# Project
from rsagent.config import params
from rsagent.services.main import Agent

logger = logging.getLogger(f"{__package__}.{__name__}")


if __name__ == "__main__":
    server = ThreadedServer(
        Agent,
        hostname=str(params.listen_address),
        port=params.listen_port,
        ipv6=True,
        logger=logger,
    )
    server.start()
