from trame_client.widgets.core import AbstractElement
from . import module


class HtmlElement(AbstractElement):
    def __init__(self, _elem_name, children=None, **kwargs):
        super().__init__(_elem_name, children, **kwargs)
        if self.server:
            self.server.enable_module(module)


# Expose your vue component(s)
class ColormapEditor(HtmlElement):
    def __init__(self, **kwargs):
        super().__init__(
            "colormap-editor",
            **kwargs,
        )
        self._attr_names += [
            ("histogram_data", "histogramData"),
            "colors",
            "opacities",
            "dark",
        ]
        self._event_names += [
            ("update_colors", "updateColors"),
            ("update_opacities", "updateOpacities"),
        ]
