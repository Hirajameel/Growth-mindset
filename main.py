import streamlit as st
import pandas as pd
from io import BytesIO

st.set_page_config(page_title="File Convertor & Cleaner", layout="wide")
st.title("File Convertor & Cleaner")
st.write("Upload your CSV and Excel Files to clean the data and convert formats effortlessly")

files = st.file_uploader("Upload CSV or Excel Files", type=["csv", "xlsx"], accept_multiple_files=True)

if files:
    for file in files:
        ext = file.name.split(".")[-1].lower()
        df = pd.read_csv(file) if ext == "csv" else pd.read_excel(file)

        st.subheader(f"{file.name} - Preview")
        st.dataframe(df.head())

        if st.checkbox(f"Fill Missing Values - {file.name}"):
            # Fill only numerical columns with mean
            numeric_cols = df.select_dtypes(include="number").columns
            df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
            st.success("Missing values filled successfully!")
            st.dataframe(df.head())

        selected_columns = st.multiselect(f"Select Columns - {file.name}", df.columns, default=df.columns)
        df = df[selected_columns]
        st.dataframe(df.head())

        if st.checkbox(f"Show Chart - {file.name}") and not df.select_dtypes(include="number").empty:
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        format_choice = st.radio(f"Convert {file.name} to:", ["CSV", "Excel"], key=file.name)

        # Download button
        towrite = BytesIO()
        if format_choice == "CSV":
            df.to_csv(towrite, index=False)
            st.download_button(label="Download as CSV", data=towrite.getvalue(), file_name=file.name.replace(ext, "csv"), mime="text/csv")
        else:
            with pd.ExcelWriter(towrite, engine='xlsxwriter') as writer:
                df.to_excel(writer, index=False, sheet_name='Sheet1')
            st.download_button(label="Download as Excel", data=towrite.getvalue(), file_name=file.name.replace(ext, "xlsx"), mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
