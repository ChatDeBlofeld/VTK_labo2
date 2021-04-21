

import vtk
import math


# in [m]
EARTH_RADIUS: int = 6371009

def toCartesian(azimuth: float, inclination: float, elevation):
    # x = r*sin(phi)*cos(theta), y = r*sin(phi)*sin(theta), z = r*cos(phi). 
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
        for j in range(rows):
            elevations = (int(x) for x in file.readline().strip().split(" "))
            for i, elevation in enumerate(elevations):
                # Missing elevation attribute somewhere
                (x,y,z) = toCartesian(lon_begin + i * azimuth_offset, lat_begin + j * inclination_offset, EARTH_RADIUS + elevation)
                points.InsertNextPoint(x , y, z)

        grid = vtk.vtkStructuredGrid()
        grid.SetDimensions(rows, cols, 1)
        grid.SetPoints(points)

        return grid


grid = parse("altitudes.txt", 45, 47.5, 5, 7.5)

mapper = vtk.vtkDataSetMapper()
mapper.SetInputData(grid)

gridActor = vtk.vtkActor()
gridActor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(gridActor)
renderer.SetBackground(0.1, 0.2, 0.4)

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(300, 300)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()
iren.Start()
