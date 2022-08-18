from .vtk_pipeline import VtkPipeline
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DEFAULT_COLOR_MAP = [
    [-3000, 0, 0, 0],
    [-2000, 1, 0, 0],
    [-1000, 0, 1, 0],
    [0, 0, 0, 1],
    [1000, 1, 0, 1],
    [2000, 1, 1, 0],
    [3000, 0, 1, 1],
    [4000, 1, 1, 1],
]


DEFAULT_OPACITY_MAP = [
    [-3000, 0],
    [0, 0.01],
    [2000, 0.5],
    [4000, 1],
]


# ---------------------------------------------------------
# Server binding
# ---------------------------------------------------------
def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "Colormap Editor"
    state.histogram_data = []
    state.colormap_points = DEFAULT_COLOR_MAP
    state.opacity_points = DEFAULT_OPACITY_MAP

    torso_vti = "/home/anne/data/torso.vti"
    vtk_pipeline = VtkPipeline(torso_vti)

    @state.change("colormap_points")
    def update_colors(colormap_points, **kwargs):
        vtk_pipeline.update_colors(colormap_points)
        ctrl.view_update()

    @state.change("opacity_points")
    def update_opacity(opacity_points, **kwargs):
        vtk_pipeline.update_opacity(opacity_points)
        ctrl.view_update()

    @ctrl.set("get_render_window")
    def get_render_window():
        return vtk_pipeline.render_window

    @ctrl.set("reset_colormap_points")
    def reset_colormap_points(self):
        self._server.state.colormap_points = DEFAULT_COLOR_MAP
