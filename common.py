import json
import logging
import datetime
import os

import dateutil.parser
import dateutil.utils

from fasttravel import fast_travel_filter, fast_travel_postprocess


def overworld_marker_definitions():
    markers = [
        dict(name="Players", filterFunction=player_icons, checked=True),
        dict(
            name="Signs",
            filterFunction=fastlizard_sign_filter,
            checked=True,
            icon="signpost_icon.png",
            showIconInLegend=True,
        ),
        dict(
            name="Player bases",
            filterFunction=fastlizard_house_sign_filter,
            icon="custom-icons/player/marker_house.png",
            checked=True,
            showIconInLegend=True,
        ),
        dict(
            name="Fast Travel",
            filterFunction=fast_travel_filter,
            icon="custom-icons/transport/marker_fasttravel.png",
            checked=True,
            showIconInLegend=True,
            postProcessFunction=fast_travel_postprocess,
        ),
        dict(
            name="Railways",
            filterFunction=fastlizard_rail_line_filter,
            icon="custom-icons/transport/marker_train.png",
            checked=False,
            showIconInLegend=True,
            postProcessFunction=fastlizard_rail_line_postprocess
        ),
        dict(
            name="Named mobs",
            filterFunction=named_mob_filter,
            icon="https://mcmaps.fastlizard4.org/ocelot.png",
            checked=False,
            showIconInLegend=True
        ),
        dict(
            name="Graves",
            filterFunction=graves_filter,
            icon="custom-icons/player/marker_headstone.png",
            checked=True,
            showIconInLegend=True
        ),
        dict(
            name="All Allays",
            filterFunction=all_allays_filter,
            icon="custom-icons/marker_allay.png",
            checked=False,
            showIconInLegend=True
        ),
        dict(
            name="mCalendar",
            filterFunction=fastlizard_mcal_filter,
            icon="custom-icons/marker_calendar.png",
            checked=True,
            showIconInLegend=True,
            postProcessFunction=fastlizard_mcal_postprocess
        ),
    ]

    return markers


def nether_marker_definitions():
    return [
        dict(name="Players", filterFunction=player_icons, checked=True),
        dict(
            name="Signs",
            filterFunction=fastlizard_sign_filter,
            checked=True,
            icon="signpost_icon.png",
            showIconInLegend=True,
        ),
        dict(
            name="Player bases",
            filterFunction=fastlizard_house_sign_filter,
            icon="custom-icons/player/marker_house.png",
            checked=True,
            showIconInLegend=True,
        ),
        dict(
            name="Named mobs",
            filterFunction=named_mob_filter,
            icon="https://mcmaps.fastlizard4.org/ocelot.png",
            checked=False,
            showIconInLegend=True
        ),
        dict(
            name="Graves",
            filterFunction=graves_filter,
            icon="custom-icons/player/marker_headstone.png",
            checked=True,
            showIconInLegend=True
        ),
    ]


def nether_roof_marker_definitions():
    return [
        dict(name="Players", filterFunction=player_icons, checked=True),
        dict(
            name="Signs",
            filterFunction=fastlizard_sign_filter,
            checked=True,
            icon="signpost_icon.png",
            showIconInLegend=True,
        ),
        dict(
            name="Named mobs",
            filterFunction=named_mob_filter,
            icon="https://mcmaps.fastlizard4.org/ocelot.png",
            checked=False,
            showIconInLegend=True
        ),
        dict(
            name="Graves",
            filterFunction=graves_filter,
            icon="custom-icons/player/marker_headstone.png",
            checked=True,
            showIconInLegend=True
        ),
    ]


def end_marker_definitions():
    return [
        dict(name="Players", filterFunction=player_icons, checked=True),
        dict(
            name="Portals",
            filterFunction=portal_sign_filter,
            icon="custom-icons/transport/marker_endportal.png",
            checked=True,
            showIconInLegend=True,
        ),
        dict(
            name="Signs",
            filterFunction=fastlizard_sign_filter,
            checked=True,
            icon="signpost_icon.png",
            showIconInLegend=True,
        ),
        dict(
            name="Player bases",
            filterFunction=fastlizard_house_sign_filter,
            icon="custom-icons/player/marker_house.png",
            checked=True,
            showIconInLegend=True,
        ),
        dict(
            name="Named mobs",
            filterFunction=named_mob_filter,
            icon="https://mcmaps.fastlizard4.org/ocelot.png",
            checked=False,
            showIconInLegend=True
        ),
        dict(
            name="Graves",
            filterFunction=graves_filter,
            icon="custom-icons/player/marker_headstone.png",
            checked=True,
            showIconInLegend=True
        ),
    ]


def format_sign(poi, title, note, include_first_line=False):
    try:
        if poi["id"] in ["minecraft:sign", "minecraft:hanging_sign"]:
            poi_type = "hanging" if poi["id"] == "minecraft:hanging_sign" else "normal"

            if "front_text" in poi:
                front_lines = poi["front_text"]["messagesRaw"]
                back_lines = poi["back_text"]["messagesRaw"]
            else:
                front_lines = [poi["Text1Raw"], poi["Text2Raw"], poi["Text3Raw"], poi["Text4Raw"]]
                back_lines = []

            if not include_first_line:
                front_lines = front_lines[1:]

            def trim_blank_lines(lines):
                while "" in lines:
                    if lines[0] == "":
                        lines = lines[1:]
                    elif lines[-1] == "":
                        lines = lines[:-1]
                    else:
                        break
                return lines

            front_lines = trim_blank_lines([json_text_to_html(x) for x in front_lines])
            back_lines = trim_blank_lines([json_text_to_html(x) for x in back_lines])

        else:
            poi_type = "none"
            front_lines = []
            back_lines = []

        hover = list(front_lines)
        hover.append(
            "(" + ", ".join([str(poi["x"]), str(poi["y"]), str(poi["z"])]) + ")"
        )

        title_html = ""
        if title is not None:
            title_html = "<strong>" + title + "</strong><br />"
            hover.insert(0, title)

        info_window_text = title_html
        front_lines_text = ""

        if front_lines:
            # Annoyingly, we need to account here for both the old and new sign formats
            if "front_text" in poi:
                glowing = " mcglow-1" if poi["front_text"]["has_glowing_text"] == 1 else ""
                colour = " mccolor-" + poi["front_text"]["color"]
            else:
                glowing = " mcglow-1" if poi.get("GlowingText", 0) == 1 else ""
                colour = " mccolor-" + poi.get("Color", "black")

            front_lines_text = (
                '<div class="signtext mcpoi-'
                + poi_type
                + colour
                + glowing
                + '">'
                + "<br />".join(front_lines)
                + "</div><br />"
            )
            info_window_text += front_lines_text
        if back_lines:
            # No need to account for the old sign format here, since old signs never have back text.

            back_lines_text = (
                '<div class="signtext mcpoi-' + poi_type
                + " mccolor-" + poi["back_text"]["color"]
                + (" mcglow-1" if poi["back_text"]["has_glowing_text"] == 1 else "")
                + '">'
                + "<br />".join(back_lines)
                + "</div><br />"
            )

            if front_lines_text != back_lines_text:
                # If the text is different front+back, then show both the back too.
                info_window_text += back_lines_text

        coords = (
            "("
            + "X: "
            + str(poi["x"])
            + ", Y: "
            + str(poi["y"])
            + ", Z: "
            + str(poi["z"])
            + ")"
        )
        info_window_text += ("" if note is None else note) + coords
    except KeyError as e:
        print(poi.keys())
        raise e

    return "\n".join([x for x in hover if x]), info_window_text


def global_sign_filter(poi):
    if poi["id"] in ["minecraft:sign", "minecraft:hanging_sign"]:
        return format_sign(poi, "Potato?", None, include_first_line=True)


def get_sign_text(poi):
    if "front_text" in poi:
        front = " ".join(poi["front_text"]["messages"]).strip().lower()
        back = " ".join(poi["back_text"]["messages"]).strip().lower()
    else:
        front = (
            " ".join([poi["Text1"], poi["Text2"], poi["Text3"], poi["Text4"]])
            .strip()
            .lower()
        )
        back = ""

    return front, back, front + " " + back


def sign_explicit_visibility(front, back, char):
    if len(front) > 0 and front[0] == char:
        return True

    if len(back) > 0 and back[0] == char:
        return True

    return False


def fastlizard_sign_filter(poi):
    if poi["id"] in ["minecraft:sign", "minecraft:hanging_sign"]:
        front, back, all_text = get_sign_text(poi)
        sign_type = "Hanging Sign" if poi["id"] == "minecraft:hanging_sign" else "Sign"

        public = "claim" in all_text or "deathpile" in all_text

        is_station = (
            "north line" in all_text
            or "green line" in all_text
            or "east line" in all_text
            or "south line" in all_text
            or "purple line" in all_text
        )

        if all_text == "":
            return None  # Return nothing; sign is private
        elif is_station:
            return None  # should be handled by train filter instead
        elif sign_explicit_visibility(front, back, "#"):
            return None  # Return nothing; sign is private
        elif sign_explicit_visibility(front, back, "@"):
            return format_sign(
                poi, "Public " + sign_type, None, include_first_line=True
            )
        elif public:
            return format_sign(poi, sign_type, None, include_first_line=True)
        else:
            return None  # Return nothing; sign is private


def fastlizard_house_sign_filter(poi):
    if poi["id"] in ["minecraft:sign", "minecraft:hanging_sign"]:
        front, back, all_text = get_sign_text(poi)

        public = "home" in all_text or "house" in all_text or "outpost" in all_text

        if all_text == "":
            return None  # Return nothing; sign is private
        elif sign_explicit_visibility(front, back, "#"):
            return None  # Return nothing; sign is private
        elif public:
            return format_sign(poi, "Player House", None, include_first_line=True)
        else:
            return None  # Return nothing; sign is private


RAIL_MARKER = '#[RAIL]'
RAIL_STATION_MARKER = '#[RAIL STATION]'
RAIL_MARKER_TYPES = {RAIL_MARKER, RAIL_STATION_MARKER}


def fastlizard_rail_line_filter(poi):
    """
    POI filter function for handling rail line overlays.

    This filter function does the per-POI setup for rendering the overlay. This includes parsing the sign data and
    passing the required data in a sensible format on to the postprocess function. This filter func should only return
    valid railway marker data, with anything that's detected as not valid railway marker discarded. We don't draw the
    railway lines here, but we do prepare the station signs for rendering.
    """
    if poi['id'] != 'minecraft:sign':
        return

    # This is new map functionality in 1.20, so we only care about "new" sign formats.
    if 'front_text' in poi and poi['front_text']['messages'][0].strip() in RAIL_MARKER_TYPES:
        marker_side = poi['front_text']
        display_side = poi['back_text']
    elif 'back_text' in poi and poi['back_text']['messages'][0].strip() in RAIL_MARKER_TYPES:
        marker_side = poi['back_text']
        display_side = poi['front_text']
    else:
        return

    marker_type = marker_side['messages'][0].strip()

    try:
        # line 3 is a config line. Either a colour, or a sequence number. Need not be monotonic nor positive.
        config_line = marker_side['messages'][3].strip()

        # pad with slashes to allow omitting trailing slashes
        config_line = f'{config_line}////'

        i, dx, dy, dz, flags, *_ = config_line.split('/')
        dx = int_or_default(dx, 0)
        dy = int_or_default(dy, 0)
        dz = int_or_default(dz, 0)
        sequence = int_or_default(i, 0)
        line_colour = i if int_or_default(i, None) is None else None

        path = ' '.join([marker_side['messages'][1], marker_side['messages'][2]]).strip()

        extra = dict({
            'type': marker_type,
            'path': path,
            'sequence': sequence,
            'colour': line_colour,
            'dx': dx,
            'dy': dy,
            'dz': dz,
            'flags': flags,
        })

        data = dict({
            'extra': extra
        })

        if marker_type == RAIL_STATION_MARKER:
            station_name = ' '.join(display_side['messages']).strip()
            extra['station'] = station_name
            extra['text'] = display_side

        return data
    except Exception as e:
        # Something's gone wrong. This is user-submitted data in a very specific format so it's likely to go
        # horribly wrong at some point. This will log the specific issue and the coordinates of the sign, and
        # just carry on with the next point without killing the render.
        logging.warning("Unable to process rail marker at [%d, %d, %d]: (%s) %s", poi['x'], poi['y'], poi['z'], type(e).__name__, e)


def fastlizard_rail_line_postprocess(pois):
    """
    This function post-processes every dimension's set of railway markers.

    We receive a set of POIs with augmented data from `fastlizard_rail_line_filter(...)` and adapt it into something
    we can render. There's two sorts of POI we can receive - a rail marker, and a station marker.

    All rail and station markers are combined into a single polyline POI per railway line, so this function will
    consume, for example:
        8 RAIL POIs and 2 STATION POIs for line A (total 10)
        16 RAIL POIs and 4 STATION POIs for line B (total 20)
        12 RAIL POIs and 3 STATION POIs for line C (total 15)
    and it will output:
        2 STATION marker POIs and 1 polyline POI consisting of 10 points for line A
        4 STATION marker POIs and 1 polyline POI consisting of 20 points for line B
        3 STATION marker POIs and 1 polyline POI consisting of 15 points for line C

    It will *also* group stations with the identical names together to form a single "interchange" POI.
    """
    lines = dict()

    # Colours apply across an entire line, set these outside of the segment code
    line_colours = dict()
    # Store the current segment for each part of the path
    current_segment = dict()

    raw_station_markers = dict()
    station_markers = []

    def get_segment_name(path_name):
        if path_name not in current_segment:
            current_segment[path_name] = 0

        return f'{path_name}~s{current_segment[path_name]}'


    for poi in sorted(pois, key=lambda x: x['extra']['sequence']):
        if poi['extra']['type'] == RAIL_STATION_MARKER:
            # Stations are rendered twice. Once as a rail waypoint (a polyline point), and once as a station marker.
            # Here we copy the POI and remove the extra data, and pass it on as any other marker.
            # The original copy is still dealt with as a waypoint below.
            station_marker = poi.copy()
            station_name = station_marker['extra']['station']
            if station_name not in raw_station_markers:
                raw_station_markers[station_name] = []
            raw_station_markers[station_name].append(station_marker)

        # End of segment; add this point to the old segment and bump the segment count
        if 'X' in poi['extra']['flags']:
            old_segment_name = get_segment_name(poi['extra']['path'])
            lines[old_segment_name]['points'].append({
                'x': poi['x'] + poi['extra']['dx'],
                'y': poi['y'] + poi['extra']['dy'],
                'z': poi['z'] + poi['extra']['dz']
            })

            current_segment[poi['extra']['path']] += 1

        # Set up the new track segment
        segment_name = get_segment_name(poi['extra']['path'])
        if segment_name not in lines:
            lines[segment_name] = dict({
                '_pathName': poi['extra']['path'],
                'strokeColor': '#000000',
                'strokeWeight': 4,
                'fill': False,
                'isLine': True,
                'points': list(),
                'createInfoWindow': True,
            })

        lines[segment_name]['points'].append({
            'x': poi['x'] + poi['extra']['dx'],
            'y': poi['y'] + poi['extra']['dy'],
            'z': poi['z'] + poi['extra']['dz']
        })

        if poi['extra']['colour'] is not None and poi['extra']['colour'].strip() != '':
            # Colours apply across an entire line, set these outside of the segment code
            line_colours[poi['extra']['path']] = poi['extra']['colour'].strip()

        if 'C' in poi['extra']['flags']:
            lines[segment_name]['opacity'] = 0.5
            lines[segment_name]['dashArray'] = "1 15"
            lines[segment_name]['_construction'] = True

        if 'D' in poi['extra']['flags']:
            lines[segment_name]['strokeWeight'] = 5
            lines[segment_name]['_tracks'] = 2

        if 'S' in poi['extra']['flags']:
            lines[segment_name]['strokeWeight'] = 2
            lines[segment_name]['_tracks'] = 1

    def register_station(x, y, z, station_type, note, front_text):
        fake_poi = dict()
        fake_poi['id'] = 'minecraft:sign'
        fake_poi['x'], fake_poi['y'], fake_poi['z'] = (x, y, z)
        fake_poi['front_text'] = front_text
        fake_poi['back_text'] = dict({'messagesRaw': []})

        fake_poi['hovertext'], fake_poi['text'] = format_sign(fake_poi, station_type, note, include_first_line=True)

        del fake_poi['front_text'], fake_poi['back_text'], fake_poi['id']
        station_markers.append(fake_poi)

    single_station_message = '<p class="rail-line">This station is on the <strong style="border-color:%s">%s</strong></p><br>'

    for station_name, pois in raw_station_markers.items():
        poi_lines = [poi["extra"]["path"] for poi in pois]
        has_dupe_lines = len(set(poi_lines)) != len(poi_lines)

        if not pois:
            raise ValueError(f"No station markers found for station {station_name}")
        elif len(pois) == 1:
            station_type = 'Rail Station'
            note = single_station_message % (line_colours[pois[0]["extra"]["path"]], pois[0]["extra"]["path"])

            register_station(pois[0]['x'], pois[0]['y'], pois[0]['z'], station_type, note, pois[0]['extra']['text'])
        elif station_name == "":
            # Blank station names shouldn't ever be merged
            logging.info("Not grouping %d stations without a name", len(pois))

            station_type = 'Rail Station'
            for poi in pois:
                note = single_station_message % (line_colours[poi["extra"]["path"]], poi["extra"]["path"])
                register_station(poi['x'], poi['y'], poi['z'], station_type, note, poi['extra']['text'])
        elif has_dupe_lines:
            # Multiple stations named the same thing on the same line is likely unintended.
            logging.warning("Not grouping %d stations with the same name (%s) with duplicates on the same line", len(pois), station_name)

            station_type = 'Rail Station'
            for poi in pois:
                note = single_station_message % (line_colours[poi["extra"]["path"]], poi["extra"]["path"])
                register_station(poi['x'], poi['y'], poi['z'], station_type, note, poi['extra']['text'])
        else:
            # More than one station with this name. Let's merge them.
            station_type = 'Rail Interchange Station'
            x, y, z = (
                round(sum([p['x'] for p in pois]) / len(pois)),
                round(sum([p['y'] for p in pois]) / len(pois)),
                round(sum([p['z'] for p in pois]) / len(pois)))
            ic_lines = ''.join(
                [f'<li class="rail-line"><strong style="border-color:{line_colours[p["extra"]["path"]]}">{p["extra"]["path"]}</strong></li>'
                 for p in pois])
            note = f'This station is an interchange between the following lines:<ul>{ic_lines}</ul>'

            register_station(x, y, z, station_type, note, pois[0]['extra']['text'])

    # Apply the stored colours and text to each line
    for l in lines:
        path_name = lines[l]['_pathName']
        lines[l]['strokeColor'] = line_colours[path_name]
        lines[l]['hovertext'] = path_name

        construction_text = ''
        line_count_text = ''

        if '_construction' in lines[l] and lines[l]['_construction']:
            lines[l]['hovertext'] = f'{path_name} (Under construction)'
            construction_text = '<div><em>Under Construction</em></div>'

        if '_tracks' in lines[l]:
            if lines[l]['_tracks'] == 2:
                line_count_text = '<div>Duplex track</div>'
            if lines[l]['_tracks'] == 1:
                line_count_text = '<div>Simplex track</div>'

        lines[l]['text'] = f'<strong>Railway Line</strong><br /><p class="rail-line" style="margin-top: 1rem"><strong style="border-color:{line_colours[path_name]}">{path_name}</strong></p>{construction_text}{line_count_text}'


    return list(lines.values()) + station_markers


def portal_sign_filter(poi, roof=None):
    if roof is True and poi["y"] < 127:
        return None
    if roof is False and poi["y"] > 127:
        return None

    if poi["id"] == "minecraft:end_gateway":
        poi["icon"] = "custom-icons/transport/marker_endportal.png"
        return format_sign(poi, "End Gateway", None)


def player_icons(poi):
    if poi["id"] == "Player":
        poi["icon"] = "./avatars/%s.png" % poi["EntityId"]
        return "Last known location for %s" % poi["EntityId"]


graves_cache = {}


def graves_filter(poi):
    if "CustomName" in poi and poi['id'] == 'minecraft:armor_stand' and 'graveHologram' in poi["Tags"]:
        # Extract the UUID of the grave from the armour stand tags
        grave_uuid = [t for t in poi["Tags"] if t.startswith('graveHologramGraveUUID:')][0][23:]

        # Shenanigans are afoot.
        # Graves are actually represented by three marker armour stands plus a player head.
        # The player head is on the block grid, so inaccessible to us in the genPOI run.
        # We need to create a cache outside the POI run as we need to combine the three POIs into one.
        # The cache only needs to persist for the current chunk, but data volumes are low enough that we're lazy and
        # persist it for the lifetime of the POI run.
        # Luckily, each armor stand has a tag with a UUID representing which grave it belongs to.
        if grave_uuid not in graves_cache:
            graves_cache[grave_uuid] = ["", "", "", ""]

        if poi["CustomName"].endswith("'s Grave"):
            graves_cache[grave_uuid][0] = poi["CustomNameRaw"]
            graves_cache[grave_uuid][3] = poi["CustomName"]  # for the hover text
        elif poi["CustomName"].startswith("Death: "):
            graves_cache[grave_uuid][2] = poi["CustomNameRaw"]
        else:
            graves_cache[grave_uuid][1] = poi["CustomNameRaw"]

        if not all(graves_cache[grave_uuid]):
            # Not yet got complete data for this grave; skip for now and a later POI should complete it
            return None

        hover = graves_cache[grave_uuid][3]

        window = '<div class="infoWindow-grave-wrapper">'
        window += '<div class="infoWindow-grave-overlay">'
        line1 = json_text_to_html(graves_cache[grave_uuid][0])
        line2 = json_text_to_html(graves_cache[grave_uuid][1])
        line3 = json_text_to_html(graves_cache[grave_uuid][2])

        window += '<div class="infoWindow-grave-text"><h4>%s</h4><div>%s</div><div>%s</div></div>' % (line1, line2, line3)

        window += '</div>'  # overlay
        window += '</div>'  # wrapper

        return hover, window


ENTITY_NAMES = {
    'allay': 'Allay',
    'armadillo': 'Armadillo',
    'axolotl': 'Axolotl',
    'bat': 'Bat',
    'bee': 'Bee',
    'blaze': 'Blaze',
    'bogged': 'Bogged',
    'breeze': 'Breeze',
    'camel': 'Camel',
    'cat': 'Cat',
    'cave_spider': 'Cave Spider',
    'chicken': 'Chicken',
    'cod': 'Cod',
    'cow': 'Cow',
    'creeper': 'Creeper',
    'dolphin': 'Dolphin',
    'donkey': 'Donkey',
    'drowned': 'Drowned',
    'elder_guardian': 'Elder Guardian',
    'ender_dragon': 'Ender Dragon',
    'enderman': 'Enderman',
    'endermite': 'Endermite',
    'evoker': 'Evoker',
    'fox': 'Fox',
    'frog': 'Frog',
    'ghast': 'Ghast',
    'glow_squid': 'Glow Squid',
    'goat': 'Goat',
    'guardian': 'Guardian',
    'hoglin': 'Hoglin',
    'horse': 'Horse',
    'husk': 'Husk',
    'illusioner': 'Illusioner',
    'iron_golem': 'Iron Golem',
    'llama': 'Llama',
    'magma_cube': 'Magma Cube',
    'mooshroom': 'Mooshroom',
    'mule': 'Mule',
    'ocelot': 'Ocelot',
    'panda': 'Panda',
    'parrot': 'Parrot',
    'phantom': 'Phantom',
    'pig': 'Pig',
    'piglin_brute': 'Piglin Brute',
    'piglin': 'Piglin',
    'pillager': 'Pillager',
    'polar_bear': 'Polar Bear',
    'pufferfish': 'Pufferfish',
    'rabbit': 'Rabbit',
    'ravager': 'Ravager',
    'salmon': 'Salmon',
    'sheep': 'Sheep',
    'shulker': 'Shulker',
    'silverfish': 'Silverfish',
    'skeleton_horse': 'Skeleton Horse',
    'skeleton': 'Skeleton',
    'slime': 'Slime',
    'sniffer': 'Sniffer',
    'snow_golem': 'Snow Golem',
    'spider': 'Spider',
    'squid': 'Squid',
    'stray': 'Stray',
    'strider': 'Strider',
    'tadpole': 'Tadpole',
    'trader_llama': 'Trader Llama',
    'tropical_fish': 'Tropical Fish',
    'turtle': 'Turtle',
    'vex': 'Vex',
    'villager': 'Villager',
    'vindicator': 'Vindicator',
    'wandering_trader': 'Wandering Trader',
    'warden': 'Warden',
    'witch': 'Witch',
    'wither_skeleton': 'Wither Skeleton',
    'wither': 'Wither',
    'wolf': 'Wolf',
    'zombie_villager': 'Zombie Villager',
    'zombie': 'Zombie',
    'zombified_piglin': 'Zombified Piglin',
}


def _process_entity_poi(poi):
    """Apply common processing to entity POIs.

    **Do NOT mutate the ``poi`` parameter in this function.**"""
    entity_id = poi['id'][len('minecraft:'):]

    hover = "%s" % (poi.get("CustomName") or entity_id)

    window = '<div class="infoWindow-entity-wrapper">'
    window += '<div class="infoWindow-entity-icon icon mc-entity-%s"></div>' % entity_id

    if "CustomNameRaw" in poi:
        name_html = json_text_to_html(poi["CustomNameRaw"])
    else:
        name_html = entity_id

    mob_name = ENTITY_NAMES.get(entity_id, entity_id)
    window += '<div class="infoWindow-entity-text"><h4>%s</h4><div>%s</div></div></div>' % (name_html, mob_name)

    if "Pos" in poi:
        # All entities should have a Pos tag where their position in the world is represented by three doubles in a list
        # (for X, Y, and Z), but this is Minecraft, so you never know....
        coords = (
            "("
            + "X: "
            + str(round(poi["Pos"][0]))
            + ", Y: "
            + str(round(poi["Pos"][1]))
            + ", Z: "
            + str(round(poi["Pos"][2]))
            + ")"
        )
        window += coords

    return hover, window, entity_id


def named_mob_filter(poi):
    if "CustomName" in poi and "Health" in poi:
        # Skip any mobs which have been silenced by datapack
        if poi.get('Silent', 0) == 1:
            return None

        # Ignore marker armour stands (ie, graves)
        if poi['id'] == 'minecraft:armor_stand' and poi.get('Marker', 0) == 1:
            return None

        hover, window, entity_id = _process_entity_poi(poi)

        poi['cssClass'] = 'mc-entity-' + entity_id

        return hover, window


def all_allays_filter(poi):
    if poi.get('id') == 'minecraft:allay':
        poi['cssClass'] = 'mc-entity-allay'

        hover, window, _ = _process_entity_poi(poi)

        return hover, window


def fastlizard_mcal_filter(poi):
    if poi['id'] != 'minecraft:sign':
        return None

    if poi['front_text']['messages'][0].strip() != '#mCal':
        return None

    try:
        username = poi['front_text']['messages'][1].strip()
        rawDate = poi['front_text']['messages'][2].strip()
        if rawDate.startswith('Date:'):
            rawDate = rawDate[len('Date:'):]
        rawDate = rawDate.strip()

        parsedDate = dateutil.parser.parse(rawDate, fuzzy=True)

        # If specified date is Saturday, push it to Sunday
        # This arbitrary decision is because UTC is the One True Timezone(tm).
        if parsedDate.isoweekday() == 6:
            parsedDate += datetime.timedelta(days=1)

        # Skip past dates.
        if parsedDate < dateutil.utils.today():
            return None

        rsvp = poi['front_text']['messages'][3].strip()
        if rsvp.startswith('RSVP:'):
            rsvp = rsvp[len('RSVP:'):]
        rsvp = rsvp.strip()

        extra = dict({
            'username': username,
            'date': parsedDate.date().isoformat(),
            'rsvp': rsvp,
        })

        data = dict({
            'extra': extra,
        })

        return data
    except Exception as e:
        logging.warning("Unable to process mCal marker at [%d, %d, %d]: (%s) %s", poi['x'], poi['y'], poi['z'], type(e).__name__, e)


def fastlizard_mcal_postprocess(pois):
    by_date = dict()

    vcal = "BEGIN:VCALENDAR\nVERSION:2.0\n"

    for poi in pois:
        if poi['extra']['date'] not in by_date:
            by_date[poi['extra']['date']] = []
        by_date[poi['extra']['date']].append(poi['extra'])

    window = '<div class="icon-header"><img src="custom-icons/marker_calendar.png" alt=""><h2>Minecraft Calendar</h2><a href="Minecraft.ical">iCal</a></div>'
    window += '<div class="mCal-container">'

    for d in sorted(by_date.keys())[:4]:
        dateParsed = dateutil.parser.parse(d)
        dateDisplay = dateParsed.strftime('%a, %B %d')

        eventDescription = ""

        window += f'<div class="mCal-date-entry"><h3>{dateDisplay}</h3><dl>'
        for poi in by_date[d]:
            window+= f'<dt>{poi["username"]}</dt><dd>{poi["rsvp"]}</dd>'
            eventDescription+= f'{poi["username"]}: {poi["rsvp"]}\\n'
        window += f'</dl></div>'

        eventUid = f"minecraft{dateParsed.strftime('%Y%m%d')}@minecraft.fastlizard4.org"
        now = datetime.datetime.now().strftime('%Y%m%dT%H%M%SZ')
        vcal += f"BEGIN:VEVENT\nUID:{eventUid}\nDTSTART:{dateParsed.strftime('%Y%m%d')}T060000Z\nDTEND:{dateParsed.strftime('%Y%m%d')}T150000Z\nDTSTAMP:{now}\nSUMMARY:Minecraft\nDESCRIPTION:{eventDescription}\nEND:VEVENT\n"
    window += '</div>'

    vcal += 'END:VCALENDAR\n'
    f = open(os.environ.get("OVERVIEWER_OUTPUT_DIRECTORY") + '/Minecraft.ical', 'w')
    f.write(vcal)
    f.close()

    newPoi = dict({
        'x': -101,
        'y': 66,
        'z': 182,
        'hovertext': "Minecraft Calendaring and Scheduling Core Object Specification",
        'text': window
    })

    return [newPoi]


def json_text_to_html(json_text):
    """
    This is roughly based on the Overviewer Core function jsonText. The
    warning from that function, copied below, also applies to this function.

    The aforementioned warning reads as follows:

    If you want to keep your stomach contents do not, under any circumstance,
    read the body of the following function. You have been warned.
    """

    if json_text is None or json_text == "null":
        return ""

    json_text_colours = ["black", "dark_blue", "dark_green", "dark_aqua", "dark_red", "dark_purple", "gold", "gray",
                         "dark_gray", "blue", "green", "aqua", "red", "light_purple", "yellow", "white"]

    if ((json_text.startswith('"') and json_text.endswith('"')) or
            (json_text.startswith('{') and json_text.endswith('}'))):
        try:
            js = json.loads(json_text)
        except ValueError:
            return json_text

        def parse_internal(input_value, colour, bold, italic, underlined, strikethrough, obfuscated):
            """
            Input can be a list, object, or bare string.
            https://minecraft.wiki/w/Raw_JSON_text_format
            """
            output_value = ""
            if isinstance(input_value, list):
                for extra in input_value:
                    output_value += parse_internal(extra, colour, bold, italic, underlined, strikethrough, obfuscated)
            elif isinstance(input_value, dict):
                has_value = False

                if 'color' in input_value:
                    if input_value['color'] in json_text_colours:
                        colour = input_value['color']
                    elif input_value['color'].startswith('#'):
                        colour = input_value['color']
                if 'bold' in input_value:
                    bold = input_value['bold']
                if 'italic' in input_value:
                    italic = input_value['italic']
                if 'underlined' in input_value:
                    underlined = input_value['underlined']
                if 'strikethrough' in input_value:
                    strikethrough = input_value['strikethrough']
                if 'obfuscated' in input_value:
                    obfuscated = input_value['obfuscated']

                if "text" in input_value and len(input_value["text"]) > 0:
                    output_value = style_text(input_value['text'], colour, bold, italic, underlined, strikethrough, obfuscated)
                    has_value = True
                if "extra" in input_value and len(input_value["extra"]) > 0:
                    extra_bits = parse_internal(input_value["extra"], colour, bold, italic, underlined, strikethrough, obfuscated)
                    if extra_bits != "":
                        output_value += extra_bits
                        has_value = True

                if not has_value:
                    output_value = ""
            elif isinstance(input_value, str):
                output_value = style_text(input_value, colour, bold, italic, underlined, strikethrough, obfuscated)
            return output_value

        def style_text(text, colour, bold, italic, underlined, strikethrough, obfuscated):
            if text is None or text == "":
                # No text to render, no point wrapping it.
                return ""

            if colour is None and not bold and not italic and not underlined and not strikethrough and not obfuscated:
                # plain text, just return as-is
                return text

            css_class = ''
            style_attr = ''
            output_value = ''
            custom_colour = False

            if colour is not None:
                if colour in json_text_colours:
                    css_class += ' mctext-' + colour
                elif colour.startswith('#'):
                    if not obfuscated:
                        # we'll deal with obfuscated custom-coloured text separately.
                        style_attr += 'color: %s;' % colour
                    custom_colour = True
            if bold:
                css_class += ' mctext-bold'
            if italic:
                css_class += ' mctext-italic'
            if underlined:
                css_class += ' mctext-underlined'
            if strikethrough:
                css_class += ' mctext-strikethrough'
            if obfuscated:
                if not custom_colour:
                    css_class += ' mctext-obfuscated'
                else:
                    # thanks, I hate it.
                    style_attr += f'text-shadow: 0 0 6px {colour}, 0 0 6px {colour}, 0 0 6px {colour}, 0 0 6px {colour}, 0 0 8px {colour}, 0 0 8px {colour};color: transparent;'

            if style_attr != '':
                style_attr = f'style="{style_attr}"'

            output_value += '<span class="%s" %s>' % (css_class.lstrip(), style_attr)
            output_value += text
            output_value += '</span>'

            return output_value

        parse_result = parse_internal(js, None, False, False, False, False, False)

        if parse_result != "":
            parse_result = f'<span class="mc-jsontext">{parse_result}</span>'

        return parse_result


def int_or_default(i, default):
    try:
        return int(i)
    except ValueError:
        return default
