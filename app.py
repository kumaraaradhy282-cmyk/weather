import streamlit as st
import pydeck as pdk
import requests

st.set_page_config(page_title="Globe Weather MVP", page_icon="🌍", layout="wide")

st.title("🌍 Rotating Globe → Click to See Live Weather")
st.caption("Minimal MVP • Streamlit Free • No API keys")

# ---------------------------
# Weather Function (No API key)
# ---------------------------
def get_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}"
        "&current_weather=true"
    )
    return requests.get(url).json()["current_weather"]

# ---------------------------
# Click handling
# ---------------------------
if "click" not in st.session_state:
    st.session_state.click = None

def on_click(info):
    if info and "coordinate" in info:
        st.session_state.click = info["coordinate"]

# ---------------------------
# Globe (REAL 3D)
# ---------------------------
view_state = pdk.ViewState(
    latitude=0,
    longitude=0,
    zoom=0.8,
    bearing=0,
    pitch=0,
)

deck = pdk.Deck(
    views=[pdk.View(type="GlobeView")],
    initial_view_state=view_state,
    map_style=None,
    on_click=on_click,
)

st.pydeck_chart(deck)

# ---------------------------
# Weather Output
# ---------------------------
if st.session_state.click:
    lon, lat = st.session_state.click
    weather = get_weather(lat, lon)

    st.divider()
    st.subheader("🌦️ Live Weather at Selected Location")

    st.write(f"**Latitude:** {lat:.2f}")
    st.write(f"**Longitude:** {lon:.2f}")
    st.write(f"**Temperature:** {weather['temperature']} °C")
    st.write(f"**Wind Speed:** {weather['windspeed']} km/h")
    st.write(f"**Condition Code:** {weather['weathercode']}")

st.caption("Weather data: Open-Meteo • Globe: deck.gl")
