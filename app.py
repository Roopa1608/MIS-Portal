import streamlit as st
import pandas as pd

st.set_page_config(page_title="MIS Attendance Portal", layout="centered")
st.title("📊 Real-Time MIS & Attendance Portal")

@st.cache_data(ttl=60) 
def load_data():
    # Your updated, real-world Google Sheet CSV link
    sheet_url = "https://docs.google.com/spreadsheets/d/12xRSl91R6N-_LjwP1DNxpmgqKFspQMA70mPvMWWY_TI/export?format=csv&gid=0"
    return pd.read_csv(sheet_url)

df = load_data()

# Updated to match the new column 'Empoyee ID'
search_input = st.text_input("Enter Employee ID:", max_chars=15)

if search_input:
    # Filter using the exact spelling from your sheet
    employee_data = df[df['Empoyee ID'] == search_input.upper()]
    
    if not employee_data.empty:
        # Pulling data using your new headers
        name = employee_data.iloc[0]['NAME']
        doj = employee_data.iloc[0]['DOJ']
        designation = employee_data.iloc[0]['DESIGNATION']
        status = employee_data.iloc[0]['CURRENT STATUS']
        
        # New Attendance Metrics
        present = employee_data.iloc[0]['P']
        total = employee_data.iloc[0]['Total']
        payable_days = employee_data.iloc[0]['Payable Days']
        
        # Calculate percentage (using a try/except block to prevent division by zero errors)
        try:
            attendance_pct = round((float(present) / float(total)) * 100, 1)
        except:
            attendance_pct = 0.0
        
        # Displaying the Dashboard
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
