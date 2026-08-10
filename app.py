import streamlit as st
import pandas as pd

# Page setup
st.set_page_config(page_title="AI Vigilance Grid", layout="wide")

st.title("🛡️ AI Vigilance Grid (AIVG)")
st.caption("AI-Powered Automatic Corruption Inquiry System")

# ---------------------------------------------------------
# COLUMN WIDTHS: [3, 1] sets 75% for table, 25% for alert panel
# Change to [2, 1] or [4, 1] if you want to tweak side spacing
# ---------------------------------------------------------
col_main, col_side = st.columns([3, 1])

with col_main:
    st.subheader("📊 Site Work Progress & Attendance Tracker")
    
    # Sample Data
    data = {
        "Worker ID": ["WRK_101", "WRK_102", "WRK_103"],
        "Worker Name": ["Ramesh Mohanty", "Suresh Panda", "Anil Swain"],
        "Attendance Days": [25, 24, 22],
        "Physical Progress (%)": [30, 85, 90]
    }
    df = pd.DataFrame(data)
    
    # Display full-width table
    st.dataframe(df, use_container_width=True)

with col_side:
    st.subheader("🚨 Vigilance Panel")
    
    # Logic check for worker anomalies
    for index, row in df.iterrows():
        attendance_days = row["Attendance Days"]
        physical_progress = row["Physical Progress (%)"]
        
        # Fixed syntax logic (no quotes wrapping the if-statement)
        if physical_progress < 50 and attendance_days > 20:
            st.error("🚨 BIOMETRIC vs. WORK PROGRESS ANOMALY DETECTED")
            st.warning(f"Worker {row['Worker ID']} ({row['Worker Name']}): High attendance ({attendance_days} days) but low physical progress ({physical_progress}%).")
            
        
        
        
    
    
    
    
        
        
        
    
  
