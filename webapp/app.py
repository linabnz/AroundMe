import streamlit as st
from utils import get_street_data, display_museum_data, display_parking_data, display_toilet_data, display_sports_data, display_street_info

st.markdown("""
    <style>
    body {
        background-color: #f4f4f9; /* Light neutral background */
    }
    .main-title {
        font-size: 40px;
        color: #8fbf9c; /* Slightly darker pastel green */
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    .sub-title {
        font-size: 24px;
        color: #f5a9a7; /* Slightly darker pastel pink */
        text-align: center;
        font-family: 'Arial', sans-serif;
    }
    .stButton>button {
        background-color: #8fbf9c; /* Slightly darker pastel green */
        color: white;
        border-radius: 10px;
        border: none;
        padding: 10px 20px;
        cursor: pointer;
    }
    .stButton>button:hover {
        background-color: #a8d5ba; /* Original pastel green for hover */
        color: white;
    }
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #8fbf9c; /* Slightly darker pastel green */
        color: white;
        text-align: center;
        padding: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)



# Titles
st.markdown('<h1 class="main-title">🌟 AroundMe</h1>', unsafe_allow_html=True)
st.markdown('<h2 class="sub-title">Explore Paris streets and nearby amenities</h2>', unsafe_allow_html=True)

# Session state initialization
if "suggestion" not in st.session_state:
    st.session_state.suggestion = None
if "current_input" not in st.session_state:
    st.session_state.current_input = None

# Input and search button layout
col1, col2 = st.columns([4, 1])
with col1:
    user_input = st.text_input("🔍 Enter a street name:", placeholder="Example: Champs-Élysées")
with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    search = st.button("Search")

def display_results(street_name):
    """Fetch and display results for a given street name."""
    # Fetch street data
    street_data, suggestion = get_street_data(street_name)
    st.session_state.suggestion = suggestion

    if street_data is not None:
        st.success(f"✅ Results for *{street_name}*:")  # Display results        
        # Display results in tabs
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📜 Street Details",
            "🚗 Nearby Parking",
            "🚻 Nearby Toilets",
            "🏛️ Nearby Museums",
            "🏀 Nearby Sports"
        ])

        with tab1:
            st.markdown("### Street Details")
            display_street_info(street_data)
            
        with tab2:
            st.markdown("### Nearby Parking")
            display_parking_data(street_name)
        with tab3:
            st.markdown("### Nearby Toilets")
            display_toilet_data(street_name)
        with tab4:
            st.markdown("### Nearby Museums")
            display_museum_data(street_name)
        with tab5:
            st.markdown("### Nearby Sports")
            display_sports_data(street_name)


# Search logic
if search and user_input.strip():
    st.session_state.current_input = user_input
    display_results(user_input)
elif search:
    st.error("❌ Please enter a street name to start the search.")

# Handle suggestion
if st.session_state.suggestion:
    if st.button(f"💡 Suggestion: Try with '{st.session_state.suggestion}'"):  
        display_results(st.session_state.suggestion)

# Footer
st.markdown('<div class="footer"><p>Powered by AroundMe - Explore Paris, One Street at a Time</p></div>', unsafe_allow_html=True)
