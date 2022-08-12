from pathlib import Path

# Compute local path to serve
serve_path = str(Path(__file__).with_name("serve").resolve())

# Serve directory for JS/CSS files
serve = {"__trame_app": serve_path}

# List of JS files to load (usually from the serve path above)
scripts = ["__trame_app/vue-trame_app.umd.min.js"]

# List of CSS files to load (usually from the serve path above)
styles = ["__trame_app/vue-trame_app.css"]

vuetify_config = {}

# List of Vue plugins to install/load
vue_use = ["trame_app", ("trame_vuetify", vuetify_config)]

# Uncomment to add entries to the shared state
# state = {}


# Optional if you want to execute custom initialization at module load
def setup(app, **kwargs):
    """Method called at initialization with possibly some custom keyword arguments"""
    pass
