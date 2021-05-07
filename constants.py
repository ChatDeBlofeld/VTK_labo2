# file with raw data
INPUT_FILE = "altitudes.txt"

# area to display on earth [lat-, lat+, lon-, lon+]
EARTH_AREA = [45, 47.5, 5, 7.5]

# file used to store pre-computed data
VTK_PRE_COMPUTED_FILE = "map.vtk"

# in [m]
EARTH_RADIUS: int = 6371009

# in cells, don't know exactly which area it is, comes from trial and error
MIN_LAKE_AREA = 200

# for usage in the transfer color function
LAKE_FAKE_ELEVATION = -1