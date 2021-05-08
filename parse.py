import vtk
import math
from constants import *
# pip install -r requirements.txt
import numpy as np
from skimage import measure, morphology

def get_elevations_with_lakes(grid):
    '''
    BY THE POWER OF DATA SCIENCE [INSERT EXTREMELY VULGAR EXCLAMATION OF JOY OF YOUR CHOICE]
    '''

    # rip RAM
    grid = grid.copy()
    # defines regions with same elevation
    labels = measure.label(grid, connectivity=1)
    # removes too small regions
    mask = morphology.remove_small_objects(labels, MIN_LAKE_AREA) > 0
    # Use an arbitrary value to represent water
    grid[mask] = LAKE_FAKE_ELEVATION
    return grid

def toCartesian(azimuth: float, inclination: float, elevation):
    '''
    Transform spherical coord to cartesian coords.
    Uses physics' world conventions about what azimuth and inclination means
    '''
    azimuth = math.radians(azimuth)
    inclination = math.radians(inclination)
    x = elevation * math.sin(inclination) * math.sin(azimuth)
    y = elevation * math.cos(inclination)
    z = elevation * math.sin(inclination) * math.cos(azimuth)
    return x,y,z

def parse(filename: str, lat_begin: float, lat_end: float, lon_begin: float, lon_end: float):
    '''
    Parse an altitude file to a Structured Grid object with elevation attributes

    A structured grid seems to be the best choice since a point is only stored once and
    we don't have to care about topology since continus points are already binded
    '''
    with open(filename) as file:
        rows, cols = (int(x) for x in file.readline().strip().split(" "))

        # Angle between each coord
        inclination_offset = (lat_end - lat_begin) / (rows - 1)
        azimuth_offset = (lon_end - lon_begin) / (cols - 1)

        # Will store the points of the geometry
        points = vtk.vtkPoints()
        # Will store the attributes of the above points
        attributes = vtk.vtkIntArray()

        # Reading data
        raw_elevations = np.array([[int(x) for x in file.readline().strip().split(" ")] for i in range(rows)])
        # Remove relief below sea level
        raw_elevations[raw_elevations < SEA_LEVEL] = SEA_LEVEL
        # Same data with lake areas indications (attributes)
        raw_elevations_with_lakes = get_elevations_with_lakes(raw_elevations)

        for j, elevations in enumerate(raw_elevations):
            for i, elevation in enumerate(elevations):
                # Since with make an approximation of the eath with a perfect sphere,
                # we can convert spherical to cartesian coords
                (x,y,z) = toCartesian(lon_begin + i * azimuth_offset, lat_begin + j * inclination_offset, EARTH_RADIUS + elevation)
                points.InsertNextPoint(x , y, z)
                attributes.InsertNextValue(raw_elevations_with_lakes[j,i])

        # Create grid
        grid = vtk.vtkStructuredGrid()
        grid.SetDimensions(rows, cols, 1)
        grid.SetPoints(points)
        grid.GetPointData().SetScalars(attributes)     

        return grid


grid = parse(INPUT_FILE, *EARTH_AREA)

# Export grid
writer = vtk.vtkStructuredGridWriter()
writer.SetFileName(VTK_PRE_COMPUTED_FILE )
writer.SetFileTypeToBinary()
writer.SetInputData(grid)
writer.Write()