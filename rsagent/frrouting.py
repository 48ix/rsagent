"""FRRouting Interaction."""

# Standard Library
import logging
import subprocess
from pathlib import Path

# Project
from rsagent.config import params

log = logging.getLogger(f"{__package__}.{__name__}")


def validate_config(file: Path) -> bool:
    """Run FRR Reload Script with --test to validate new config."""
    completed = subprocess.run([str(params.frr_reload), "--test", str(file)])
    valid = completed.returncode == 0

    if not valid:
        log.error("Config %s is invalid", file.name)
    else:
        log.info("Config %s is valid", file.name)

    return valid


def merge_config(file: Path) -> bool:
    """Merge new config with running FRR config."""
    completed = subprocess.run(
        [str(params.frr_reload), "--reload", str(file)], capture_output=True
    )

    if completed.stderr:
        log.error(completed.stderr.decode())

    valid = completed.returncode == 0

    if valid:
        log.info("Merged config %s", file.name)

    return valid
