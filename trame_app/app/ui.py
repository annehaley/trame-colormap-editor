from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify
from trame.widgets import vtk as trame_vtk

from trame.app import get_server
from trame_app.widgets import ColormapEditor

from vtkmodules import all as vtk

server = get_server()
state, ctrl = server.state, server.controller


colorFunctionPoints = [
    [-3000, 0, 0, 0],
    [-2000, 1, 0, 0],
    [-1000, 0, 1, 0],
    [0, 0, 0, 1],
    [1000, 1, 0, 1],
    [2000, 1, 1, 0],
    [3000, 0, 1, 1],
    [4000, 1, 1, 1],
]


def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "Colormap Editor"

    torso_vti = "/home/anne/data/torso.vti"
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(torso_vti)
    reader.Update()
    mapper = vtk.vtkFixedPointVolumeRayCastMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    print(reader.GetOutput().GetScalarRange())

    colorFunction = vtk.vtkColorTransferFunction()
    for point in colorFunctionPoints:
        colorFunction.AddRGBPoint(*point)

    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.SetColor(colorFunction)
    # volumeProperty.SetInterpolationTypeToLinear()

    actor = vtk.vtkVolume()
    actor.SetProperty(volumeProperty)
    actor.SetMapper(mapper)
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderer.AddVolume(actor)
    renderer.ResetCamera()

    with SinglePageWithDrawerLayout(server) as layout:
        layout.title.set_text("Colormap Editor WIP")

        with layout.drawer:
            with vuetify.VContainer(classes="pa-5"):
                ColormapEditor(
                    scalar_data="Hewwo World",
                    v_model="colormap_points",
                )

        # Main content
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                html_view = trame_vtk.VtkLocalView(renderWindow)
                ctrl.on_server_ready.add(html_view.update)

        # Footer
        layout.footer.hide()
