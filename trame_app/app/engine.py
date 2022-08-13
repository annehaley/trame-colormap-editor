r"""
Define your classes and create the instances that you need to expose
"""
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


# ---------------------------------------------------------
# Engine class
# ---------------------------------------------------------
class MyEngine:
    def __init__(self, server):
        self._server = server
        state, ctrl = server.state, server.controller
        state.colormap_points = [[0, 1, 1, 1]]
        ctrl.reset_colormap_points = self.reset_colormap_points

    def reset_colormap_points(self):
        self._server.state.colormap_points = [[0, 1, 1, 1]]


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
