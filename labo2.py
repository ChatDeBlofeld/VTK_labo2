import vtk
from constants import *

# import stuff

grid = vtk.vtkStructuredGrid()

reader = vtk.vtkStructuredGridReader()
reader.SetFileName(VTK_PRE_COMPUTED_FILE)
reader.SetOutput(grid)
reader.ReadAllScalarsOn()
reader.Update()

# Display stuff


# Our transfer function. It was quite a long process of trial and error 
# to know how many points to add, at which elevations and especially 
# which colors to choose but we really like the result.
ctf = vtk.vtkColorTransferFunction()
ctf.AddRGBPoint(0, 0.514, 0.49, 1)
ctf.AddRGBPoint(1, 0.157, 0.325, 0.141)
ctf.AddRGBPoint(400, 0.392, 0.725, 0.357)
ctf.AddRGBPoint(800, 0.898, 0.784, 0.537)
ctf.AddRGBPoint(1600, 1, 1, 1)

mapper = vtk.vtkDataSetMapper()
mapper.SetInputData(grid)
mapper.SetLookupTable(ctf)

gridActor = vtk.vtkActor()
gridActor.SetMapper(mapper)

renderer = vtk.vtkRenderer()
renderer.AddActor(gridActor)
renderer.GetActiveCamera().SetFocalPoint(*FOCAL_POINT)
renderer.GetActiveCamera().SetPosition(*CAMERA_POSITION)
renderer.GetActiveCamera().SetClippingRange(0.1, 1_000_000) 

renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(800, 800)

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)

style = vtk.vtkInteractorStyleTrackballCamera()
iren.SetInteractorStyle(style)

iren.Initialize()
iren.Render()
iren.Start()