import streamlit as st
import pydeck as pdk
import requests

st.set_page_config(page_title="Globe Weather MVP", page_icon="🌍", layout="wide")

st.title("🌍 Globe + Live Weather (MVP)")
st.caption("Smallest working globe app on Streamlit Free")

# ---------------------------
# Country list (small set)
# ---------------------------
COUNTRIES = {
    "USA": (38.9, -77.0),
    "India": (28.6, 77.2),
    "UK": (51.5, -0.1),
    "Japan": (35.6, 139.7),
    "Australia": (-35.3, 149.1)
}

country = st.selectbox("Select Country", COUNTRIES.keys())
lat, lon = COUNTRIES[country]

# ---------------------------
# Weather (no API key)
# ---------------------------
@st.cache_data(ttl=900)
def get_weather(lat, lon):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current_weather=true"
    )
    return requests.get(url).json()["current_weather"]

weather = get_weather(lat, lon)

# ---------------------------
# 3D Globe (NO click handler)
# ---------------------------
view_state = pdk.ViewState(
    latitude=lat,
    longitude=lon,
    zoom=0.9,
)

deck = pdk.Deck(
    views=[pdk.View(type="GlobeView")],
    initial_view_state=view_state,
    map_style=None,
)

st.pydeck_chart(deck)

# ---------------------------
# Weather Display
# ---------------------------
st.subheader(f"🌦️ Live Weather — {country}")
st.write(f"**Temperature:** {weather['temperature']} °C")
st.write(f"**Wind Speed:** {weather['windspeed']} km/h")

st.caption("Weather: Open-Meteo | Globe: deck.gl")
