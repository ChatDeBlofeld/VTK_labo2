import vtk
from constants import *

def MakeLUTFromCTF(tableSize):
    '''
    Use a color transfer Function to generate the colors in the lookup table.
    See: http://www.vtk.org/doc/nightly/html/classvtkColorTransferFunction.html
    :param: tableSize - The table size
    :return: The lookup table.
    '''
    ctf = vtk.vtkColorTransferFunction()
    ctf.SetColorSpaceToDiverging()
    # Green to tan.
    ctf.AddRGBPoint(400, 0.085, 0.532, 0.201)
    ctf.AddRGBPoint(700, 0.865, 0.865, 0.865)
    ctf.AddRGBPoint(1000, 0.677, 0.492, 0.093)

    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(tableSize)
    lut.Build()

    for i in range(0,tableSize):
        rgb = list(ctf.GetColor(float(i)/tableSize))+[1]
        lut.SetTableValue(i,rgb)

    return lut


# import stuff

grid = vtk.vtkStructuredGrid()

reader = vtk.vtkStructuredGridReader()
reader.SetFileName(VTK_PRE_COMPUTED_FILE)
reader.SetOutput(grid)
reader.ReadAllScalarsOn()
reader.ReadAllVectorsOn()
reader.Update()

# Display stuff

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