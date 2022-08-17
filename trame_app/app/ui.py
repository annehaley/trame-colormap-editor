from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify
from trame.widgets import vtk as trame_vtk

from trame.app import get_server
from trame_app.widgets import ColormapEditor

from vtkmodules import all as vtk

server = get_server()
state, ctrl = server.state, server.controller


def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "Colormap Editor"
    color_function_points = state.colormap_points
    opacity_function_points = state.opacity_points

    torso_vti = "/home/anne/data/torso.vti"
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(torso_vti)
    reader.Update()
    mapper = vtk.vtkFixedPointVolumeRayCastMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    scalar_data_source = reader.GetOutput().GetPointData().GetScalars()
    scalar_data = [
        scalar_data_source.GetValue(i) for i in range(scalar_data_source.GetSize())
    ]
    print(len(scalar_data), "scalar data computed")

    color_function = vtk.vtkColorTransferFunction()
    for point in color_function_points:
        color_function.AddRGBPoint(*point)

    opacity_function = vtk.vtkPiecewiseFunction()
    for point in opacity_function_points:
        opacity_function.AddPoint(*point)

    volume_property = vtk.vtkVolumeProperty()
    volume_property.SetColor(color_function)
    volume_property.SetScalarOpacity(opacity_function)
    # volumeProperty.SetInterpolationTypeToLinear()

    actor = vtk.vtkVolume()
    actor.SetProperty(volume_property)
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
                    # scalar_data=scalar_data,
                    v_model="colormap_points",
                )

        # Main content
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                html_view = trame_vtk.VtkLocalView(renderWindow)
                ctrl.on_server_ready.add(html_view.update)

        # Footer
        layout.footer.hide()
