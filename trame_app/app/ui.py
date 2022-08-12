from trame.ui.vuetify import SinglePageWithDrawerLayout
from trame.widgets import vuetify
from trame.widgets import vtk as trame_vtk

from trame.app import get_server
from trame_app.widgets import trame_app as my_widgets

from vtkmodules import all as vtk

server = get_server()
state, ctrl = server.state, server.controller


def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "Colormap Editor"

    torso_vti = "/home/anne/data/torso.vti"
    reader = vtk.vtkXMLImageDataReader()
    reader.SetFileName(torso_vti)
    reader.Update()
    # cone_source = vtk.vtkConeSource()
    mapper = vtk.vtkFixedPointVolumeRayCastMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtk.vtkVolume()
    actor.SetMapper(mapper)
    renderer = vtk.vtkRenderer()
    renderWindow = vtk.vtkRenderWindow()
    renderWindow.AddRenderer(renderer)
    renderer.AddActor(actor)
    renderer.ResetCamera()

    with SinglePageWithDrawerLayout(server) as layout:
        layout.title.set_text("Colormap Editor WIP")
        # Toolbar
        # with layout.toolbar:

        with layout.drawer:
            with vuetify.VContainer(classes="pa-5"):
                my_widgets.CustomWidget(
                    attribute_name="Hello",
                    py_attr_name="World",
                    click=ctrl.widget_click,
                    change=ctrl.widget_change,
                )
            # vuetify.VSlider(  # Add slider
            #     v_model=("resolution", 6),  # bind variable with an initial value of 6
            #     min=3,
            #     max=60,  # slider range
            #     dense=True,
            #     hide_details=True,  # presentation setup
            # )

        # Main content
        with layout.content:
            with vuetify.VContainer(fluid=True, classes="pa-0 fill-height"):
                html_view = trame_vtk.VtkLocalView(renderWindow)
                ctrl.on_server_ready.add(html_view.update)

        # Footer
        layout.footer.hide()
