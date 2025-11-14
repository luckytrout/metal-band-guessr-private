import streamlit as st
from streamlit.components.v1 import html
import folium
from data_loader import load_metal_bands

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


def make_map():
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

    # Show clicked lat/lon via popup
    folium.LatLngPopup().add_to(m)

    # Helpful note marker in the map
    folium.map.Marker(
        [20, 0],
        icon=folium.DivIcon(
            html=f"<div style='font-size:12px'>Click map to get coords</div>"
        ),
    ).add_to(m)

    return m


m = make_map()

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
