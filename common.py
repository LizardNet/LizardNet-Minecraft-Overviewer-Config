import json
import logging


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
            filterFunction=fastlizard_fast_travel_filter,
            icon="custom-icons/transport/marker_fasttravel.png",
            checked=True,
            showIconInLegend=True,
        ),
        dict(
            # To be removed once the Railways filter has been fully implemented
            name="Transport",
            filterFunction=fastlizard_transport_sign_filter,
            icon="custom-icons/transport/marker_train.png",
            checked=True,
            showIconInLegend=True,
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


HANGING_SIGN_TYPE = 'minecraft:hanging_sign'
SIGN_TYPES = {'minecraft:sign', HANGING_SIGN_TYPE}


def format_sign(poi, title, note, include_first_line=False):
    try:
        if poi["id"] in SIGN_TYPES:
            poi_type = "hanging" if poi["id"] == HANGING_SIGN_TYPE else "normal"

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
    if poi["id"] in SIGN_TYPES:
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
    if poi["id"] in SIGN_TYPES:
        front, back, all_text = get_sign_text(poi)
        sign_type = "Hanging Sign" if poi["id"] == HANGING_SIGN_TYPE else "Sign"

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
    if poi["id"] in SIGN_TYPES:
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


def fastlizard_fast_travel_filter(poi):
    if poi["id"] in SIGN_TYPES:
        front, back, all_text = get_sign_text(poi)

        public = "fast travel" in all_text or "faster travelling" in all_text

        if all_text == "":
            return None  # Return nothing; sign is private
        elif sign_explicit_visibility(front, back, "#"):
            return None  # Return nothing; sign is private
        elif public:
            poi["icon"] = "custom-icons/transport/marker_fasttravel.png"
            return format_sign(poi, "Fast Travel", None, include_first_line=True)
        else:
            return None  # Return nothing; sign is private


def fastlizard_transport_sign_filter(poi):
    if poi["id"] in SIGN_TYPES:
        front, back, all_text = get_sign_text(poi)

        is_station = (
            "north line" in all_text
            or "green line" in all_text
            or "east line" in all_text
            or "south line" in all_text
            or "purple line" in all_text
        )

        if all_text == "":
            return None  # Return nothing; sign is private
        elif sign_explicit_visibility(front, back, "#"):
            return None  # Return nothing; sign is private
        elif sign_explicit_visibility(front, back, "@") and is_station:
            poi["icon"] = "custom-icons/transport/marker_train.png"
            return format_sign(poi, "Minecart Station", None, include_first_line=True)
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
    if poi['id'] not in SIGN_TYPES:
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
        config_line = f'{config_line}///'

        i, dx, dy, dz = config_line.split('/')
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
        })

        data = dict({
            'extra': extra
        })

        if marker_type == RAIL_STATION_MARKER:
            poi['front_text']['messagesRaw'] = display_side['messagesRaw']
            poi['back_text']['messagesRaw'] = []
            note = 'This station is on the <strong>' + path + '</strong><br /><br />'

            data['hovertext'], data['text'] = format_sign(poi, 'Rail Station', note, include_first_line=True)

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

    """
    lines = dict()

    extra_markers = []

    for poi in sorted(pois, key=lambda x: x['extra']['sequence']):
        if poi['extra']['type'] == RAIL_STATION_MARKER:
            # Stations are rendered twice. Once as a rail waypoint (a polyline point), and once as a station marker.
            # Here we copy the POI and remove the extra data, and pass it on as any other marker.
            # The original copy is still dealt with as a waypoint below.
            station_marker = poi.copy()
            del station_marker['extra']
            extra_markers.append(station_marker)

        if poi['extra']['path'] not in lines:
            lines[poi['extra']['path']] = dict({
                'strokeColor': '#000000',
                'strokeWeight': 4,
                'fill': False,
                'isLine': True,
                'points': list(),
                'createInfoWindow': True,
                'text': '<strong>Railway Line</strong><br />' + poi['extra']['path'],
                'hovertext': poi['extra']['path']
            })

        lines[poi['extra']['path']]['points'].append({
            'x': poi['x'] + poi['extra']['dx'],
            'y': poi['y'] + poi['extra']['dy'],
            'z': poi['z'] + poi['extra']['dz']
        })

        if poi['extra']['colour'] is not None and poi['extra']['colour'].strip() != '':
            lines[poi['extra']['path']]['strokeColor'] = poi['extra']['colour'].strip()

    return list(lines.values()) + extra_markers


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
        poi["icon"] = "https://overviewer.org/avatar/%s" % poi["EntityId"]
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


def named_mob_filter(poi):
    if "CustomName" in poi and "Health" in poi:
        # Skip any mobs which have been silenced by datapack
        if poi.get('Silent', 0) == 1:
            return None

        # Ignore marker armour stands (ie, graves)
        if poi['id'] == 'minecraft:armor_stand' and poi.get('Marker', 0) == 1:
            return None

        entity_id = poi['id'][len('minecraft:'):]

        poi['cssClass'] = 'mc-entity-' + entity_id

        hover = "%s" % poi["CustomName"]

        window = '<div class="infoWindow-entity-wrapper">'
        window += '<div class="infoWindow-entity-icon icon mc-entity-%s"></div>' % entity_id
        name_html = json_text_to_html(poi["CustomNameRaw"])
        mob_name = entity_id_to_mob(entity_id)
        window += '<div class="infoWindow-entity-text"><h4>%s</h4><div>%s</div></div></div>' % (name_html, mob_name)

        return hover, window


def entity_id_to_mob(id):
    mapping = {
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

    return mapping.get(id, id)


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

        def parse_internal(input_value):
            """
            Input can be a list, object, or bare string.
            https://minecraft.wiki/w/Raw_JSON_text_format
            """
            output_value = ""
            if isinstance(input_value, list):
                for extra in input_value:
                    output_value += parse_internal(extra)
            elif isinstance(input_value, dict):
                css_class = 'mc-jsontext'
                style_attr = ''

                has_value = False

                if 'color' in input_value:
                    if input_value['color'] in json_text_colours:
                        css_class += ' mctext-' + input_value['color']
                    elif input_value['color'].startswith('#'):
                        style_attr = 'style="color: %s"' % input_value['color']

                if 'bold' in input_value and input_value['bold']:
                    css_class += ' mctext-bold'
                if 'italic' in input_value and input_value['italic']:
                    css_class += ' mctext-italic'
                if 'underlined' in input_value and input_value['underlined']:
                    css_class += ' mctext-underlined'
                if 'strikethrough' in input_value and input_value['strikethrough']:
                    css_class += ' mctext-strikethrough'
                if 'obfuscated' in input_value and input_value['obfuscated']:
                    css_class += ' mctext-obfuscated'

                output_value += '<span class="%s" %s>' % (css_class, style_attr)

                if "text" in input_value and len(input_value["text"]) > 0:
                    output_value += input_value["text"]
                    has_value = True
                if "extra" in input_value and len(input_value["extra"]) > 0:
                    extra_bits = parse_internal(input_value["extra"])
                    if extra_bits != "":
                        output_value += extra_bits
                        has_value = True

                output_value += "</span>"

                if not has_value:
                    output_value = ""
            elif isinstance(input_value, str):
                output_value = input_value
            return output_value

        return parse_internal(js)


def int_or_default(i, default):
    try:
        return int(i)
    except ValueError:
        return default
