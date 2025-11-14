"""Simple local geocoding: map common country names to approximate lat/lon.

This is intentionally small and offline — it covers the common origin values
from the dataset. Unknown origins will return None.
"""
from typing import Optional, Tuple

# Mapping of normalized country name -> (lat, lon)
COUNTRY_COORDINATES = {
    "united kingdom": (55.3781, -3.4360),
    "united states": (38.0, -97.0),
    "usa": (38.0, -97.0),
    "us": (38.0, -97.0),
    "sweden": (60.1282, 18.6435),
    "finland": (61.9241, 25.7482),
    "germany": (51.1657, 10.4515),
    "norway": (60.4720, 8.4689),
    "poland": (51.9194, 19.1451),
    "france": (46.2276, 2.2137),
    "the netherlands": (52.1326, 5.2913),
    "netherlands": (52.1326, 5.2913),
    "brazil": (-14.2350, -51.9253),
    "portugal": (39.3999, -8.2245),
    "switzerland": (46.8182, 8.2275),
    "australia": (-25.2744, 133.7751),
    "canada": (56.1304, -106.3468),
    "italy": (41.8719, 12.5674),
    "greece": (39.0742, 21.8243),
    "austria": (47.5162, 14.5501),
    "denmark": (56.2639, 9.5018),
    "israel": (31.0461, 34.8516),
    "ireland": (53.1424, -7.6921),
    "spain": (40.4637, -3.7492),
    "russia": (61.5240, 105.3188),
    "argentina": (-38.4161, -63.6167),
    "japan": (36.2048, 138.2529),
    "china": (35.8617, 104.1954),
    "belgium": (50.5039, 4.4699),
    "czech republic": (49.8175, 15.4730),
    "slovenia": (46.1512, 14.9955),
}


def normalize_name(name: str) -> str:
    if not name:
        return ""
    n = name.strip().lower()
    # common aliases
    n = n.replace("u.s.a.", "usa").replace("u.s.", "usa")
    n = n.replace("united states of america", "united states")
    n = n.replace("us", "usa")
    # remove excess whitespace and periods
    n = n.replace(".", "")
    return n


def get_coords(origin_text: str) -> Optional[Tuple[float, float]]:
    """Try to get coordinates for an origin string.

    The origin_text can be a single country or a comma-separated list; we try
    each candidate until we find a match in the local mapping.
    """
    if not origin_text or not isinstance(origin_text, str):
        return None

    # Split on common separators (commas, slash, semicolon)
    parts = [p.strip() for p in origin_text.replace("/", ",").split(",") if p.strip()]

    for part in parts:
        n = normalize_name(part)
        # direct match
        if n in COUNTRY_COORDINATES:
            return COUNTRY_COORDINATES[n]

        # try a simple substring match (e.g., 'united kingdom' in 'united kingdom, usa')
        for country_key in COUNTRY_COORDINATES.keys():
            if country_key in n:
                return COUNTRY_COORDINATES[country_key]

    return None


def resolve_origin(origin_text: str) -> Tuple[Optional[str], Optional[Tuple[float, float]]]:
    """Return a normalized country key and coordinates for an origin string.

    Returns (country_key, (lat, lon)) or (None, None) if not resolvable.
    """
    if not origin_text or not isinstance(origin_text, str):
        return None, None

    parts = [p.strip() for p in origin_text.replace("/", ",").split(",") if p.strip()]

    for part in parts:
        n = normalize_name(part)
        # direct match
        if n in COUNTRY_COORDINATES:
            return n, COUNTRY_COORDINATES[n]

        # substring match
        for country_key in COUNTRY_COORDINATES.keys():
            if country_key in n:
                return country_key, COUNTRY_COORDINATES[country_key]

    return None, None
