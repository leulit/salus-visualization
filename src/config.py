# Column nane with the binned probabilities
prob_name = 'prob_bin'

# Pre-select infrastructure list
selected_infra = 1

# Define number of bins of the propagation probability should be visualized 3 or 4
# at the moment only prob_bin_count = 4 works
prob_bin_count = 4

# Define a colormap:
map_colors = {
    "-1": "#9be3ff",
     "0": "#fff279",
    "25": "#ffb488",
    "50": "#ff5441",
    "75": "#990709"
}
if prob_bin_count == 3:
    map_colors = {
        "-1": "#9be3ff",
         "0": "#fff279",
        "33": "#ff5441",
        "66": "#990709"
    }

# map_colors = {
#     "-1":	"#9be3ff",
#      "0":   "#fff279",
#     "33":	"#ffa771",
#     "66":	"#ff5d4b",
#     "75":	"#f40b13"
# }
#
# Define the URL, label, and credits of basemap layers
basemaps = {
    "pnoa_lidar": {"url": "https://wmts-mapa-lidar.idee.es/lidar?SERVICE=WMTS&REQUEST=GetTile&VERSION=1.0.0&LAYER=EL.GridCoverageDSM&TILEMATRIXSET=GoogleMapsCompatible&TILEMATRIX={z}&TILEROW={y}&TILECOL={x}&FORMAT=image/png",
                   "credits": "© Instituto Geográfico Nacional de España, PNOA, IDEE",
                   "dropdown_label": "PNOA Lidar"
    },
    "openstreetmap": {"url": "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png",
                      "credits": "© OpenStreetMap contributors, https://www.openstreetmap.org/copyright",
                      "dropdown_label": "OpenStreetMap"
    },
    "esri_world_imagery": {"url": "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}",
                           "credits": "Earthstar Geographics - Instituto Geográfico Nacional, Esri, TomTom, Garmin, FAO, NOAA, USGS, © Powered by Esri",
                           "dropdown_label": "ESRI World Imagery"
    },
}

# Dropdown dictionary
infra_dictionary = {
    "complete_network_roads" : "Complete road network",
    "rural_roads" : "Rural roads",
    "power_pnts_towers" : "Electricity towers",
    "power_pnts_infra" : "Electricity infrastructure",
    "power_pnts_generation" : "Electricity generation",
    "power_lines" : "Electricity network",
    "complete_network_railway" : "Railway network",
    "active_network_railway" : "Active railway network",
    "emergencyservices_amenity" : "Emergency services",
    "buildings_pnts_final" : "Buildings",
    "place_pnts" : "Local dwellings with buildings",
    "complete_db" : "Complete exposure database"
}

