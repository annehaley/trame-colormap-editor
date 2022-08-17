r"""
Define your classes and create the instances that you need to expose
"""
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
# Engine class
# ---------------------------------------------------------
class MyEngine:
    def __init__(self, server):
        self._server = server
        state, ctrl = server.state, server.controller
        state.colormap_points = DEFAULT_COLOR_MAP
        state.opacity_points = DEFAULT_OPACITY_MAP
        ctrl.reset_colormap_points = self.reset_colormap_points

    def reset_colormap_points(self):
        self._server.state.colormap_points = DEFAULT_COLOR_MAP


# ---------------------------------------------------------
# Server binding
# ---------------------------------------------------------
def initialize(server):
    state = server.state

    @state.change("colormap_points")
    def colormap_points_changed(colormap_points, **kwargs):
        logger.info(f">>> Colormap points changed to {colormap_points}")

    engine = MyEngine(server)
    return engine
