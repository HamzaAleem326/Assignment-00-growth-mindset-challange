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
data_uploader = st.file_uploader("Upload you data in ecxel or csv format",type=["cvs","xlsx"],accept_multiple_files=(True))
if data_uploader:
    for file in data_uploader:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == "csv":
            df = pd.read_csv(file)
        elif file_ext == "xlsx":
            df = pd.read_excel(file)
        else: 
            st.error(f"unsupplrted file type: {file_ext}")
            continue

        #details
        st.write("Dataframe Preview")
        st.dataframe(df.head())
        # data cleaning
        st.subheader("Data cleaning types")
        if st.checkbox(f"Clear from {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove duplicates for : {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("Removed")

            with col2:
                if st.button(f"Fill missing values in {file.name}"):
                    numeric_cols = df.select_dtypes(includes=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("Missing values filled")

        st.subheader("select columns to keep")
        columns = st.multiselect(f"Choose columns in {file.name}",df.columns,default=df.colums)
        df = df[columns]

        # visualization
        st.subheader("Visualization of you data here")
        if st.checkbox(f"Visualization from {file.name}"):
            st.bar_chart(df.select_dtypes(include='numbers').iloc[:, :2])

        # conversion types

        st.subheader("conversion types")
        conversion_type = st.radio(f"Convert{file.name =} to:", ["Cvs","Excel"],key=file.name)
        if st.button(f"Convert{file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to.csv(buffer, index= False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to.to_excel(buffer, index=False)
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocuments.spreadsheet.sheet"
            buffer.seek(0)

            st.download_button(
                label=f"Download {file.name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )
st.success("files processed successfully")



