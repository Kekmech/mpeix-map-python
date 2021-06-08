import ujson


async def handle_get_map_markers(conn):
    query = "select place_uid, address, json_build_object('lat', lat, 'lng', lng)::json as location,  " \
            "place_name, place_type, icon, tag from map_markers"
    data = list(map(dict, await conn.fetch(query)))
    return data
