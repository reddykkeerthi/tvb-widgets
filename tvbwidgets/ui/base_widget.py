# -*- coding: utf-8 -*-
#
# "TheVirtualBrain - Widgets" package
#
# (c) 2022-2023, TVB Widgets Team
#
from ipywidgets import DOMWidget
from tvb.basic.neotraits.api import HasTraits

from tvbwidgets.core.logger.builder import get_logger


class TVBWidget(object):

    def __init__(self, **kwargs):
        self.logger = get_logger(self.__class__.__module__)

    def get_widget(self):
        if isinstance(self, DOMWidget):
            return self
        self.logger.error("Not a valid widget! Try to overwrite get_widget or inherit DOMWidget!")
        raise RuntimeWarning("Not a valid widget!")

    def add_datatype(self, datatype):
        # type: (HasTraits) -> None
        raise NotImplementedError
