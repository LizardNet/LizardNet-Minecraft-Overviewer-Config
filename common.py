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
        dict(name="Named entities", filterFunction=named_entity_filter, checked=False),
        dict(name="Squids", filterFunction=squid_filter, checked=False),
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
        dict(name="Named entities", filterFunction=named_entity_filter, checked=False),
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
        dict(name="Named entities", filterFunction=named_entity_filter, checked=False),
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
        dict(name="Named entities", filterFunction=named_entity_filter, checked=False),
    ]


def format_sign(poi, title, note, include_first_line=False):
    if poi["id"] in ["minecraft:sign", "minecraft:hanging_sign"]:
        poi_type = "hanging" if poi["id"] == "minecraft:hanging_sign" else "normal"

        if "front_text" in poi:
            front_lines = poi["front_text"]["messages"]
            back_lines = poi["back_text"]["messages"]
        else:
            front_lines = [poi["Text1"], poi["Text2"], poi["Text3"], poi["Text4"]]
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

        front_lines = trim_blank_lines(front_lines)
        back_lines = trim_blank_lines(back_lines)

    else:
        poi_type = "none"
        front_lines = []
        back_lines = []

    hover = list(front_lines)
    hover.append("(" + ", ".join([str(poi["x"]), str(poi["y"]), str(poi["z"])]) + ")")

    title_html = ""
    if title is not None:
        title_html = "<strong>" + title + "</strong><br />"
        hover.insert(0, title)

    info_window_text = title_html

    if front_lines:
        # Annoyingly, we need to account here for both the old and new sign formats
        if "front_text" in poi:
            info_window_text += (
                '<div class="signtext mcpoi-'
                + poi_type
                + " mccolor-"
                + poi["front_text"]["color"]
                + " mcglow-"
                + str(poi["front_text"]["has_glowing_text"])
                + '">'
                + "<br />".join(front_lines)
                + "</div><br />"
            )
        else:
            info_window_text += (
                '<div class="signtext mcpoi-'
                + poi_type
                + " mccolor-"
                + poi["Color"]
                + " mcglow-"
                + str(poi["GlowingText"])
                + '">'
                + "<br />".join(front_lines)
                + "</div><br />"
            )
    if back_lines:
        # No need to account for the old sign format here, since old signs never have back text.
        info_window_text += (
            '<div class="signtext mcpoi-'
            + poi_type
            + " mccolor-"
            + poi["back_text"]["color"]
            + " mcglow-"
            + str(poi["back_text"]["has_glowing_text"])
            + '">'
            + "<br />".join(back_lines)
            + "</div><br />"
        )

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


def named_entity_filter(poi):
    if "CustomName" in poi:
        if poi["CustomName"] and poi["id"] != "Control" and poi["id"] != "Chest":
            poi["icon"] = "https://mcmaps.fastlizard4.org/ocelot.png"
            return "%s" % poi["CustomName"], "%s named %s" % (
                poi["id"],
                poi["CustomName"],
            )


def squid_filter(poi):
    if poi["id"] == "Squid":
        poi["icon"] = "https://mcmaps.fastlizard4.org/ocelot.png"
        return "%s" % poi["CustomName"], "%s" % poi["id"]
