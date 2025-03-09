import json
import numpy as np
import common

# defined as the block your *head* occupies when entering the FTH
# Split out for testing purposes.
FTH_ORIGIN = np.array((52, 65, 62))

# Load the data file for the FTH
FTH_FLOORS = json.load(open('fast-travel-hub.json'))['floors']

# Unless the FTH is massively redesigned, this shouldn't ever change
FTH_COL_OFFSET = np.array((0, 0, -13))
FTH_FLOOR_OFFSET = np.array((0, 4, 0))
FTH_SEARCH_OFFSETS = [(-4, 0, -4), (4, 0, 4)]

# Count the floors and columns in the data file
FTH_MAX_FLOOR = max([max([f['level'] for f in x['pages']]) for x in FTH_FLOORS])
FTH_MAX_COLUMN = max([max([f['column'] for f in x['pages']]) for x in FTH_FLOORS])

# Figure out the centre of the "room" diagonally opposite the origin
FTH_FAR_CENTRE = np.add(
    FTH_ORIGIN,
    np.add(FTH_FLOOR_OFFSET * FTH_MAX_FLOOR, FTH_COL_OFFSET * FTH_MAX_COLUMN)
)

# Shuffle the coordinates around and add the search offsets to give a volume
# FTH signs should exist within
FTH_SEARCH_VOLUME = (
    (
        min(FTH_FAR_CENTRE[0], FTH_ORIGIN[0]) + FTH_SEARCH_OFFSETS[0][0],
        min(FTH_FAR_CENTRE[1], FTH_ORIGIN[1]) + FTH_SEARCH_OFFSETS[0][1],
        min(FTH_FAR_CENTRE[2], FTH_ORIGIN[2]) + FTH_SEARCH_OFFSETS[0][2]
    ),
    (
        max(FTH_FAR_CENTRE[0], FTH_ORIGIN[0]) + FTH_SEARCH_OFFSETS[1][0],
        max(FTH_FAR_CENTRE[1], FTH_ORIGIN[1]) + FTH_SEARCH_OFFSETS[1][1],
        max(FTH_FAR_CENTRE[2], FTH_ORIGIN[2]) + FTH_SEARCH_OFFSETS[1][2]
    )
)


def point_in_volume(poi, volume) -> bool:
    return (
            volume[0][0] <= poi['x'] <= volume[1][0]
        and volume[0][1] <= poi['y'] <= volume[1][1]
        and volume[0][2] <= poi['z'] <= volume[1][2]
    )


def fast_travel_filter(poi):
    if poi["id"] not in ["minecraft:sign", "minecraft:hanging_sign"]:
        return None

    if poi["front_text"]["messages"][0] == "# FTH #":
        if point_in_volume(poi, FTH_SEARCH_VOLUME):
            return dict({
                "extra": {
                    "type": "hub",
                    "front_text": poi['front_text']
                }
            })


    front, back, all_text = common.get_sign_text(poi)
    public = "fast travel" in all_text or "faster travelling" in all_text

    if all_text == "":
        return None  # Return nothing; sign is private
    elif common.sign_explicit_visibility(front, back, "#"):
        return None  # Return nothing; sign is private
    elif public:
        return dict({
            "extra": {
                "type": "station",
                "front_text": poi['front_text'],
                "back_text": poi['back_text'],
                "id": poi['id'],
            },
        })
    else:
        return None  # Return nothing; sign is private


def fast_travel_postprocess(pois):
    # process floor searchable areas into testable volumes
    for f in FTH_FLOORS:
        f['volumes'] = []
        for p in f['pages']:
            offset = np.add(FTH_COL_OFFSET * p['column'], FTH_FLOOR_OFFSET * p['level'])
            centrepoint = np.add(FTH_ORIGIN, offset)
            f['volumes'].append((
                (centrepoint[0] + FTH_SEARCH_OFFSETS[0][0], centrepoint[1] + FTH_SEARCH_OFFSETS[0][1], centrepoint[2] + FTH_SEARCH_OFFSETS[0][2]),
                (centrepoint[0] + FTH_SEARCH_OFFSETS[1][0], centrepoint[1] + FTH_SEARCH_OFFSETS[1][1], centrepoint[2] + FTH_SEARCH_OFFSETS[1][2]),
            ))

    # organise FTH POIs by name, augmented with floor
    raw_fth_pois = [x for x in pois if x['extra']['type'] == 'hub']
    fth_pois = {}

    for poi in raw_fth_pois:
        ft_name = " ".join(poi['extra']["front_text"]["messages"][1:3])
        if not poi['extra']["front_text"]["messages"][3].startswith("("):
            ft_name += f" {poi['extra']['front_text']['messages'][3]}"
        ft_name = ft_name.strip().lower()

        found = False
        for cat in FTH_FLOORS:
            for i in range(len(cat['volumes'])):
                if point_in_volume(poi, cat['volumes'][i]):
                    fth_pois[ft_name] = (cat['name'], i)
                    found = True
                    break
            if found:
                break

    # we should now have a dict in `fth_pois` indexed by fast travel name, with a tuple of category/page.
    # go through stations augmenting with floor data
    station_pois = [x for x in pois if x['extra']['type'] == 'station']

    for poi in station_pois:
        # Temp set these values so format_sign works properly
        poi['front_text'] = poi['extra']['front_text']
        poi['back_text'] = poi['extra']['back_text']
        poi['id'] = poi['extra']['id']

        location_data = ""

        sign_text = common.get_sign_text(poi)[2]
        for k in fth_pois.keys():
            if k in sign_text:
                cat_name = fth_pois[k][0]
                cat_page = f' (page {fth_pois[k][1] + 1})'
                category_data = [x for x in FTH_FLOORS if x['name'] == cat_name][0]
                cat_colour = category_data['colour']
                poi["icon"] = f"fast-travel/{category_data['marker']}.png"

                if len(category_data['pages']) == 1:
                    cat_page = ''

                location_data = f'<div class="fth-location"><strong>Fast Travel Hub</strong><br /><span class="fth-floor" style="border-color:{cat_colour}">{cat_name}{cat_page}</span></div>'
                break

        hovertext, windowtext = common.format_sign(poi, "Fast Travel", location_data, include_first_line=True)

        # We have to clean these up again
        del poi['front_text']
        del poi['back_text']
        del poi['id']

        poi['text'] = windowtext
        poi['hovertext'] = hovertext

    return station_pois