import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px

st.set_page_config(page_title="graphs")
st.title("Charts")

uploaded_file = st.file_uploader("Choose an Excel file", type=["xlsx", "xls"])

if uploaded_file is not None:
        # Read Excel file
        xls = pd.ExcelFile(uploaded_file)
        sheet_names = xls.sheet_names

        # Show the data in the app
        st.write("Data Preview:")

        # User selects the Excel sheet
        selected_sheet = st.selectbox("Select Excel Sheet", sheet_names)
        df = pd.read_excel(uploaded_file, sheet_name=selected_sheet)
        
        st.write("Data Preview:")
        st.write(df.head())
        
        # st.write(df.dtypes)
        
        date_col = st.selectbox("Select x-axis column", df.columns)
        
        data_cols = st.multiselect("Select Data Columns", df.columns, default=df.columns[3])
        # data_col = "SOUTH LAeq [dB]"
        
        
        
        # User selects the date range
        min_date, max_date = df[date_col].min(), df[date_col].max()
        col1, col2 = st.columns(2)
        start_date = col1.date_input("Start Date", min_date, min_value=min_date, max_value=max_date)
        end_date = col2.date_input("End Date", max_date, min_value=min_date, max_value=max_date)

        st.write(df[[date_col]].head())
    
        if st.button("Generate Time Series Graph"):
            if data_cols:
                # Filter data based on selected date range
                mask = (df[date_col] >= pd.to_datetime(start_date)) & (df[date_col] <= pd.to_datetime(end_date))
                filtered_df = df.loc[mask]

                # Create the plot using Plotly
                fig = px.line(filtered_df, x=date_col, y=data_cols, title="Time Series Graph")
                fig.update_xaxes(title_text=date_col)
                for data_col in data_cols:
                    fig.update_yaxes(title_text=data_col, secondary_y=True if data_col != data_cols[0] else False)

                # Display the plot
                st.plotly_chart(fig)
            else:
                st.error("Please select at least one data column.")
    
        
            # Display the plot
            st.plotly_chart(fig)