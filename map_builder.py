"""Build a folium map with markers for bands using the offline geo mapping.

This module can be executed to sanity-check that marker creation works.
"""
from data_loader import load_metal_bands
from geo import resolve_origin
import folium
from folium.plugins import MarkerCluster


def build_map():
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="OpenStreetMap")
    folium.TileLayer(
        "Stamen Terrain",
        attr=(
            "Map tiles by Stamen Design, CC BY 3.0 — Data by OpenStreetMap contributors"
        ),
    ).add_to(m)
    folium.TileLayer("CartoDB positron", attr=("&copy; OpenStreetMap contributors &copy; CARTO")).add_to(m)

    # Aggregate bands by country
    country_map = {}
    df = load_metal_bands()
    for _, row in df.iterrows():
        origin = row.get("origin")
        if not origin or not isinstance(origin, str):
            continue
        country_key, coords = resolve_origin(origin)
        if country_key and coords:
            entry = country_map.setdefault(country_key, {"coords": coords, "bands": []})
            entry["bands"].append(row.get("band_name") or "<unknown>")

    added = 0
    for country_key, info in country_map.items():
        lat, lon = info["coords"]
        bands = info["bands"]
        count = len(bands)
        shown = bands[:20]
        more = count - len(shown)
        list_html = """
        <div style='max-height: 300px; overflow:auto;'>
          <h4 style='margin:0;'>%s</h4>
          <div>bands: %d</div>
          <ul style='margin-top:0;'>%s</ul>
          %s
        </div>
        """ % (
            country_key.title(),
            count,
            "".join(f"<li>{b}</li>" for b in shown),
            f"<div>and {more} more...</div>" if more > 0 else "",
        )
        popup = folium.Popup(list_html, max_width=400)
        folium.CircleMarker(location=[lat, lon], radius=7, color="blue", fill=True, fill_opacity=0.7, popup=popup).add_to(m)
        added += 1

    return m, added


if __name__ == '__main__':
    m, count = build_map()
    print('markers added:', count)
