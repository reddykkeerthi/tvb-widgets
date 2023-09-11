# -*- coding: utf-8 -*-
#
# "TheVirtualBrain - Widgets" package
#
# (c) 2022-2023, TVB Widgets Team
#
import ipywidgets

from tvbwidgets.ui.connectivity_ipy.config import ConnectivityConfig
from tvbwidgets.ui.connectivity_ipy.exceptions import UnknownOutputException
from enum import Enum
import ipywidgets as widgets
import pyvista


class Output3D(Enum):
    PYVISTA = 'PyVista'

    def __str__(self):
        return str(self.value)


class PyVistaOutput(widgets.Output):
    CONFIG = ConnectivityConfig()
    plotter = pyvista.Plotter()

    def toggle_actor(self, actor, visible):
        if visible:
            self.display_actor(actor)
        else:
            self.hide_actor(actor)
        self.update_plot()

    def display_actor(self, actor):
        self.plotter.renderer.add_actor(actor, render=False)

    def hide_actor(self, actor):
        self.plotter.renderer.remove_actor(actor, render=False)

    def update_plot(self):
        with self:
            self.clear_output(wait=True)
            self.plotter.show()

    def get_window_controls(self):
        height = ipywidgets.IntSlider(
            value=self.CONFIG.size[1],
            min=50,
            max=1500,
            step=1,
            orientation='horizontal',
            description='Plot height',
            continuous_update=False,
        )
        width = ipywidgets.IntSlider(
            value=self.CONFIG.size[0],
            min=50,
            max=1500,
            step=1,
            orientation='horizontal',
            description='Plot width',
            continuous_update=False,
        )

        self.plotter.window_size = [width.value, height.value]

        def on_change_height(value):
            self.plotter.window_size = [width.value, value['new']]
            self.update_plot()

        def on_change_width(value):
            self.plotter.window_size = [value['new'], height.value]
            self.update_plot()

        height.observe(on_change_height, 'value')
        width.observe(on_change_width, 'value')
        return ipywidgets.HBox(children=(width, height))


def output_3d_factory(output_type):
    """Factory function for a custom 3d output"""
    if output_type == Output3D.PYVISTA:
        return PyVistaOutput()
    raise UnknownOutputException(f"No applicable output for {output_type}!")
