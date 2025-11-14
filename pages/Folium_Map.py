import streamlit as st
from streamlit.components.v1 import html
import folium
from data_loader import load_metal_bands
from geo import resolve_origin
import pandas as pd

st.set_page_config(page_title="Map — Folium demo", layout="wide")
st.title("Map — Folium demo")

st.markdown(
    """
    This page demonstrates embedding a Folium (Leaflet) map inside Streamlit.

    - Click anywhere on the map to get the latitude/longitude (popup).
    - This is a minimal landing map; later we'll add markers, country click handling,
      and tie clicks back to the band dataset for the guessing game.
    """
)

with st.expander("Dataset info"):
    try:
        df = load_metal_bands()
        st.write("Rows:", df.shape[0], "Columns:", df.shape[1])
        st.dataframe(df.head(5))
    except Exception as e:
        st.warning(f"Could not load dataset preview: {e}")


def make_map(show_debug_marker: bool = False):
    # Basic world map centered roughly at lat 20, lon 0
    m = folium.Map(location=[20, 0], zoom_start=2, tiles="OpenStreetMap")

    # Add a few tile layers to switch between (provide required attributions)
    folium.TileLayer(
        "Stamen Terrain",
        attr=(
            "Map tiles by Stamen Design, CC BY 3.0 — Data by OpenStreetMap contributors"
        ),
    ).add_to(m)
    folium.TileLayer(
        "CartoDB positron",
        attr=("&copy; OpenStreetMap contributors &copy; CARTO"),
    ).add_to(m)
    folium.LayerControl().add_to(m)

    # Show clicked lat/lon via popup (handy for prototyping)
    folium.LatLngPopup().add_to(m)

    # Small helper: pick first non-empty value from several possible column names
    def _first_nonempty(row, *cols):
        for c in cols:
            v = row.get(c)
            # guard against pandas NaN
            if isinstance(v, float) and pd.isna(v):
                continue
            if v is None:
                continue
            if isinstance(v, str) and v.strip() == "":
                continue
            return v
        return None

    # Aggregate bands by resolved country key and coords
    country_map = {}  # country_key -> {coords: (lat,lon), bands: [names]}
    try:
        df = load_metal_bands()
        for _, row in df.iterrows():
            # support both the old dataset (origin/band_name) and new (Country/Name)
            origin = _first_nonempty(row, "origin", "Origin", "Country", "country")
            if not origin or not isinstance(origin, str):
                continue
            country_key, coords = resolve_origin(origin)
            if country_key and coords:
                entry = country_map.setdefault(country_key, {"coords": coords, "bands": []})
                # band name might be under several column headers
                band = _first_nonempty(row, "band_name", "band", "Band Name", "Name", "name")
                entry["bands"].append(band or "<unknown>")
    except Exception:
        country_map = {}

    # Add one marker per country with a popup listing bands
    added = 0
    for country_key, info in country_map.items():
        lat, lon = info["coords"]
        bands = info["bands"]
        count = len(bands)
        # Build HTML popup: title + count + up to 20 band names
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
        # Use a circle marker for better visibility at country centroid
        folium.CircleMarker(location=[lat, lon], radius=7, color="blue", fill=True, fill_opacity=0.7, popup=popup).add_to(m)
        added += 1

    # Optional debug marker: a large red marker at the center to ensure markers render
    if show_debug_marker:
        folium.Marker(location=[20, 0], popup=folium.Popup("Debug marker", max_width=200),
                      icon=folium.Icon(color='red', icon='info-sign')).add_to(m)

    return m, added


show_debug = st.checkbox("Show debug center marker (red)")
m, added = make_map(show_debug_marker=show_debug)

# Display how many markers were added (helps diagnose clustering/hiding)
st.info(f"Markers added (resolvable origins): {added}")

# Embed folium map HTML in Streamlit. Works in Streamlit and Jupyter notebooks.
m_html = m._repr_html_()
html(m_html, height=650)

st.markdown(
    """
    Notes / next steps:

    - To capture click events back in Python, we'll create a small Streamlit component
      or use a JS postMessage bridge that sets a Streamlit widget value. For now the
      map supports LatLng popups which is handy for prototyping.
    - We can later add markers for band origins (after geocoding `origin`) and
      compute distances to clicked points to grade guesses.
    """
)
