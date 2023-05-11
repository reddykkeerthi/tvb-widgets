# -*- coding: utf-8 -*-
#
# "TheVirtualBrain - Widgets" package
#
# (c) 2022-2023, TVB Widgets Team
#

import numpy as np
import ipywidgets as widgets
from plotly_resampler import register_plotly_resampler, FigureWidgetResampler
from tvbwidgets.ui.ts.base_ts_widget import TimeSeriesWidgetBase

class TimeSeriesWidgetPlotly(TimeSeriesWidgetBase):
    """ TimeSeries Widget drawn using plotly"""

    def __init__(self, **kwargs):
        # data
        self.fig = None
        self.data = None
        self.ch_names = []
        self.raw = None
        self.sample_freq = 0
        self.start_time = 0
        self.end_time = 0
        self.std_step = 0
        self.amplitude = 1

        # plot & UI
        self.checkboxes = dict()
        self.plot_and_channels_area = widgets.HBox()
        self.output = widgets.Output(layout=widgets.Layout(width='75%'))
        self.channel_selection_area = widgets.HBox(layout=widgets.Layout(width='25%', height='700px',
                                                                         margin="50px 0px 0px 0px"))
        self.plot_and_channels_area.children += (self.output, self.channel_selection_area)
        self.scaling_title = widgets.Label(value='Increase/Decrease signal scaling (scaling value to the right)')
        self.scaling_slider = widgets.IntSlider(value=1, layout=widgets.Layout(width='30%'))

        super().__init__([self.plot_and_channels_area, self.scaling_title, self.scaling_slider],
                         layout=self.DEFAULT_BORDER)
        self.logger.info("TimeSeries Widget with Plotly initialized")

    # =========================================== SETUP ================================================================
    def _populate_from_data_wrapper(self, data_wrapper):
        super()._populate_from_data_wrapper(data_wrapper=data_wrapper)
        del self.ch_order, self.ch_types  # delete these as we don't use them in plotly
        self.channels_area = self._create_channel_selection_area(array_wrapper=data_wrapper)
        self._setup_scaling_slider()
        self.channel_selection_area.children += (self.channels_area,)
        self.plot_ts_with_plotly()

    # =========================================== PLOT =================================================================
    def add_traces_to_plot(self, data, ch_names):
        """ Draw the traces """
        # traces will be added from bottom to top, so reverse the lists to put the first channel on top
        data = data[::-1]
        ch_names = ch_names[::-1]

        self.fig.add_traces(
            [dict(y=ts * self.amplitude + i * self.std_step, name=ch_name, customdata=ts, hovertemplate='%{customdata}')
             for i, (ch_name, ts) in enumerate(zip(ch_names, data))]
        )

    def _populate_plot(self, data=None, ch_names=None):
        # create traces for each signal
        data_from_raw, times = self.raw[:, :]
        data = data if data is not None else data_from_raw
        ch_names = ch_names if ch_names is not None else self.ch_names
        self.std_step = 10 * np.max(np.std(data, axis=1))

        self.add_traces_to_plot(data, ch_names)

        # display channel names for each trace
        for i, ch_name in enumerate(ch_names[::-1]):
            self.fig.add_annotation(
                x=0.0, y=i * self.std_step,
                text=ch_name,
                showarrow=False,
                xref='paper',
                xshift=-70
            )

        # add ticks between channel names and their traces
        self.fig.update_yaxes(fixedrange=False, showticklabels=False, ticks='outside', ticklen=3,
                              tickvals=np.arange(len(ch_names)) * self.std_step)

        # configure legend
        self.fig.update_layout(
            # traces are added from bottom to top, but legend displays the names from top to bottom
            legend={'traceorder': 'reversed'}
        )

    def add_visibility_buttons(self):
        # buttons to show/hide all traces
        self.fig.update_layout(dict(updatemenus=[dict(type="buttons", direction="left",
                                                      buttons=list([dict(args=["visible", True], label="Show All",
                                                                         method="restyle"),
                                                                    dict(args=["visible", False], label="Hide All",
                                                                         method="restyle")
                                                                    ]),
                                                      showactive=False,  # personal preference
                                                      # position buttons in top right corner of plot
                                                      x=1,
                                                      xanchor="right",
                                                      y=1.1,
                                                      yanchor="top")]
                                    ))

    def create_plot(self, data=None, ch_names=None):
        # register resampler so every plot will benefit from it
        register_plotly_resampler(mode='auto')

        self.fig = FigureWidgetResampler()

        self._populate_plot(data, ch_names)

        # different visual settings
        self.fig.update_layout(
            width=1000, height=800,
            showlegend=True,
            template='plotly_white'
        )

        self.add_visibility_buttons()

    def plot_ts_with_plotly(self, data=None, ch_names=None):
        self.create_plot(data, ch_names)
        with self.output:
            self.output.clear_output(wait=True)
            display(self.fig)

    # ================================================ TIMELINE ========================================================
    def _setup_scaling_slider(self):
        # set min and max scaling values
        self.scaling_slider.min = 1
        self.scaling_slider.max = 10
        self.scaling_slider.observe(self.update_scaling, names='value', type='change')

    def update_scaling(self, val):
        """ Update the amplitude of traces based on slider value """
        new_val = val['new']
        self.amplitude = new_val

        # delete old traces
        self.fig.data = []
        data =  self.raw[:, :][0]

        self.add_traces_to_plot(data, self.ch_names)

    # =========================================== CHANNELS SELECTION ===================================================
    def _create_channel_selection_area(self, array_wrapper, no_checkbox_columns=2):
        # type: (ABCDataWrapper) -> widgets.Accordion
        """ Create the whole channel selection area: Submit button to update plot, Select/Uselect all btns,
            State var. & Mode selection and Channel checkboxes
        """
        # checkboxes
        checkboxes_region = self._create_checkboxes(array_wrapper=array_wrapper,
                                                    no_checkbox_columns=no_checkbox_columns)
        for cb_stack in checkboxes_region.children:
            cb_stack.layout = widgets.Layout(width='50%')

        # selection submit button
        self.submit_selection_btn = widgets.Button(description='Submit selection', layout=self.BUTTON_STYLE)
        self.submit_selection_btn.on_click(self._update_ts)

        # select/unselect all buttons
        select_all_btn, unselect_all_btn = self._create_select_unselect_all_buttons()

        # select dimensions buttons (state var. & mode)
        selections = self._create_dim_selection_buttons(array_wrapper=array_wrapper)
        for selection in selections:
            selection.layout = widgets.Layout(width='50%')

        # add all buttons to channel selection area
        channels_region = widgets.VBox(children=[self.submit_selection_btn, widgets.HBox(selections),
                                                 widgets.HBox([select_all_btn, unselect_all_btn]),
                                                 checkboxes_region])
        channels_area = widgets.Accordion(children=[channels_region], selected_index=None,
                                          layout=widgets.Layout(width='70%'))
        channels_area.set_title(0, 'Channels')
        return channels_area

    def _update_ts(self, btn):
        self.logger.debug('Updating TS')
        ch_names = list(self.ch_names)

        # save selected channels using their index in the ch_names list
        picks = []
        for cb in list(self.checkboxes.values()):
            ch_index = ch_names.index(cb.description)  # get the channel index
            if cb.value:
                picks.append(ch_index)  # list with number representation of channels

        # if unselect all
        # TODO: should we remove just the traces and leave the channel names and the ticks??
        if not picks:
            self.fig.data = []  # remove traces
            self.fig.layout.annotations = []  # remove channel names
            self.fig.layout.yaxis.tickvals = []  # remove ticks between channel names and traces
            return

        # get data and names for selected channels; self.raw is updated before redrawing starts
        data, _ = self.raw[:, :]
        data = data[picks, :]
        ch_names = [ch_names[i] for i in picks]

        # redraw the entire plot
        self.plot_ts_with_plotly(data, ch_names)
