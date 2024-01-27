import os
import sys

sys.path.append(os.environ.get("WORKSPACE"))

from collections import OrderedDict

from .observer import JSObserver, MultiplexingObserver, LoggingObserver
from common import (
    overworld_marker_definitions,
    nether_marker_definitions,
    end_marker_definitions,
)

worlds = OrderedDict()
renders = OrderedDict()

world_name_map = {
    "s2": "Bob",
}

server_id = os.environ.get("SERVER")
world_name = world_name_map[server_id]

worlds[world_name] = (
    os.environ.get("MINECRAFT_WORLD_STAGING") + f"/{server_id}/{world_name}"
)
worlds[f"{world_name}_nether"] = (
    os.environ.get("MINECRAFT_WORLD_STAGING") + f"/{server_id}/{world_name}_nether"
)
worlds[f"{world_name}_the_end"] = (
    os.environ.get("MINECRAFT_WORLD_STAGING") + f"/{server_id}/{world_name}_the_end"
)

outputdir = os.environ.get("OVERVIEWER_OUTPUT_DIRECTORY")
customwebassets = os.environ.get("WORKSPACE") + "/assets"

if os.environ.get("IN_MAPGEN", 0):
    observer_list = [LoggingObserver(), JSObserver(outputdir=outputdir, minrefresh=10)]
else:
    observer_list = [LoggingObserver()]

observer = MultiplexingObserver(*observer_list)


renders["myrender"] = {
    "world": world_name,
    "title": f"LizardNet Minecraft Server {server_id} Overworld",
    "markers": overworld_marker_definitions(),
    "rendermode": "smooth_lighting",
    "dimension": "overworld",
    "imgformat": "jpeg",
    "imgquality": 90
    # "optimizeimg": [optipng(olevel=3)]
}

renders["myrender_night"] = {
    "world": world_name,
    "title": f"LizardNet Minecraft Server {server_id} Overworld (nighttime)",
    "markers": overworld_marker_definitions(),
    "rendermode": "smooth_night",
    "dimension": "overworld",
    "imgformat": "jpeg",
    "imgquality": 90
    # "optimizeimg": [optipng(olevel=3)]
}

renders["nether"] = {
    "world": f"{world_name}_nether",
    "title": f"LizardNet Minecraft Server {server_id} NETHER",
    "markers": nether_marker_definitions(),
    "rendermode": "nether",
    "dimension": "nether",
    "imgformat": "jpeg",
    "imgquality": 90
    # "optimizeimg": [optipng(olevel=3)]
}

renders["the_end"] = {
    "world": f"{world_name}_the_end",
    "title": f"LizardNet Minecraft Server {server_id} THE END",
    "markers": end_marker_definitions(),
    "rendermode": "normal",
    "dimension": "end",
    "imgformat": "jpeg",
    "imgquality": 90
    # "optimizeimg": [optipng(olevel=3)]
}

renders["biomeoverlay"] = {
    "world": world_name,
    "rendermode": [ClearBase(), BiomeOverlay()],
    "title": "Biome Coloring Overlay",
    "overlay": ["myrender"],
    "dimension": "overworld",
    "imgformat": "jpeg",
    "imgquality": 90
    # "optimizeimg": [optipng(olevel=3)]
}
