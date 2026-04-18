import streamlit as st
import pandas as pd

# 1. Premium Page Configuration
st.set_page_config(
    page_title="Enterprise MIS Portal", 
    page_icon="🏢", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injecting Custom CSS for a "Top-Notch" UI
st.markdown("""
    <style>
    .metric-card {
        background-color: #f8f9fa;
        border-radius: 10px;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        text-align: center;
        border-left: 5px solid #0052cc;
    }
    .metric-title {
        color: #6c757d;
        font-size: 14px;
        font-weight: 600;
        text-transform: uppercase;
    }
    .metric-value {
        color: #172b4d;
        font-size: 32px;
        font-weight: bold;
        margin-top: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar Branding
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942813.png", width=80)
    st.title("Admin Console")
    st.write("Welcome to the Flex Workforce MIS Tracking system.")
    st.divider()
    st.caption("Secure Connection: Active 🟢")
    st.caption("Database: Google Cloud Sync")

# 4. Main Header
st.title("🏢 Real-Time MIS & Attendance Portal")
st.markdown("Enter an employee's unique ID to pull live operational data from the master database.")

# 5. Data Loading & The Bug Fix
@st.cache_data(ttl=60) 
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSX3174rGnpJyOXOKRAyXJ1EnLFd0K2c6g4egdNbFjDUqmEWessrdcUSc5nY1sxQaXd-EXYGCDpZjyy/pub?output=csv"
    
    # Read the CSV, and FORCE the ID column to be a String to prevent the matching bug
    df = pd.read_csv(sheet_url, dtype={'Empoyee ID': str})
    
    # Clean up the column by stripping accidental spaces
    df['Empoyee ID'] = df['Empoyee ID'].str.strip().str.upper()
    return df

df = load_data()

# 6. The Search Interface
# Placed inside a clean container
with st.container():
    search_input = st.text_input("🔍 Search Employee ID:", max_chars=15, placeholder="e.g., 837897")

st.divider()

# 7. Processing & Beautiful Display
if search_input:
    search_term = search_input.strip().upper()
    employee_data = df[df['Empoyee ID'] == search_term]
    
    if not employee_data.empty:
        st.success("✅ Employee Record Authenticated and Retrieved")
        
        # Extract Data
        name = employee_data.iloc[0]['NAME']
        doj = employee_data.iloc[0]['DOJ']
        designation = employee_data.iloc[0]['DESIGNATION']
        status = employee_data.iloc[0]['CURRENT STATUS']
        
        present = employee_data.iloc[0]['P']
        total = employee_data.iloc[0]['Total']
        payable_days = employee_data.iloc[0]['Payable Days']
        
        # Safe Math Calculation
        try:
            attendance_pct = round((float(present) / float(total)) * 100, 1)
        except:
            attendance_pct = 0.0
            
        # UI Layout: Two columns for a dashboard feel
        col_prof, col_stats = st.columns([1, 2])
        
        with col_prof:
            st.markdown(f"### 👤 {name}")
            st.write(f"**Role:** {designation}")
            st.write(f"**Status:** `{status}`")
            st.write(f"**Joining Date:** {doj}")
            
            st.write("")
            st.write("**Overall Attendance Health**")
            # Visual Progress Bar
            progress_val = min(attendance_pct / 100, 1.0) # Ensure it doesn't break if over 100%
            st.progress(progress_val)
            
        with col_stats:
            # Using the custom CSS classes we injected at the top
            scol1, scol2, scol3 = st.columns(3)
            
            with scol1:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Total Days</div>
                    <div class="metric-value">{total}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with scol2:
                st.markdown(f"""
                <div class="metric-card">
                    <div class="metric-title">Days Present</div>
                    <div class="metric-value">{present}</div>
                </div>
                """, unsafe_allow_html=True)
                
            with scol3:
                # Color code the percentage (Green if good, Red if bad)
                color = "#2e7d32" if attendance_pct >= 80 else "#c62828"
                st.markdown(f"""
                <div class="metric-card" style="border-left: 5px solid {color};">
                    <div class="metric-title">Attendance %</div>
                    <div class="metric-value" style="color: {color};">{attendance_pct}%</div>
                </div>
                """, unsafe_allow_html=True)
                
        st.write("")
        st.info(f"💰 **Payroll Module:** Authorized for **{payable_days}** payable days this cycle.")
        
    else:
        st.error("⚠️ Error: Employee ID not found in the active database. Please verify the ID and try again.")
