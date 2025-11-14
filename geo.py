"""Simple local geocoding: map common country names to approximate lat/lon.

This is intentionally small and offline — it covers the common origin values
from the dataset. Unknown origins will return None.
"""
from typing import Optional, Tuple
import re
import unicodedata

# Mapping of normalized country name -> (lat, lon)
COUNTRY_COORDINATES = {
    # Europe
    "afghanistan": (33.9391, 67.7100),
    "albania": (41.1533, 20.1683),
    "algeria": (28.0339, 1.6596),
    "andorra": (42.5063, 1.5218),
    "angola": (-11.2027, 17.8739),
    "argentina": (-38.4161, -63.6167),
    "armenia": (40.0691, 45.0382),
    "aruba": (12.5211, -69.9683),
    "australia": (-25.2744, 133.7751),
    "austria": (47.5162, 14.5501),
    "azerbaijan": (40.1431, 47.5769),
    "bahrain": (26.0667, 50.5577),
    "bangladesh": (23.6850, 90.3563),
    "barbados": (13.1939, -59.5432),
    "belarus": (53.7098, 27.9534),
    "belgium": (50.5039, 4.4699),
    "belize": (17.1899, -88.4976),
    "bolivia": (-16.2902, -63.5887),
    "bosnia and herzegovina": (43.9159, 17.6791),
    "botswana": (-22.3285, 24.6849),
    "brazil": (-14.2350, -51.9253),
    "brunei": (4.5353, 114.7277),
    "bulgaria": (42.7339, 25.4858),
    "cambodia": (12.5657, 104.9910),
    "canada": (56.1304, -106.3468),
    "chile": (-35.6751, -71.5430),
    "china": (35.8617, 104.1954),
    "colombia": (4.5709, -74.2973),
    "costa rica": (9.7489, -83.7534),
    "croatia": (45.1000, 15.2000),
    "cuba": (21.5218, -77.7812),
    "curacao": (12.1696, -68.9900),
    "cyprus": (35.1264, 33.4299),
    "czechia": (49.8175, 15.4730),
    "denmark": (56.2639, 9.5018),
    "dominican republic": (18.7357, -70.1627),
    "east timor": (-8.8742, 125.7275),
    "ecuador": (-1.8312, -78.1834),
    "egypt": (26.8206, 30.8025),
    "el salvador": (13.7942, -88.8965),
    "estonia": (58.5953, 25.0136),
    "ethiopia": (9.1450, 40.4897),
    "falkland islands": (-51.7963, -59.5236),
    "faroe islands": (61.8926, -6.9118),
    "finland": (61.9241, 25.7482),
    "france": (46.2276, 2.2137),
    "french guiana": (3.9339, -53.1258),
    "french polynesia": (-15.3767, -140.3340),
    "georgia": (42.3154, 43.3569),
    "germany": (51.1657, 10.4515),
    "gibraltar": (36.1408, -5.3536),
    "greece": (39.0742, 21.8243),
    "greenland": (71.7069, -42.6043),
    "guadeloupe": (16.2650, -61.5510),
    "guam": (13.4443, 144.7937),
    "guatemala": (15.7835, -90.2308),
    "guernsey": (49.4657, -2.5853),
    "guyana": (4.8604, -58.9302),
    "honduras": (15.2000, -86.2419),
    "hong kong": (22.3193, 114.1694),
    "hungary": (47.1625, 19.5033),
    "iceland": (64.9631, -19.0208),
    "india": (20.5937, 78.9629),
    "indonesia": (-0.7893, 113.9213),
    "international": (20.0, 0.0),
    "iran": (32.4279, 53.6880),
    "iraq": (33.2232, 43.6793),
    "ireland": (53.1424, -7.6921),
    "isle of man": (54.2361, -4.5481),
    "israel": (31.0461, 34.8516),
    "italy": (41.8719, 12.5674),
    "jamaica": (18.1096, -77.2975),
    "japan": (36.2048, 138.2529),
    "jersey": (49.2144, -2.1313),
    "jordan": (30.5852, 36.2384),
    "kazakhstan": (48.0196, 66.9237),
    "kenya": (-0.0236, 37.9062),
    "korea, south": (36.0, 128.0),
    "korea": (36.0, 128.0),
    "korea south": (36.0, 128.0),
    "korea north": (40.3399, 127.5101),
    "kuwait": (29.3117, 47.4818),
    "kyrgyzstan": (41.2044, 74.7661),
    "laos": (19.8563, 102.4955),
    "latvia": (56.8796, 24.6032),
    "lebanon": (33.8547, 35.8623),
    "libya": (26.3351, 17.2283),
    "liechtenstein": (47.1660, 9.5554),
    "lithuania": (55.1694, 23.8813),
    "luxembourg": (49.8153, 6.1296),
    "madagascar": (-18.7669, 46.8691),
    "malawi": (-13.2543, 34.3015),
    "malaysia": (4.2105, 101.9758),
    "maldives": (3.2028, 73.2207),
    "malta": (35.9375, 14.3754),
    "mauritius": (-20.3484, 57.5522),
    "mexico": (23.6345, -102.5528),
    "moldova": (47.4116, 28.3699),
    "monaco": (43.7384, 7.4246),
    "mongolia": (46.8625, 103.8467),
    "montenegro": (42.7087, 19.3744),
    "morocco": (31.7917, -7.0926),
    "mozambique": (-18.6657, 35.5296),
    "myanmar": (21.9162, 95.9560),
    "namibia": (-22.9576, 18.4904),
    "nepal": (28.3949, 84.1240),
    "netherlands": (52.1326, 5.2913),
    "new caledonia": (-20.9043, 165.6180),
    "new zealand": (-40.9006, 174.8860),
    "nicaragua": (12.8654, -85.2072),
    "north macedonia": (41.6086, 21.7453),
    "norway": (60.4720, 8.4689),
    "oman": (21.5126, 55.9233),
    "pakistan": (30.3753, 69.3451),
    "palestine": (31.9522, 35.2332),
    "panama": (8.5379, -80.7821),
    "paraguay": (-23.4425, -58.4438),
    "peru": (-9.189967, -75.015152),
    "philippines": (12.8797, 121.7740),
    "poland": (51.9194, 19.1451),
    "portugal": (39.3999, -8.2245),
    "puerto rico": (18.2208, -66.5901),
    "qatar": (25.3548, 51.1839),
    "reunion": (-21.1151, 55.5364),
    "romania": (45.9432, 24.9668),
    "russia": (61.5240, 105.3188),
    "saint pierre and miquelon": (46.8852, -56.3159),
    "san marino": (43.9424, 12.4578),
    "saudi arabia": (23.8859, 45.0792),
    "serbia": (44.0165, 21.0059),
    "singapore": (1.3521, 103.8198),
    "slovakia": (48.6690, 19.6990),
    "slovenia": (46.1512, 14.9955),
    "south africa": (-30.5595, 22.9375),
    "spain": (40.4637, -3.7492),
    "sri lanka": (7.8731, 80.7718),
    "suriname": (3.9193, -56.0278),
    "svalbard": (77.5536, 23.6703),
    "sweden": (60.1282, 18.6435),
    "switzerland": (46.8182, 8.2275),
    "syria": (34.8021, 38.9968),
    "taiwan": (23.6978, 120.9605),
    "tajikistan": (38.8610, 71.2761),
    "thailand": (15.8700, 100.9925),
    "trinidad and tobago": (10.6918, -61.2225),
    "tunisia": (33.8869, 9.5375),
    "turkmenistan": (38.9697, 59.5563),
    "turkiye": (38.9637, 35.2433),
    "turkey": (38.9637, 35.2433),
    "uganda": (1.3733, 32.2903),
    "ukraine": (48.3794, 31.1656),
    "united arab emirates": (23.4241, 53.8478),
    "united kingdom": (55.3781, -3.4360),
    "united states": (38.0, -97.0),
    "united states of america": (38.0, -97.0),
    "united states": (38.0, -97.0),
    "united states (usa)": (38.0, -97.0),
    "united states of america (usa)": (38.0, -97.0),
    "united states of america": (38.0, -97.0),
    "united states": (38.0, -97.0),
    "united states": (38.0, -97.0),
    "united states": (38.0, -97.0),
    "united states": (38.0, -97.0),
    "usa": (38.0, -97.0),
    "us": (38.0, -97.0),
    "unknown": (20.0, 0.0),
    "uruguay": (-32.5228, -55.7658),
    "uzbekistan": (41.3775, 64.5853),
    "venezuela": (6.4238, -66.5897),
    "vietnam": (14.0583, 108.2772),
    "zimbabwe": (-19.0154, 29.1549),
    "aland islands": (60.1785, 19.9156),
}


def normalize_name(name: str) -> str:
    if not name:
        return ""
    # basic lowercasing/strip
    n = name.strip().lower()
    # remove diacritics so e.g. 'Türkiye' -> 'turkiye'
    n = unicodedata.normalize("NFKD", n)
    n = "".join(ch for ch in n if not unicodedata.combining(ch))

    # common aliases
    n = n.replace("u.s.a.", "usa").replace("u.s.", "usa")
    n = n.replace("united states of america", "united states")
    # replace standalone token 'us' with 'usa' (avoid changing inside words like 'australia')
    n = re.sub(r"\bus\b", "usa", n)
    # remove excess periods
    n = n.replace(".", "")
    return n


def get_coords(origin_text: str) -> Optional[Tuple[float, float]]:
    """Try to get coordinates for an origin string.

    The origin_text can be a single country or a comma-separated list; we try
    each candidate until we find a match in the local mapping.
    """
    if not origin_text or not isinstance(origin_text, str):
        return None

    # First try the full original string (handles values like 'Korea, South')
    full_norm = normalize_name(origin_text)
    if full_norm in COUNTRY_COORDINATES:
        return COUNTRY_COORDINATES[full_norm]

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

    # as fallback, try substring match on the full normalized text
    for country_key in COUNTRY_COORDINATES.keys():
        if country_key in full_norm:
            return COUNTRY_COORDINATES[country_key]

    return None


def resolve_origin(origin_text: str) -> Tuple[Optional[str], Optional[Tuple[float, float]]]:
    """Return a normalized country key and coordinates for an origin string.

    Returns (country_key, (lat, lon)) or (None, None) if not resolvable.
    """
    if not origin_text or not isinstance(origin_text, str):
        return None, None

    parts = [p.strip() for p in origin_text.replace("/", ",").split(",") if p.strip()]
    # try the full string first
    full_norm = normalize_name(origin_text)
    if full_norm in COUNTRY_COORDINATES:
        return full_norm, COUNTRY_COORDINATES[full_norm]

    for part in parts:
        n = normalize_name(part)
        # direct match
        if n in COUNTRY_COORDINATES:
            return n, COUNTRY_COORDINATES[n]

        # substring match
        for country_key in COUNTRY_COORDINATES.keys():
            if country_key in n:
                return country_key, COUNTRY_COORDINATES[country_key]

    # fallback substring match on full normalized text
    for country_key in COUNTRY_COORDINATES.keys():
        if country_key in full_norm:
            return country_key, COUNTRY_COORDINATES[country_key]

    return None, None
