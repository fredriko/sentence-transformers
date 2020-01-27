import platform
from pathlib import Path


def get_data_root() -> Path:
    if platform.system() == "Darwin":
        data_root = Path("/Users/fredriko")
    else:
        data_root = Path("/")
    return data_root
