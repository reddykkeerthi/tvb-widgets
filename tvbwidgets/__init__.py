# -*- coding: utf-8 -*-
#
# "TheVirtualBrain - Widgets" package
#
# (c) 2022-2023, TVB Widgets Team
#

from pkg_resources import get_distribution, DistributionNotFound
from .logger.builder import get_logger

LOGGER = get_logger(__name__)
try:
    __version__ = get_distribution("tvb-widgets").version
except DistributionNotFound:
    LOGGER.debug("Package is not fully installed")
    try:
        from ._version import __version__

        LOGGER.debug("Version read from the internal _version.py file")
    except ImportError:
        LOGGER.warn("Version not found, we will use fallback")
        __version__ = "1.0"

LOGGER.info(f"Version: {__version__}")
