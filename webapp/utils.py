import pandas as pd
import streamlit as st
import folium
from streamlit_folium import folium_static
from googletrans import Translator
from difflib import get_close_matches

from math import radians, sin, cos, sqrt, asin

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance in kilometers between two points 
    on the earth (specified in decimal degrees)
    """
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. 
    return c * r

# Constants
DATA_PATHS = {
    "streets": "data/street_data_staged.csv",
    "parking": "data/parking_data_staged.csv",
    "toilets": "data/toilets_data_staged.csv",
    "museums": "data/museum_data_staged.csv",
    "sports": "data/sports_data_staged.csv"
}

# Load datasets
data = pd.read_csv(DATA_PATHS["streets"])
data_parking = pd.read_csv(DATA_PATHS["parking"])
data_toilets = pd.read_csv(DATA_PATHS["toilets"])
data_museums = pd.read_csv(DATA_PATHS["museums"])
data_sports = pd.read_csv(DATA_PATHS["sports"])

# Utility functions
def translate_text(text, dest="en"):
    """Translates a given text to the target language."""
    translator = Translator()
    return translator.translate(text, dest=dest).text

def format_arrondissement(arr):
    """Formats arrondissement codes to match expected formats."""
    if len(arr) == 1:
        return "7500" + arr
    elif len(arr) == 2:
        return "750" + arr
    return arr


# Core functions
def get_street_data(street_name):
    """Returns information about a street, with suggestions if needed."""
    search_term = street_name.strip().upper()
    if search_term not in data["typo"].values:
        suggestions = get_close_matches(search_term, data["typo"].unique(), n=1, cutoff=0.7)
        if suggestions:
            return None, suggestions[0]
        else:
            return None, None
    street_data = data[data["typo"] == search_term]
    street_data.loc[:, "historique"] = street_data["historique"].apply(translate_text)
    street_data.loc[:, "orig"] = street_data["orig"].apply(translate_text)
    return street_data, None

def get_nearby_data_within_radius(data_source, street_coords, radius=1):
    street_lat, street_lon = street_coords
    data_source["Ylat"] = pd.to_numeric(data_source["Ylat"], errors="coerce")
    data_source["Xlong"] = pd.to_numeric(data_source["Xlong"], errors="coerce")
    data_source = data_source.dropna(subset=["Ylat", "Xlong"])
    data_source.loc[:, "distance"] = data_source.apply(
        lambda row: haversine(street_lon, street_lat,  row["Xlong"], row["Ylat"]),
        axis=1
    )
    radius = int(radius)
    data_source = data_source.copy()
    data_source["distance"] = data_source["distance"].astype(int)
    data_source = data_source.dropna(subset=["distance"])
    return data_source[data_source["distance"] <= radius]


def get_street_coordinates(street_name):
    """
    Get the coordinates (latitude, longitude) of a street from the dataset.
    """
    street_data = data[data["typo"].str.contains(street_name, case=False, na=False)]
    if street_data.empty:
        return None
    return street_data.iloc[0]["Ylat"], street_data.iloc[0]["Xlong"]

def display_map(data_source, lat_col, long_col, popup_generator, section, special_point=None, to_show = "adresse"):
    """
    Displays a Folium map with markers based on the data source.
    Optionally centers and highlights a special point.
    
    Args:
        data_source (pd.DataFrame): The data source containing marker information.
        lat_col (str): The name of the latitude column in the data source.
        long_col (str): The name of the longitude column in the data source.
        popup_generator (callable): A function to generate popups for markers.
        section (str): The section name for the map.
        special_point (tuple): Optional. A tuple of (latitude, longitude) for a special point to center on.
    """
    if data_source.empty:
        st.info(f"🚫 No nearby {section} found.")
        return None
    if special_point:
        center = special_point
    else:
        center = [data_source.iloc[0][lat_col], data_source.iloc[0][long_col]]

    m = folium.Map(location=center, zoom_start=15)

    for _, row in data_source.iterrows():
        popup = folium.Popup(popup_generator(row), max_width=300)
        folium.Marker(
            location=[row[lat_col], row[long_col]],
            popup=popup,
            tooltip=row[to_show]
        ).add_to(m)
    
    if special_point:
        folium.Marker(
            location=special_point,
            popup="📍 Your street",
            icon=folium.Icon(color="green", icon="star")
        ).add_to(m)
    
    folium_static(m)


def parking_popup(row):
    """Generates HTML content for parking markers."""
    return f"""
        <b>Address:</b> {row['adresse']}<br>
        <b>Free:</b> {row['gratuit']}<br>
        <b>Rate (1h):</b> {row['tarif_1h']} €<br>
        <b>Rate (2h):</b> {row['tarif_2h']} €<br>
        <b>Rate (3h):</b> {row['tarif_3h']} €<br>
        <b>Rate (4h):</b> {row['tarif_4h']} €<br>
        <b>Max Height:</b> {row['hauteur_max']} cm<br>
    """

def toilet_popup(row):
    """Generates HTML content for toilet markers."""
    return f"""
        <b>Accessible to disabled:</b> {row['ACCES_PMR']}<br>
        <b>Schedule:</b> {row['HORAIRE']}<br>
    """

def museum_popup(row):
    """Generates HTML content for museum markers."""
    return f"""
        <b>Name:</b> {row['name']}<br>
        <b>Address:</b> {row['adresse']}
    """

def sports_popup(row):
    """Generates HTML content for sports facility markers."""
    return f"""
        <b>Name:</b> {row['name']}<br>
    """
# Display functions
def display_street_info(street_data):
    """Displays detailed information about a street."""
    st.write(f"- **Historical Name:** {street_data['historique'].values[0]}")
    st.write(f"- **Original Name:** {street_data['orig'].values[0]}")
    st.write(f"- **District:** {street_data['arrdt'].values[0]}")
    st.write(f"- **Neighborhood:** {street_data['quartier'].values[0]}")

def display_parking_data(street_name, radius=1):
    street_coords = get_street_coordinates(street_name)
    if not street_coords:
        st.warning("Street not found.")
        return
    parking_data = get_nearby_data_within_radius(data_parking, street_coords, radius)
    display_map(parking_data, "Ylat", "Xlong", parking_popup, "parking", special_point=street_coords)

def display_toilet_data(street_name, radius=1):
    street_coords = get_street_coordinates(street_name)
    if not street_coords:
        st.warning("Street not found.")
        return
    toilet_data = get_nearby_data_within_radius(data_toilets, street_coords, radius)
    display_map(toilet_data, "Ylat", "Xlong", toilet_popup, "toilets", special_point=street_coords)

def display_museum_data(street_name, radius=1):
    street_coords = get_street_coordinates(street_name)
    if not street_coords:
        st.warning("Street not found.")
        return
    museum_data = get_nearby_data_within_radius(data_museums, street_coords, radius)
    display_map(museum_data, "Ylat", "Xlong", museum_popup, "museums", special_point=street_coords, to_show="name")

def display_sports_data(street_name, radius=1):
    street_coords = get_street_coordinates(street_name)
    if not street_coords:
        st.warning("Street not found.")
        return
    sports_data = get_nearby_data_within_radius(data_sports, street_coords, radius)
    display_map(sports_data, "Ylat", "Xlong", sports_popup, "sports", special_point=street_coords, to_show= "name")