# # pages/1_Analysis.py
# import streamlit as st
# import pandas as pd
# from utils import load_data # Import the cached function
#
# st.title("Analysis of your data")
#
# # File uploader within a container
# # 'key' is important if you have multiple file_uploaders on different pages
# # or if you want to reset its state.
# uploaded_files = st.container(border=True).file_uploader(
#     label="Upload your data",
#     type=["csv", "xlsx"],
#     accept_multiple_files=True,
#     key="analysis_file_uploader"
# )
#
# # Update session state with the current list of uploaded files
# if uploaded_files:
#     # This stores the UploadedFile objects in session_state.
#     # The load_data function will use these objects as input for caching.
#     st.session_state['uploaded_files_list'] = uploaded_files
#     st.success(f"Successfully uploaded {len(uploaded_files)} file(s).")
# else:
#     # If the user clears the uploader, also clear session state
#     if st.session_state['uploaded_files_list']:
#         st.session_state['uploaded_files_list'] = []
#         st.info("No files currently uploaded.")
#
# st.markdown("---")
# st.subheader("Preview of Uploaded Data:")
#
# if 'uploaded_files_list' not in st.session_state:
#     st.session_state['uploaded_files_list'] = []
#
# if st.session_state['uploaded_files_list']:
#     for uploaded_file in st.session_state['uploaded_files_list']:
#         with st.expander(f"Preview: {uploaded_file.name}"):
#             df = load_data(uploaded_file) # Calls the cached function
#             if df is not None:
#                 st.dataframe(df)
#                 # You can't use x_label/y_label directly here for st.line_chart.
#                 # You need to specify column names from your DataFrame.
#                 # Example: Assuming 'Year' and 'Value' columns exist for a line chart.
#                 # if 'Year' in df.columns and 'Value' in df.columns:
#                 #     st.line_chart(df, x='Year', y='Value')
#                 # else:
#                 #     st.info("Line chart requires 'Year' and 'Value' columns for example.")
#             else:
#                 st.warning(f"Could not load data for {uploaded_file.name}.")
# else:
#     st.info("Upload files using the uploader above to see a preview.")

# pages/1_Analysis.py
import streamlit as st
import pandas as pd

# Import the cached function from utils.py
# Assuming utils.py is in the parent directory of 'pages' or at the root of your app.
# Adjust the import path if your 'utils.py' is located elsewhere.
try:
    from utils import load_data
except ImportError:
    st.error("Could not import 'load_data' from 'utils.py'. Please ensure 'utils.py' is accessible.")
    st.stop() # Stop execution if a critical import fails

st.title("Analysis of your data")

# Initialize session state for uploaded files list if not already present.
# This ensures 'uploaded_files_list' always exists before being accessed.
if 'uploaded_files_list' not in st.session_state:
    st.session_state['uploaded_files_list'] = []

# File uploader within a container
uploaded_files_from_uploader = st.container(border=True).file_uploader(
    label="Upload your data",
    type=["csv", "xlsx"],
    accept_multiple_files=True,
    key="analysis_file_uploader" # Unique key for the widget
)

# Logic to update session state based on uploader activity
if uploaded_files_from_uploader:
    # If new files are uploaded, update the session state list
    # We compare the lists to avoid unnecessary re-assignments that might trigger re-runs
    if uploaded_files_from_uploader != st.session_state['uploaded_files_list']:
        st.session_state['uploaded_files_list'] = uploaded_files_from_uploader
        st.success(f"Successfully uploaded {len(uploaded_files_from_uploader)} file(s).")
else:
    # If the uploader is empty (e.g., user cleared it or no files selected initially)
    # and there were previously uploaded files in session state, clear them.
    if st.session_state['uploaded_files_list']:
        st.session_state['uploaded_files_list'] = []
        st.info("Files cleared. Please upload for analysis.")
    else:
        # This is the initial state or when no files are currently selected
        st.info("Please upload for analysis.")


st.markdown("---")
st.subheader("Preview of Uploaded Data:")

# Display preview of files currently in session state
if st.session_state['uploaded_files_list']:
    for uploaded_file in st.session_state['uploaded_files_list']:
        with st.expander(f"Preview: {uploaded_file.name}"):
            df = load_data(uploaded_file) # Calls the cached function
            if df is not None:
                st.dataframe(df)
                # You can add your chart examples here if desired, similar to Revenue page
                # For example:
                # if 'Year' in df.columns and 'Value' in df.columns:
                #     st.line_chart(df, x='Year', y='Value')
                # else:
                #     st.info("Line chart requires 'Year' and 'Value' columns for example.")
            else:
                st.warning(f"Could not load data for {uploaded_file.name}. Please check file format.")
else:
    # This message appears if st.session_state['uploaded_files_list'] is empty
    st.info("No data to preview. Please upload for analysis.")

