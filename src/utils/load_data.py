import json
import geopandas as gpd
import pandas as pd
import numpy as np
#from geopandas.io.file import read_file
#from tifffile.tifffile import unique_strings

from src.config import infra_dictionary, prob_name, prob_bin_count

# Convert GeoDataFrame to GeoJSON
def gdf_to_geojson(gdf):
    return json.loads(gdf.to_json())

#TODO: why does this run 4 times?
#TODO: why does this run 4 times?
def read_geojson_inputdata():
    # Read Data: polygons of burned area
    gdf = gpd.read_file(f'data/ppm_plygn_merged_bins_{prob_bin_count}.geojson').to_crs(epsg=4326)
    list_bins = gdf[prob_name].unique()
    list_hours = gdf['hour'].unique()

    # Read Data: exposure data
    exposure_data = gpd.read_file(f'data/exposure_data_overlay_bins_{prob_bin_count}.geojson').to_crs(epsg=4326)
    full_exposure_data = gpd.read_file('data/exposure_data_complete.geojson').to_crs(epsg=4326)

    # Add a new column 'geometry_type' to store 'p' for Point/MultiPoint and 'l' for LineString/MultiLineString
    exposure_data['geometry_type'] = exposure_data['geometry'].apply(
        lambda x: 'p' if x.geom_type in ['Point', 'MultiPoint'] else 'l' if x.geom_type in ['LineString',
                                                                                            'MultiLineString'] else None)
    print(f"bins: {gdf[prob_name].unique()}")
    # Unique infrastructure types
    infra_list = exposure_data['infra'].unique()
    if len(full_exposure_data) > 0:
        infra_list = np.append(infra_list, "complete_db")

    # Convert to DataFrame
    infra_df = pd.DataFrame(exposure_data['infra'].unique(), columns=['infra'])

    infra_map = pd.DataFrame(columns=['infra', 'name'])

    keys_list = list(infra_dictionary.keys())
    for i in infra_list:

        # Find index of 'rural_roads'
        if i in keys_list:
            index = keys_list.index(i)  # Get index
            key = keys_list[index]  # Get key
            value = infra_dictionary[key]  # Get value

            # Append to DataFrame
            infra_map.loc[len(infra_map)] = [key, value]

    return gdf, infra_df, exposure_data, full_exposure_data, infra_map, list_bins, list_hours