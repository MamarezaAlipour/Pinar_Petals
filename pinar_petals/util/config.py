"""

Define configuration parameters.
"""

__all__ = [
    'CONFIG',
]


import logging
from pathlib import Path

import pinar
import pinar.util.config
from pinar.util.config import (
    Config, _fetch_conf, CONFIG_NAME, CONFIG, CONSOLE)

LOGGER = logging.getLogger('pinar_petals')
LOGGER.propagate = False
LOGGER.addHandler(CONSOLE)

CORE_DIR = Path(pinar.__file__).parent
SOURCE_DIR = Path(__file__).absolute().parent.parent

CONFIG.__dict__ = Config.from_dict(_fetch_conf([
    CORE_DIR / 'conf',  # default config from the pinar repository
    SOURCE_DIR / 'conf',  # default config from the pinar_petals repository
    Path.home() / 'pinar' / 'conf',  # ~/pinar/conf directory
    Path.home() / '.config',  # ~/.config directory
    Path.cwd(),  # current working directory
], CONFIG_NAME)).__dict__
LOGGER.setLevel(getattr(logging, CONFIG.log_level.str()))
