import vtk

# import stuff
grid = vtk.vtkStructuredGrid()

reader = vtk.vtkStructuredGridReader()
reader.SetFileName("map.vtk")
reader.SetOutput(grid)
reader.ReadAllScalarsOn()
reader.ReadAllVectorsOn()
reader.Update()


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