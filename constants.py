# file with raw data
INPUT_FILE: str = "altitudes.txt"

# area to display on earth [lat-, lat+, lon-, lon+]
EARTH_AREA = [45, 47.5, 5, 7.5]

# file used to store pre-computed data
VTK_PRE_COMPUTED_FILE: str = "map.vtk"

# in [m]
EARTH_RADIUS: int = 6371009

# elevation in [m]
SEA_LEVEL: int = 0

# in cells, don't know exactly which area it is, comes from trial and error
MIN_LAKE_AREA: int = 200

# for usage in the transfer color function
LAKE_FAKE_ELEVATION: int = -1

# elevation 0, lon 6.25 lat 46.25
FOCAL_POINT = [501_025, 4_405_635, 4_574_833]

# elavation 300km, lon 6.25 lat 46.25
CAMERA_POSITION = [524_618, 4_613_089, 4_790_254]