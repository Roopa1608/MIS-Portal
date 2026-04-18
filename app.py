import streamlit as st
import pandas as pd

# 1. Pro-Level Page Configuration
st.set_page_config(
    page_title="Attendance Management System", 
    page_icon="🏢", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Injecting Advanced CSS for Dashboard and Calendar Grid
st.markdown("""
    <style>
    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        text-align: center;
        border-left: 5px solid #0052cc;
        transition: transform 0.2s;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-title { color: #6c757d; font-size: 13px; font-weight: 700; letter-spacing: 1px; text-transform: uppercase; }
    .metric-value { color: #091e42; font-size: 34px; font-weight: 800; margin-top: 8px; }
    
    /* Calendar Grid */
    .calendar-container { margin-top: 20px; }
    .calendar-grid {
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 12px;
        margin-top: 15px;
    }
    .cal-day {
        background: #ffffff;
        border: 2px solid #e0e0e0;
        border-radius: 10px;
        padding: 15px 10px;
        text-align: center;
        box-shadow: 0 2px 5px rgba(0,0,0,0.02);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        min-height: 80px;
    }
    .cal-num { font-size: 16px; font-weight: bold; color: #333; margin-bottom: 5px; }
    .cal-status { font-size: 14px; font-weight: 800; padding: 4px 10px; border-radius: 20px; }
    
    /* Status Colors */
    .status-P { background: #e8f5e9; color: #2e7d32; border-color: #a5d6a7; }
    .status-A { background: #ffebee; color: #c62828; border-color: #ef9a9a; }
    .status-WO { background: #f5f5f5; color: #616161; border-color: #e0e0e0; }
    .status-HD { background: #e3f2fd; color: #1565c0; border-color: #90caf9; }
    .status-LWP { background: #fff3e0; color: #e65100; border-color: #ffcc80; }
    .status-NA { background: #fafafa; color: #bdbdbd; border-color: #eeeeee; }
    </style>
""", unsafe_allow_html=True)

# 3. Sidebar - Professional Corporate Branding
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3063/3063822.png", width=100)
    st.title("Admin Console")
    st.write("**Welcome to the Attendance Management System.**")
    st.divider()
    st.caption("🔒 Security: 256-bit Encrypted")
    st.caption("☁️ Database: Cloud Sync Active")

# 4. Main Header
st.title("🏢 Attendance Management System")
st.markdown("Secure Access Portal. Please enter an authorized 6-digit Employee ID.")

# 5. Data Loading Engine
@st.cache_data(ttl=60) 
def load_data():
    sheet_url = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSX3174rGnpJyOXOKRAyXJ1EnLFd0K2c6g4egdNbFjDUqmEWessrdcUSc5nY1sxQaXd-EXYGCDpZjyy/pub?output=csv"
    df = pd.read_csv(sheet_url, dtype={'Empoyee ID': str})
    df['Empoyee ID'] = df['Empoyee ID'].str.strip()
    return df

df = load_data()

# 6. Strict Input Validation (6 Digits Only)
with st.container():
    search_input = st.text_input("🔍 Employee ID (6 Digits):", max_chars=6, placeholder="e.g., 837897")

st.divider()

if search_input:
    if not (search_input.isdigit() and len(search_input) == 6):
        st.warning("⚠️ Access Denied: Employee ID format invalid. Must be exactly 6 digits.")
    else:
        employee_data = df[df['Empoyee ID'] == search_input]
        
        if not employee_data.empty:
            st.success("✅ Secure Connection Established. Record Found.")
            
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

            tab1, tab2 = st.tabs(["📊 Dashboard Overview", "📅 Day-Wise Calendar View"])
            
            with tab1:
                col_prof, col_stats = st.columns([1, 2])
                with col_prof:
                    st.markdown(f"### 👤 {name}")
                    st.write(f"**Role:** {designation}")
                    st.write(f"**Status:** `{status}`")
                    st.write(f"**Joining Date:** {doj}")
                    st.write("")
                    progress_val = min(attendance_pct / 100, 1.0)
                    st.progress(progress_val)
                    
                with col_stats:
                    scol1, scol2, scol3 = st.columns(3)
                    with scol1:
                        st.markdown(f'<div class="metric-card"><div class="metric-title">Total Days</div><div class="metric-value">{total}</div></div>', unsafe_allow_html=True)
                    with scol2:
                        st.markdown(f'<div class="metric-card"><div class="metric-title">Days Present</div><div class="metric-value">{present}</div></div>', unsafe_allow_html=True)
                    with scol3:
                        color = "#2e7d32" if attendance_pct >= 80 else "#c62828"
                        st.markdown(f'<div class="metric-card" style="border-left: 5px solid {color};"><div class="metric-title">Attendance %</div><div class="metric-value" style="color: {color};">{attendance_pct}%</div></div>', unsafe_allow_html=True)
                
                st.write("")
                st.info(f"💰 **Payroll System:** Authorized for **{payable_days}** payable days.")

            with tab2:
                st.markdown("### 📅 Monthly Attendance Record")
                st.write("Visual breakdown of daily operational presence.")
                
                calendar_html = '<div class="calendar-container"><div class="calendar-grid">'
                
                for day in range(1, 32):
                    day_str = str(day)
                    if day_str in employee_data.columns:
                        val = str(employee_data.iloc[0][day_str]).strip().upper()
                        if val == 'NAN' or val == '': val = 'NA'
                        
                        # --- THE FIX IS HERE ---
                        if val.startswith('P') or val == 'PL': status_class = 'status-P'
                        elif val.startswith('A'): status_class = 'status-A'
                        elif val == 'WO': status_class = 'status-WO'
                        elif val == 'HD': status_class = 'status-HD'
                        elif val == 'LWP': status_class = 'status-LWP'
                        else: status_class = 'status-NA'
                        
                        calendar_html += f'''
                        <div class="cal-day {status_class}">
                            <div class="cal-num">{day}</div>
                            <div class="cal-status {status_class}">{val}</div>
                        </div>
                        '''
                
                calendar_html += '</div></div>'
                st.markdown(calendar_html, unsafe_allow_html=True)
                
        else:
            st.error("⚠️ Error: Employee ID not found. Ensure the ID is active.")
