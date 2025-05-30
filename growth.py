import streamlit as st
import pandas as pd
import os
from io import BytesIO

st.set_page_config(page_title="Data Purifier",layout='wide')
# css
st.markdown(
"""
<style>
.stApp{
background-color: grey;
}
</style>
""",
unsafe_allow_html=True
)
# information
st.title("Data Purifier")
st.write("Purify your Data with Data Analysis, Automated Data Cleaning and Automated Data Preprocessing along with data visualization")
# Data Uploader
data_uploader = st.file_uploader("Upload you data in excel or csv format", type=["csv", "xlsx"], accept_multiple_files=True)  # Fixed typos: "ecxel"->"excel", "cvs"->"csv", removed extra parentheses
if data_uploader:
    for file in data_uploader:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":  # Added dot for correct extension
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file)
        else: 
            st.error(f"unsupported file type: {file_ext}")  # Fixed typo: "unsupplrted"->"unsupported"
            continue

        #details
        st.write("Here's a quick preview of your data:")
        st.dataframe(df.head())

        # data cleaning
        st.subheader("Data Cleaning Options")
        if st.checkbox(f"Clean data from {file.name}?"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates in {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("Duplicates removed!")

            with col2:
                if st.button(f"Fill missing values in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("Missing values filled with column means.")

        st.subheader("Select Columns to Keep")
        columns = st.multiselect(
            f"Choose which columns to keep from {file.name}",
            df.columns,
            default=list(df.columns)
        )
        df = df[columns]

        # visualization
        st.subheader("Visualize Your Data")
        if st.checkbox(f"Show bar chart for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:, :2])

        # conversion types
        st.subheader("Download Your Data")
        conversion_type = st.radio(
            f"Convert {file.name} to:",
            ["CSV", "Excel"],
            key=file.name
        )
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"
            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
    st.success("Files processed successfully")  # Moved inside the if-block so it only shows after files are processed



