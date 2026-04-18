import streamlit as st
import pandas as pd

st.set_page_config(page_title="MIS Attendance Portal", layout="centered")
st.title("📊 Real-Time MIS & Attendance Portal")

@st.cache_data(ttl=60) 
def load_data():
    # Your fully unblocked, published Google Sheet CSV link
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSX3174rGnpJyOXOKRAyXJ1EnLFd0K2c6g4egdNbFjDUqmEWessrdcUSc5nY1sxQaXd-EXYGCDpZjyy/pub?output=csv"
    return pd.read_csv(sheet_url)

df = load_data()

# Using the column header exactly as it appears in your sheet
search_input = st.text_input("Enter Employee ID:", max_chars=15)

if search_input:
    # Filter using the exact spelling
    employee_data = df[df['Empoyee ID'] == search_input.upper()]
    
    if not employee_data.empty:
        name = employee_data.iloc[0]['NAME']
        doj = employee_data.iloc[0]['DOJ']
        designation = employee_data.iloc[0]['DESIGNATION']
        status = employee_data.iloc[0]['CURRENT STATUS']
        
        present = employee_data.iloc[0]['P']
        total = employee_data.iloc[0]['Total']
        payable_days = employee_data.iloc[0]['Payable Days']
        
        try:
            attendance_pct = round((float(present) / float(total)) * 100, 1)
        except:
            attendance_pct = 0.0
        
        st.subheader(f"Profile: {name}")
        st.write(f"**Designation:** {designation} | **Status:** {status}")
        st.write(f"**Date of Joining:** {doj}")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Days", total)
        col2.metric("Days Present (P)", present)
        col3.metric("Attendance %", f"{attendance_pct}%")
        
        st.write("---")
        st.metric("Total Payable Days", payable_days)
        
    else:
        st.error("Error: Employee ID not found in the active database.")
