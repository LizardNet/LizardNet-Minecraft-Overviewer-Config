import json


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
            name="Transport",
            filterFunction=fastlizard_transport_sign_filter,
            icon="custom-icons/transport/marker_train.png",
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


def fastlizard_fast_travel_filter(poi):
    if poi["id"] in ["minecraft:sign", "minecraft:hanging_sign"]:
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
    if poi["id"] in ["minecraft:sign", "minecraft:hanging_sign"]:
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
        grave_uuid = [t for t in poi["Tags"] if t.startswith('graveHologramGraveUUID:')][0][23:]

        # Shenanigans are afoot.
        # Graves are actually represented by three marker armour stands plus a player head.
        # The player head is on the block grid, so inaccessible to us in the genPOI run.
        # We need to create a cache outside the POI run as we need to combine the three POIs into one.
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