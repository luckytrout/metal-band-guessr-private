import streamlit as st
from streamlit.components.v1 import html
import folium
import pandas as pd
import random

from data_loader import load_metal_bands
from geo import resolve_origin


st.set_page_config(page_title="Guesser — Demo", layout="wide")
st.title("Guesser — Demo")

st.markdown(
    """
    This is a minimal demo page for the guessing-game feature.

    - Click "Pick random band" to choose a band from the dataset with a resolvable origin.
    - The map will center on the resolved country coordinates and place a marker.
    - This page is intentionally small: later we'll hide the true location and let the
      player guess by clicking on the map.
    """
)


def _first_nonempty(row, *cols):
    for c in cols:
        v = row.get(c)
        if isinstance(v, float) and pd.isna(v):
            continue
        if v is None:
            continue
        if isinstance(v, str) and v.strip() == "":
            continue
        return v
    return None


def make_map(center=(20, 0), zoom=2, debug_marker=False):
    m = folium.Map(location=list(center), zoom_start=zoom, tiles="OpenStreetMap")
    folium.TileLayer("CartoDB positron").add_to(m)
    folium.LatLngPopup().add_to(m)
    if debug_marker:
        folium.Marker(location=list(center), popup=folium.Popup("Debug center", max_width=200),
                      icon=folium.Icon(color='red')).add_to(m)
    return m


col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Demo controls")
    if 'selected' not in st.session_state:
        st.session_state.selected = None

    if st.button("Pick random band"):
        try:
            df = load_metal_bands()
            # shuffle and find first resolvable origin
            df_s = df.sample(frac=1)
            picked = None
            for _, row in df_s.iterrows():
                origin = _first_nonempty(row, "origin", "Origin", "Country", "country")
                if not origin or not isinstance(origin, str):
                    continue
                key, coords = resolve_origin(origin)
                if key and coords:
                    band = _first_nonempty(row, "band_name", "band", "Band Name", "Name", "name") or "<unknown>"
                    # extra metadata: genre, url, photo, status
                    genre = _first_nonempty(row, "Genre", "genre")
                    url = _first_nonempty(row, "URL", "url", "Link", "link")
                    photo = _first_nonempty(row, "Photo_URL", "photo_url", "Photo URL", "photo")
                    status = _first_nonempty(row, "Status", "status")
                    picked = {
                        "band": band,
                        "origin": origin,
                        "country_key": key,
                        "coords": coords,
                        "genre": genre,
                        "url": url,
                        "photo": photo,
                        "status": status,
                    }
                    break

            if picked:
                st.session_state.selected = picked
            else:
                st.warning("Could not find a resolvable band origin in the dataset.")
        except Exception as e:
            st.error(f"Error selecting band: {e}")

    if st.session_state.selected:
        sel = st.session_state.selected
        st.markdown(f"**Band:** {sel['band']}")
        st.write("**Origin (raw):**", sel['origin'])
        st.write("**Resolved key:**", sel['country_key'])
        if sel.get('genre'):
            st.write("**Genre:**", sel.get('genre'))
        if sel.get('status'):
            st.write("**Status:**", sel.get('status'))

        # show link if available
        if sel.get('url'):
            try:
                st.markdown(f"[Band page]({sel.get('url')})")
            except Exception:
                st.write("URL:", sel.get('url'))

        # show photo if available
        if sel.get('photo'):
            try:
                st.image(sel.get('photo'), width=220)
            except Exception:
                # image fetch/display may fail; fallback to printing URL
                st.write("Photo URL:", sel.get('photo'))

    debug = st.checkbox("Show debug center marker")

with col2:
    # default map
    center = (20, 0)
    zoom = 2
    if st.session_state.get('selected'):
        center = st.session_state['selected']['coords']
        zoom = 4

    m = make_map(center=center, zoom=zoom, debug_marker=debug)
    if st.session_state.get('selected'):
        lat, lon = st.session_state['selected']['coords']
        popup_html = f"<b>{st.session_state['selected']['band']}</b><br/>{st.session_state['selected']['origin']}"
        folium.Marker(location=[lat, lon], popup=folium.Popup(popup_html, max_width=300),
                      icon=folium.Icon(color='blue', icon='music')).add_to(m)

    m_html = m._repr_html_()
    html(m_html, height=650)


st.markdown("""
Next steps: hide the true location and capture user clicks to grade guesses, add scoring, and a UI
to cycle through rounds.
""")
