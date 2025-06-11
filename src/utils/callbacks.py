from dash import Input, Output, State

from src.utils.helper import wildfire_map, line_plot
from src.utils.load_data import read_geojson_inputdata


def register_callbacks(app):
    gdf, infra_df, exposure_data, full_exposure_data, infra_map, list_bins, list_hours = read_geojson_inputdata()

    @app.callback(
        [Output('map_title', 'children'),
         Output('choropleth_map', 'figure'),
         Output('line_plot', 'figure')],

        [Input('time_slider', 'value'),
         Input('infra_dropdown', 'value'),
         Input('basemap_dropdown', 'value')],

        [State('choropleth_map', 'figure')]
    )
    def update_graphs(selected_hour, selected_infra, selected_basemap, current_fig):

        fig_map, new_maptitle, fltr_exposure = wildfire_map(gdf, selected_hour, exposure_data, infra_map, selected_infra, current_fig,
                 full_exposure_data, selected_basemap)
        fig_line = line_plot(fltr_exposure, selected_hour, list_bins, list_hours)

        return new_maptitle, fig_map, fig_line
