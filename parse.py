import vtk
import math
from constants import *
# pip install -r requirements.txt
import numpy as np
from skimage import measure, morphology

def get_elevations_with_lakes(grid):
    # BY THE POWER OF DATA SCIENCE [INSERT EXTREMELY VULGAR EXCLAMATION OF JOY OF YOUR CHOICE]
    grid = grid.copy() # rip RAM
    labels = measure.label(grid, connectivity=1)
    mask = morphology.remove_small_objects(labels, MIN_LAKE_AREA) > 0
    grid[mask] = LAKE_FAKE_ELEVATION
    return grid

def toCartesian(azimuth: float, inclination: float, elevation):
    azimuth = math.radians(azimuth)
    inclination = math.radians(inclination)
    x = elevation * math.sin(inclination) * math.cos(azimuth)
    y = elevation * math.sin(inclination) * math.sin(azimuth)
    z = elevation * math.cos(inclination)
    return x,y,z

def parse(filename: str, lat_begin: float, lat_end: float, lon_begin: float, lon_end: float):
    with open(filename) as file:
        rows, cols = (int(x) for x in file.readline().strip().split(" "))
        inclination_offset = (lat_end - lat_begin) / (rows - 1)
        azimuth_offset = (lon_end - lon_begin) / (cols - 1)

        points = vtk.vtkPoints()
        attributes = vtk.vtkIntArray()

        raw_elevations = np.array([[int(x) for x in file.readline().strip().split(" ")] for i in range(rows)])
        raw_elevations_with_lakes = get_elevations_with_lakes(raw_elevations)

        for j, elevations in enumerate(raw_elevations):
            for i, elevation in enumerate(elevations):
                (x,y,z) = toCartesian(lon_begin + i * azimuth_offset, lat_begin + j * inclination_offset, EARTH_RADIUS + elevation)
                points.InsertNextPoint(x , y, z)
                attributes.InsertNextValue(raw_elevations_with_lakes[j,i])

        grid = vtk.vtkStructuredGrid()
        grid.SetDimensions(rows, cols, 1)
        grid.SetPoints(points)
        grid.GetPointData().SetScalars(attributes)     

        return grid


grid = parse(INPUT_FILE, *EARTH_AREA)

# Export grid
writer = vtk.vtkStructuredGridWriter()
writer.SetFileName(VTK_PRE_COMPUTED_FILE )
writer.SetFileTypeToASCII()
writer.SetInputData(grid)
writer.Write()