# LizardNet-Minecraft/Overviewer-Config
This repository contains the configuration files used to render the maps for the LizardNet Minecraft servers. The maps
are rendered using [Overviewer](https://overviewer.org/). Likewise, this is primarily for internal use, but the code is
published to allow for easy collaboration and version control.

This repository primarily lives in LizardNet Code Review:
- [View repository][gitblit]
- [View Gerrit dashboard][gerrit]

It also is mirrored to GitHub as [LizardNet/LizardNet-Minecraft-Overviewer-Config][github] for convenience. Note that
the mirror is read-only (or, more accurately, unidirectional from Gerrit to GitHub), so changes cannot be directly
pushed. Pull requests are welcome, but need to be copied by an admin to Gerrit after merging.

The repository is heavily based on code by stwalkerster, adapted for use on LizardNet, which can be found at
[stwalkerster/minecraft-overviewer][github-stwalkerster-minecraft-overviewer].

## Example usage
This configuration is used to generate the maps for the LizardNet Minecraft servers; for example, the [maps for server
s2][lizardnet-s2-maps] are generated using this configuration.

## Environment
This config is used in a Jenkins job that periodically builds the maps. The job copies the Minecraft server world data
into the Jenkins workspace, then calls the [`mapgen` script](/mapgen) to render the map itself (i.e., the raster images
of the Minecraft world). After this, it calls the [`poigen` script](/poigen) to generate the points-of-interest (POI)
markers that are superimposed on the map. The `poigen` script also handles copying the `icons` directory into the map's
web root (i.e., the output directory). (Overviewer itself handles syncing the `assets` directory to the web root.)

Both `mapgen` and `poigen` invoke Overviewer with the [`config.py` script](/config.py) as the configuration file, which
in turns calls helper functions from [`common.py`](/common.py). This is where the real core of the configuration lies.

Jenkins makes the following environment variables available in all parts of the configuration:
- `WORKSPACE`: The path to the Jenkins workspace directory holding general working data. This is generally where this
  repository is cloned to.
- `MINECRAFT_TEXTURE_REFERENCE_VERSION`: The client version of Minecraft the job should download to use as a reference
  for the texture pack. This is generally set to the latest version of Minecraft that the server is running.
- `MINECRAFT_WORLD_STAGING`: The path to the directory holding the Minecraft server world data. This may be the same as
  `WORKSPACE`, or may be a different value entirely, perhaps even on a different filesystem. Each server's data is
  downloaded to its own subdirectory within this directory.
- `OVERVIEWER_OUTPUT_DIRECTORY`: The web root where Overviewer is to output files. The map is available in browsers by
  navigating to `index.html` within this directory. This generally won't be the same as `WORKSPACE` or within
  `WORKSPACE`. This will be a different unique directory for each server being rendered.
- `GERRIT_REFSPEC`: A Git refspec referencing the [Gerrit repository][gitblit] that you're looking at now! This is used
  by Jenkins to determine what version of the configuration it should use. Generally this is the value
  `refs/heads/main`, though it can be set to a different value on a one-off basis to test in-review changes (e.g.,
  `refs/changes/63/463/1`)
- `RUN_MAPGEN`: Either the string `"true"` or the string `"false"`. If `"true"`, the `mapgen` script will be run. If
  `"false"`, it will not be run. This is used to allow for one-off runs of the `poigen` script without having to run
  `mapgen` first. This is controlled by the Jenkins job, not by the scripts in this repo.
- `RUN_POIGEN`: Either the string `"true"` or the string `"false"`. If `"true"`, the `poigen` script will be run. If
  `"false"`, it will not be run. This is used to allow for one-off runs of the `mapgen` script without having to run
  `poigen` after. This is controlled by the Jenkins job, not by the scripts in this repo.

In addition, the `mapgen` and `poigen` scripts set the `IN_MAPGEN` and `IN_POIGEN` environment variables, respectively,
to a value of `1` to indicate the phase that the job is running in, which is used in the configuration files to tailor
phase-specific behavior. They should never be `1` at the same time.

[gitblit]: <https://git.fastlizard4.org/gitblit/summary/?r=LizardNet-Minecraft/Overviewer-Config.git>
[gerrit]: <https://gerrit.fastlizard4.org/r/admin/repos/LizardNet-Minecraft/Overviewer-Config>
[github]: <https://github.com/LizardNet/LizardNet-Minecraft-Overviewer-Config>
[github-stwalkerster-minecraft-overviewer]: <https://github.com/stwalkerster/minecraft-overviewer>
[lizardnet-s2-maps]: <https://mcmaps.fastlizard4.org/s2/>
