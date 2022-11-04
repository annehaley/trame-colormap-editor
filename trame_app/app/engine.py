from .vtk_pipeline import VtkPipeline
import logging
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


DEFAULT_COLOR_MAP = [
    [15, 0, 0, 0],
    [75, 0, 1, 0],
    [100, 1, 0, 0],
    [175, 0, 0, 1],
]


DEFAULT_OPACITY_MAP = [
    [0, 0],
    [100, 0.2],
    [190, 0.7],
    [200, 1],
    [255, 1],
]


# ---------------------------------------------------------
# Server binding
# ---------------------------------------------------------
def initialize(server):
    state, ctrl = server.state, server.controller
    state.trame__title = "Colormap Editor"
    state.colormap_points = DEFAULT_COLOR_MAP
    state.opacity_points = DEFAULT_OPACITY_MAP

    skull_vti = Path("trame_app/data/skull.vti")
    print(skull_vti.absolute())
    vtk_pipeline = VtkPipeline(skull_vti.absolute())
    state.histogram_data = vtk_pipeline.get_histogram_data(buckets=10)

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
