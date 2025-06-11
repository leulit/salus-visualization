"""
This dashboard is based on an example available in the the Dash gallery https://github.com/plotly/dash-opioid-epidemic-demo
"""
from dash import dcc, html
from matplotlib.pyplot import margins

from src.config import basemaps, map_colors, prob_bin_count
from src.utils.load_data import read_geojson_inputdata


gdf, infra_df, exposure_data, full_exposure_data, infra_map, list_bins, list_hours = read_geojson_inputdata()


def create_layout(app):
    return html.Div(
        id="root",
        children=[
            # Top logos and title
            html.Div(
                children=[
                    html.A(
                        children=html.Img(
                            src=app.get_asset_url("SALUS-logo.png"),
                            style={"height": "80px", "padding": "10px"}
                        ),
                        href="https://wildfire-salus.com/",
                        target="_blank",
                        style={"textDecoration": "none"}
                    ),
                    html.H1(
                        children="SALUS: Wildfire Propagation Data Viewer",
                        style={
                            "flex": "1",
                            "textAlign": "left",
                            "fontSize": "48px",
                            "margin": "10",
                        }
                    ),
                    html.A(
                        children=html.Img(
                            src=app.get_asset_url("logos_para_salus.png"),
                            style={"height": "80px", "padding": "10px"}
                        ),
                        href="https://www.ciencia.gob.es/",
                        target="_blank",
                        style={"textDecoration": "none"}
                    ),
                ],
                style={
                    "display": "flex",
                    "alignItems": "center",
                    "justifyContent": "space-between",
                    "width": "100%",
                    "padding": "10px",
                }
            ),

            # Main section
            html.Div(
                id="app-container",
                children=[
                    html.Div(
                        id="left-column",
                        children=[
                            html.Div(
                                id="slider-container",
                                children=[
                                    # html.P('Simulation Time Range', style={'marginBottom': '15px'}, id="map_title"),
                                    html.P(f'* Propagation Probability Map for hour 1 of {list_hours.max()}', style={'marginBottom': '15px'}, id="map_title"),

                                    dcc.Slider(
                                        id="time_slider",
                                        min=list_hours.min(),
                                        max=list_hours.max(),
                                        step=1,
                                        marks={i: {"label": str(i), "style": {"font-size": "18px", "color": "white"}}
                                               for i in range(gdf['hour'].min(), gdf['hour'].max() + 1)},
                                        value=gdf['hour'].min()
                                    ),
                                ],
                            ),
                            html.Div(
                                id="heatmap-container",
                                children=[
                                    dcc.Graph(id='choropleth_map', config={"scrollZoom": True}, style={"height": "600px"}),
                                    html.Span([
                                        "* Disclaimer: location of the simulation event is arbitrary and is not connected to real wildfire event. Exposure data is extracted from OpenStreetMap project.",
                                    ], style={"fontSize": "16px", "marginTop": "10px", "marginRight": "10px"})
                                ],
                            ),
                        ],
                    ),
                    html.Div(  # right column
                        id="graph-container",
                        children=[
                            html.P("Select Exposure Data:", style={'marginBottom': '10px'}  ),
                            dcc.Dropdown(
                                id="infra_dropdown",
                                options=[{'label': row, 'value': index} for index, row in enumerate(infra_map['name'])],
                                value=1,
                                clearable=False,
                                className='customDropdown',
                                style={'fontSize': '22px', 'marginBottom': '10px'},
                            ),
                            html.Div([
                                dcc.Graph(
                                    id="line_plot",
                                    figure=dict(layout=dict(
                                        paper_bgcolor="#333333",
                                        plot_bgcolor="#b3b3b3",
                                        autofill=True,
                                        margin=dict(t=25, r=50, b=100, l=50),
                                    )),
                                )
                            ]),
                            # Global legend
                            html.Div([
                                # Title
                                html.Div("Probability of Burned Area", style={
                                    "fontSize": "20px",
                                    "fontWeight": "bold",
                                    "marginBottom": "10px",
                                    "textAlign": "left"
                                }),

                                # Three-column layout for prob_bin_count = 4
                                html.Div([

                                    # Column 1
                                    html.Div([
                                        html.Div([
                                            html.Div(
                                                style={"width": "15px", "height": "15px",
                                                       "backgroundColor": map_colors["0"],
                                                       "marginRight": "5px"}),
                                            html.Span("0 - 25%", style={"fontSize": "16px"}),
                                        ], style={"display": "flex", "alignItems": "center", "marginBottom": "5px"}),

                                        html.Div([
                                            html.Div(
                                                style={"width": "15px", "height": "15px",
                                                       "backgroundColor": map_colors["25"],
                                                       "marginRight": "5px"}),
                                            html.Span("25 - 50%", style={"fontSize": "16px"}),
                                        ], style={"display": "flex", "alignItems": "center", "marginBottom": "5px"}),

                                    ], style={"flex": "1"}),


                                    # Column 2
                                    html.Div([

                                        html.Div([
                                            html.Div(
                                                style={"width": "15px", "height": "15px",
                                                       "backgroundColor": map_colors["50"],
                                                       "marginRight": "5px"}),
                                            html.Span("50 - 75%", style={"fontSize": "16px"}),
                                        ], style={"display": "flex", "alignItems": "center", "marginBottom": "5px"}),

                                        html.Div([
                                            html.Div(
                                                style={"width": "15px", "height": "15px",
                                                       "backgroundColor": map_colors["75"],
                                                       "marginRight": "5px"}),
                                            html.Span("75 - 100%", style={"fontSize": "16px"}),
                                        ], style={"display": "flex", "alignItems": "center", "marginBottom": "5px"}),
                                    ], style={"flex": "1"}),

                                    # Column 3 (label)
                                    html.Div([
                                        html.Div([
                                            html.Div(
                                                style={"width": "15px", "height": "15px", "backgroundColor": map_colors["-1"],
                                                       "marginRight": "5px"}),
                                            html.Span("Buffer zone", style={"fontSize": "16px"}),
                                        ], style={"display": "flex", "alignItems": "center", "marginBottom": "5px"}),
                                    ], style={"flex": "1", "marginLeft": "30px", "color": "white",
                                              "fontWeight": "bold"}),
                                ], style={
                                    "display": "flex",
                                    "justifyContent": "space-between",
                                    "marginBottom": "10px"
                                }),

                            ], style={
                                "marginTop": "0px",
                                "padding": "10px",
                                "backgroundColor": "transparent",
                                "color": "white",
                                "borderRadius": "10px"
                            }),
                            html.Div([
                                html.P("Select Basemap:", style={
                                    'marginTop': '5px',
                                    'marginBottom': '10px',
                                    'marginRight': '15px',
                                    'fontSize': '20px',
                                    'whiteSpace': 'nowrap'
                                }),

                                dcc.Dropdown(
                                    id='basemap_dropdown',
                                    options=[{'label': basemaps[key]["dropdown_label"], 'value': key} for key in
                                             basemaps],
                                    value='pnoa_lidar',
                                    clearable=False,
                                    style={'width': '300px', 'fontSize': '18px'}
                                )
                            ], style={
                                'display': 'flex',
                                'alignItems': 'center',
                                'marginTop': '20px',
                                'gap': '10px'
                            }),
                        ],
                    ),
                ],
            ),
            # Footnote
            html.Footer(
                children=[
                    html.Span("App layout and code is based on the example available in the "),
                    html.A("Dash gallery",
                           href="https://github.com/plotly/dash-opioid-epidemic-demo",
                           target="_blank",
                           style={'color': '#0074D9'})
                ],
                style={
                    'fontSize': '12px',
                    'marginTop': '50px',
                    'textAlign': 'center',
                    'fontStyle': 'italic'
                }
            )
        ]
    )
