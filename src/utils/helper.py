import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

from src.config import basemaps, map_colors, prob_name


def wildfire_map(gdf, selected_hour, exposure_data, infra_map, selected_infra, current_fig,
                 full_exposure_data, selected_basemap):

    new_maptitle = f"* Propagation Probability Map for hour {selected_hour} of {gdf['hour'].max()}"

    # --------------------------------------------------------
    # Filter datasets
    filtered_gdf = gdf[gdf['hour'] == selected_hour]

    fltr_exposure = exposure_data[exposure_data['infra'] == infra_map.loc[selected_infra]['infra']]
    fltr_exposure_hour = fltr_exposure[fltr_exposure['hour'] == selected_hour]

    # Zoom and center for the map
    zoom = current_fig['layout']['mapbox']['zoom'] if current_fig else 12
    center = current_fig['layout']['mapbox']['center'] if current_fig else {
        "lat": filtered_gdf.geometry.centroid.y.mean(),
        "lon": filtered_gdf.geometry.centroid.x.mean()
    }

    # --------------------------------------------------------
    # Create Map Figure

    # Convert values to string (safe way)
    filtered_gdf = filtered_gdf.copy()
    filtered_gdf[f"{prob_name}_str"] = filtered_gdf[prob_name].astype(int).astype(str)


    fig_map = px.choropleth_mapbox(
        filtered_gdf,
        geojson=filtered_gdf.__geo_interface__,
        locations=filtered_gdf.index,
        color=f"{prob_name}_str",
        color_discrete_map=map_colors,
        mapbox_style="carto-positron",
        center=center,
        zoom=zoom,
        opacity=0.5,
        title=f"Hour {selected_hour}"
    )
    # Disable hover text
    fig_map.update_traces(hovertemplate=None, hoverinfo='skip')

    # Add the complete exposure dataset
    if "complete_db" == infra_map.loc[selected_infra]['infra']:

        # Separate into points and lines
        points_gdf = full_exposure_data[full_exposure_data.geometry.geom_type == 'Point']
        lines_gdf = full_exposure_data[
            full_exposure_data.geometry.geom_type.isin(['LineString', 'MultiLineString'])]

        # Optional: reset index
        points_gdf = points_gdf.reset_index(drop=True)
        lines_gdf = lines_gdf.reset_index(drop=True)

        if len(lines_gdf) > 0:
            for idx, row in lines_gdf.iterrows():
                for line in [row['geometry']] if row['geometry'].geom_type == 'LineString' else row[
                    'geometry'].geoms:
                    lons, lats = zip(*list(line.coords))
                    fig_map.add_trace(go.Scattermapbox(
                        lon=lons,
                        lat=lats,
                        mode='lines',
                        line=dict(width=2, color='black'),
                        hoverinfo='skip'
                    ))

        if len(points_gdf) > 0:
            # Add points as a scatter layer
            points_df = points_gdf.copy()

            # Extract latitude and longitud
            points_df["lon"] = points_gdf.geometry.x
            points_df["lat"] = points_gdf.geometry.y
            points_df = points_df.drop(columns="geometry")

            fig_map.add_trace(go.Scattermapbox(
                lat=points_df["lat"],
                lon=points_df["lon"],
                mode="markers",
                marker=dict(size=10, color="white"), #, showscale=False),
                text=points_df["id"],
                hoverinfo='skip',
            ))

    # Add exposure data as lines and points (on top of polygons)
    if not fltr_exposure_hour.empty and len(fltr_exposure_hour) > 0:
        for idx, row in fltr_exposure_hour.iterrows():
            # Check if the geometry is a LINESTRING or MULTILINESTRING
            if row['geometry'].geom_type in ['LineString', 'MultiLineString']:
                for line in [row['geometry']] if row['geometry'].geom_type == 'LineString' else row[
                    'geometry'].geoms:
                    lons, lats = zip(*list(line.coords))
                    fig_map.add_trace(go.Scattermapbox(
                        lon=lons,
                        lat=lats,
                        mode='lines',
                        line=dict(width=2, color='black'), #, showscale=False),
                        hoverinfo='skip'
                    ))

    if fltr_exposure_hour.geom_type.unique().tolist() == ["Point"]:
        # Add points as a scatter layer
        points_df = fltr_exposure_hour.copy()
        # Extract latitude and longitud
        points_df["lon"] = fltr_exposure_hour.geometry.x
        points_df["lat"] = fltr_exposure_hour.geometry.y
        points_df = points_df.drop(columns="geometry")

        fig_map.add_trace(go.Scattermapbox(
            lat=points_df["lat"],
            lon=points_df["lon"],
            mode="markers",
            marker=dict(size=10, color="black"), #, showscale=False),
            text=points_df["id"],
            hoverinfo='skip'
        ))

    # Get the selected basemap URL and credits
    basemap_url = basemaps[selected_basemap]["url"]

    # Update map with WMTS Layer and map credits at the bottom of the page
    fig_map.update_layout(
        mapbox=dict(
            style="white-bg",
            layers=[{
                "sourcetype": "raster",
                "below": "traces",
                "source": [basemap_url],
            }],
        ),
        xaxis_visible=False,
        yaxis_visible=False,
        showlegend=False,
        margin=dict(l=0, r=0, t=0, b=0),
        annotations=[
            dict(
                text=basemaps[selected_basemap]["credits"],
                x=1,
                y=0,
                xref='paper',
                yref='paper',
                showarrow=False,
                font=dict(color='black'),
                bgcolor='rgba(255,255,255,0.6)',
                borderpad=4,
                align='right'
            )
        ]
    )
    fig_map.data = sorted(fig_map.data, key=lambda x: x.type == "scattermapbox", reverse=True)

    return fig_map, new_maptitle, fltr_exposure

def create_df_plot(fltr_exposure, list_bins, list_hours):
    if fltr_exposure.size > 0:
        if fltr_exposure['geometry_type'].unique() == 'p':
            geom = 'p'
            yaxis_name = "Amount of assets"
        elif fltr_exposure['geometry_type'].unique() == 'l':
            geom = 'l'
            yaxis_name = "Total length (km)"

        # Create base DataFrame with all combinations
        plt_df = pd.DataFrame([(h, p) for h in list_hours for p in list_bins], columns=["hour", prob_name])
        plt_df["total_length_km"] = 0
        plt_df["count_entries"] = 0

        # Aggregate data from fltr_exposure
        agg_df = fltr_exposure.groupby(['hour', prob_name]).agg(
            count_entries=('infra', 'size'),
            total_length_km=('length_km', 'sum')
        ).reset_index()

        # Merge aggregated values into base DataFrame
        plt_df = plt_df.merge(agg_df, on=['hour', prob_name], how='left')

        # Overwrite zero values with actuals if available
        plt_df["count_entries"] = plt_df["count_entries_y"].fillna(0)
        plt_df["total_length_km"] = plt_df["total_length_km_y"].fillna(0)

        # Final cleanup
        plt_df = plt_df[["hour", prob_name, "total_length_km", "count_entries"]]

    return plt_df.sort_values(by='hour', ascending=True), geom




def line_plot(fltr_exposure, selected_hour, list_bins, list_hours):
    # --------------------------------------------------------
    # Create and update the plot with lines showing distribution of exposure data during the simulated event
    fig_line = go.Figure()
    yaxis_name = ""  # First item on dropdown menu are line items
    y_max = 1

    # Check if DataFrame is empty
    if len(fltr_exposure) == 0:
        fig_line.update_yaxes(range=[0, y_max])
    else:
        plt_df, geom = create_df_plot(fltr_exposure, list_bins, list_hours)

        if fltr_exposure['geometry_type'].unique() == 'p':
            geom = 'p'
            yaxis_name = "Amount of assets"
            y_max = 1.1 * plt_df['count_entries'].max()
        elif fltr_exposure['geometry_type'].unique() == 'l':
            geom = 'l'
            yaxis_name = "Total length (km)"
            y_max = 1.1 * plt_df['total_length_km'].max()

        valid_probs = plt_df[prob_name].unique()
        for prob_value in valid_probs:
            key = str(int(prob_value))
            color = map_colors.get(key)
            if color is None:
                continue  # skip unknown values

            if geom == 'l':

                plot_data = []
                df_subset = plt_df[plt_df[prob_name] == prob_value]

                if df_subset['total_length_km'].sum() > 0:
                    # Full time domain (dashed)
                    plot_data.append(go.Scatter(
                        x=df_subset['hour'].values,
                        y=df_subset['total_length_km'].values,
                        mode='lines',
                        name=f'Prob {key} (Full)',
                        line=dict(color=color, dash='dash')
                    ))

                    # Plot solid lines with markers for the selected time domain
                    if selected_hour >= 1:

                        df_partial = df_subset[df_subset['hour'] <= selected_hour]
                        if not df_partial.empty:
                            plot_data.append(go.Scatter(
                                x=df_partial['hour'].values,
                                y=df_partial['total_length_km'].values,
                                mode='lines+markers',
                                name=f'Prob {key} (Partial)',
                                line=dict(color=color, dash='solid')
                            ))

                    # Add all traces at once (faster than repeatedly calling add_trace)
                    fig_line.add_traces(plot_data)

            # Plot point data
            if geom == 'p':
                # First: plot dashed lines for the entire time domain
                df_subset = plt_df[plt_df[prob_name] == prob_value]

                if df_subset['count_entries'].sum() > 0:
                    fig_line.add_trace(go.Scatter(
                        x=df_subset['hour'],
                        y=df_subset['count_entries'],
                        mode='lines',
                        # name=f'Prob {prob_value} (Full)',
                        line=dict(color=map_colors[str(int(prob_value))], dash='dash')
                    ))

                    # Plot solid lines with markers for the selected time domain
                    if selected_hour >= 1:
                        df_subset = df_subset[df_subset['hour'] <= selected_hour]
                        fig_line.add_trace(go.Scatter(
                            x=df_subset['hour'],
                            y=df_subset['count_entries'],
                            mode='lines+markers',
                            line=dict(color=map_colors[str(int(prob_value))], dash='solid')
                        ))

        # Update layout
        fig_line.update_layout(
            title="",
            xaxis_title="Hour",
            yaxis_title=yaxis_name,
            legend_title="",
            template="plotly_white",
            showlegend=False,
            xaxis=dict(range=[1, 9.15]),
            yaxis=dict(range=[0, y_max]),
            margin=dict(t=20, b=10, r=10, l=20)
        )

        return fig_line
