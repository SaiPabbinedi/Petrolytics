import streamlit as st
import pandas as pd
import numpy as np
from streamlit import container

# --- Custom CSS to hide only the 3-dots options menu and the footer ---
hide_streamlit_toolbar = """
    <style>
    #MainMenu {visibility: hidden;} /* Hides the old Streamlit menu (older versions) */
    footer {visibility: hidden;} /* Hides the "Made with Streamlit" footer */

    /* Targets specifically the 3-dots options button within the toolbar */
    button[data-testid="stOptionButton"] {
        display: none;
    }
    button[data-testid="stBaseButton-header"] {
        display: none;
    }
    </style>
    """
st.markdown(hide_streamlit_toolbar, unsafe_allow_html=True)

st.set_page_config(page_title="Dashboard")
st.title("Dashboard")

data = {
    "Name": ["Alice", "bob", "Coochie"],
    "Age": [41, 64, 43],
    "City": ["Visakhapatnam", "Hyderabad", "Bangalore"]
}

summary, gif = st.columns(2)
line, bar, area = st.columns(3)

with summary:
    st.container(border=True).write("This is a Petrolytics Dashboard with comprises of this services you can join use to enhance this data")
with gif:
    # Using a placeholder image URL, ensure it's accessible
    st.container(border=True).image("https://placehold.co/600x400/FF5733/FFFFFF?text=Dashboard+Graphic")

with line:
    with container(border=True):
        # Displaying a DataFrame from the 'data' dictionary
        st.write("Sample Data Table:")
        st.dataframe(data)

with bar:
    with container(border=True):
        st.write("Some Bar Chart goes here")
        # Example of a simple bar chart using the 'data'
        df_bar = pd.DataFrame(data)
        st.bar_chart(df_bar, x="Name", y="Age")

with area:
    with container(border=True):
        st.write("Some Area Chart goes here")
        # Example of a simple area chart using the 'data'
        df_area = pd.DataFrame(data)
        st.area_chart(df_area, x="Name", y="Age")


with st.container(border=True):
    st.write("OPEC Data")
    with st.expander("Details"):
        st.write('''
            This organization is for Petroleum.
            It plays a significant role in global oil markets.
        ''')
    # Displaying the DataFrame again for OPEC Data section
    st.dataframe(data)

