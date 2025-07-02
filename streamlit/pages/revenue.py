# pages/2_Revenue.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import io

# Initialize containers
loaded_dfs_dict = {}
generated_chart_images = {}

# Import utility modules
try:
    from utils import load_data
    from report import generate_reportlab_pdf
except ImportError as e:
    st.error(f"Import error: {e}")
    st.stop()

st.title("Revenue Optimization")
st.write("This page performs analysis on uploaded data.")

# Uploaded files session-state
if 'uploaded_files_list' not in st.session_state:
    st.session_state['uploaded_files_list'] = []

if st.session_state['uploaded_files_list']:
    st.subheader("Data from Uploaded Files:")

    for uploaded_file in st.session_state['uploaded_files_list']:
        st.write(f"### Processing: {uploaded_file.name}")
        df = load_data(uploaded_file)
        if df is None:
            st.warning(f"Could not load {uploaded_file.name}.")
            continue

        st.dataframe(df.head())
        cols = df.columns.tolist()

        # Charting input
        if len(cols) >= 2:
            x = st.selectbox(f"X-axis for chart ({uploaded_file.name})", cols, key=f"x_{uploaded_file.name}")
            y = st.selectbox(f"Y-axis for chart ({uploaded_file.name})", cols, key=f"y_{uploaded_file.name}")

            if x and y:
                chart_type = st.selectbox(
                    f"Chart type for {uploaded_file.name}",
                    ["Line", "Bar", "Area"],
                    key=f"chart_type_{uploaded_file.name}"
                )

                if chart_type == "Line":
                    st.line_chart(df, x=x, y=y)
                elif chart_type == "Bar":
                    st.bar_chart(df, x=x, y=y)
                else:
                    st.area_chart(df, x=x, y=y)

                # Save to buffer for PDF
                fig, ax = plt.subplots(figsize=(8, 4))
                if chart_type == "Line":
                    ax.plot(df[x], df[y])
                elif chart_type == "Bar":
                    ax.bar(df[x], df[y])
                else:
                    ax.fill_between(df[x], df[y], alpha=0.5)
                    ax.plot(df[x], df[y], color="blue")

                ax.set(xlabel=x, ylabel=y, title=f"{chart_type} of {y} vs {x}")
                plt.xticks(rotation=45, ha='right')
                plt.tight_layout()

                buf = io.BytesIO()
                plt.savefig(buf, format="png", bbox_inches="tight")
                plt.close(fig)
                generated_chart_images[f"{chart_type} ({y} vs {x}) for {uploaded_file.name}"] = buf

        loaded_dfs_dict[uploaded_file.name] = df
        st.markdown("---")

    # PDF Export
    if loaded_dfs_dict or generated_chart_images:
        if st.button("Download PDF Report"):
            with st.spinner("Generating PDF…"):
                pdf = generate_reportlab_pdf(loaded_dfs_dict, generated_chart_images)
                st.download_button("Download PDF", pdf, "analysis_report.pdf", "application/pdf")
            st.success("PDF created!")
    else:
        st.info("Upload files and select chart options to enable PDF report.")
else:
    st.info("No uploaded files. Please upload data via the 'Analysis' page.")
