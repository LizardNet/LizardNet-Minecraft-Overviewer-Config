import os
from .observer import JSObserver, MultiplexingObserver, LoggingObserver
from common import (
    overworld_marker_definitions,
    nether_marker_definitions,
    end_marker_definitions,
)

worlds = dict()
renders = dict()

worldNameMap = {
    "s2": "Bob",
}

serverId = os.environ.get("SERVER")
worldName = worldNameMap[serverId]

worlds[worldName] = (
    os.environ.get("MINECRAFT_WORLD_STAGING") + f"/{serverId}/{worldName}"
)
worlds[f"{worldName}_nether"] = (
    os.environ.get("MINECRAFT_WORLD_STAGING") + f"/{serverId}/{worldName}_nether"
)
worlds[f"{worldName}_the_end"] = (
    os.environ.get("MINECRAFT_WORLD_STAGING") + f"/{serverId}/{worldName}_the_end"
)

outputdir = os.environ.get("OVERVIEWER_OUTPUT_DIRECTORY")
customwebassets = os.environ.get("WORKSPACE") + "/assets"

observer = MultiplexingObserver(
    LoggingObserver(), JSObserver(outputdir=outputdir, minrefresh=10)
)


renders["myrender"] = {
    "world": worldName,
    "title": f"LizardNet Minecraft Server {serverId} Overworld",
    "markers": overworld_marker_definitions(),
    "rendermode": "smooth_lighting",
    "dimension": "overworld",
    "imgformat": "jpeg",
    "imgquality": 90
    # "optimizeimg": [optipng(olevel=3)]
}

renders["myrender_night"] = {
    "world": worldName,
    "title": f"LizardNet Minecraft Server {serverId} Overworld (nighttime)",
    "markers": overworld_marker_definitions(),
    "rendermode": "smooth_night",
    "dimension": "overworld",
    "imgformat": "jpeg",
    "imgquality": 90
    # "optimizeimg": [optipng(olevel=3)]
}

renders["nether"] = {
    "world": f"{worldName}_nether",
    "title": f"LizardNet Minecraft Server {serverId} NETHER",
    "markers": nether_marker_definitions(),
    "rendermode": "nether",
    "dimension": "nether",
    "imgformat": "jpeg",
    "imgquality": 90
    # "optimizeimg": [optipng(olevel=3)]
}

renders["the_end"] = {
    "world": f"{worldName}_the_end",
    "title": f"LizardNet Minecraft Server {serverId} THE END",
    "markers": end_marker_definitions(),
    "rendermode": "normal",
    "dimension": "end",
    "imgformat": "jpeg",
    "imgquality": 90
    # "optimizeimg": [optipng(olevel=3)]
}

renders["biomeoverlay"] = {
    "world": worldName,
    "rendermode": [ClearBase(), BiomeOverlay()],
    "title": "Biome Coloring Overlay",
    "overlay": ["myrender"],
    "dimension": "overworld",
    "imgformat": "jpeg",
    "imgquality": 90
    # "optimizeimg": [optipng(olevel=3)]
}
