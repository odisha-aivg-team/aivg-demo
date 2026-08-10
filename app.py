import streamlit as st
import pandas as pd
import datetime
import urllib.parse

# ---------------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------------
st.set_page_config(
    page_title="AIVG - AI Vigilance Grid",
    page_icon="🛡️",
    layout="wide"
)

# ---------------------------------------------------------
# HEADER & TITLE AREA
# ---------------------------------------------------------
st.title("🛡️ AI Vigilance Grid (AIVG)")
st.caption("AI-Powered Automatic Corruption Inquiry System | Governance Command Center")

st.markdown("---")

# Create tabs for Dashboard & Mobile Gateway
tab_dashboard, tab_mobile = st.tabs(["💻 Master Vigilance Dashboard", "📱 Mobile Field Gateway"])

# =========================================================
# TAB 1: MASTER VIGILANCE DASHBOARD (LAPTOP DISPLAY)
# =========================================================
with tab_dashboard:
    st.header("📍 Zone A: Site Work Progress & Attendance Tracker")
    
    # Overview Metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Active Sites", "12")
    m2.metric("Total Registered Workers", "250")
    m3.metric("Present Today", "215")
    m4.metric("Flagged Anomalies", "2", delta="Active Alerts", delta_color="inverse")
    
    st.markdown("### 📊 Real-Time Worker Attendance vs. Physical Site Progress")
    
    # Sample Site Data
    site_data = {
        "Worker ID": ["WRK_101", "WRK_102", "WRK_103", "WRK_104", "WRK_105"],
        "Worker Name": ["Ramesh Mohanty", "Suresh Panda", "Anil Swain", "Bikash Sahoo", "Prakash Rout"],
        "Attendance Days (Logged)": [25, 24, 22, 10, 26],
        "Physical Progress (%)": [30, 85, 90, 45, 28],
        "Disbursement Amount (₹)": [18000, 17200, 16000, 7500, 19000]
    }
    
    df = pd.DataFrame(site_data)
    
    # Highlighting Logic for Anomalies (Physical Progress < 50% despite high attendance)
    def highlight_anomalies(row):
        if row['Physical Progress (%)'] < 50 and row['Attendance Days (Logged)'] > 20:
            return ['background-color: #ffcccc; color: darkred; font-weight: bold'] * len(row)
        return [''] * len(row)
    
    st.dataframe(df.style.apply(highlight_anomalies, axis=1), use_container_width=True)
    
    # Automatic AI Anomaly Alert Trigger
    st.markdown("### 🚨 AI Fraud Risk Evaluation")
    
    # Check for anomalies in dataset
    anomalies_found = df[(df['Physical Progress (%)'] < 50) & (df['Attendance Days (Logged)'] > 20)]
    
    if not anomalies_found.empty:
        st.error("🚨 BIOMETRIC vs. WORK PROGRESS ANOMALY DETECTED")
        st.warning(f"⚠️ Flagged {len(anomalies_found)} worker records where logged attendance days exceed 20, but site physical progress is under 50%. High probability of inflated attendance/ghost worker records.")
        
        # Display flagged list
        st.write("**Flagged Records:**")
        st.table(anomalies_found[["Worker ID", "Worker Name", "Attendance Days (Logged)", "Physical Progress (%)"]])
        
        # WhatsApp Alert Dispatch Button
        phone_number = "919000000000"  # Replace with Vigilance Officer Phone Number
        message = f"🚨 *AIVG ALERT: BIOMETRIC vs WORK PROGRESS ANOMALY DETECTED*\n\nSite ID: SITE-GAJAPATI-01\nFlagged Records: {len(anomalies_found)}\nImmediate Vigilance Inquiry Recommended."
        encoded_message = urllib.parse.quote(message)
        whatsapp_url = f"https://api.whatsapp.com/send?phone={phone_number}&text={encoded_message}"
        
        st.link_button("📲 Dispatch Case File to Vigilance Officer (WhatsApp)", whatsapp_url)
    else:
        st.success("✅ All site worker records are consistent with physical progress.")

# =========================================================
# TAB 2: MOBILE FIELD GATEWAY (SMARTPHONE DISPLAY)
# =========================================================
with tab_mobile:
    st.header("📱 Field Worker Biometric & Mobile Check-In")
    st.info("Use this tab on your smartphone to simulate live worker verification at the construction site entrance.")
    
    col_m1, col_m2 = st.columns([1, 1])
    
    with col_m1:
        st.subheader("1. Worker Verification Gateway")
        input_worker = st.text_input("Enter Worker ID:", value="WRK_101", key="mobile_id")
        
        # Biometric Touch Sensor Simulation
        if st.button("🔴 Touch Sensor to Scan Fingerprint", use_container_width=True):
            st.success(f"✅ Biometric Match Confirmed for {input_worker}!")
            st.metric("Time-In Timestamp", datetime.datetime.now().strftime("%H:%M:%S"))
        
        st.write("---")
        
        # Camera Capture Tool
        st.subheader("2. Facial / ID Photo Capture")
        picture = st.camera_input("Take Worker Photo / Scan ID Card")
        
        if picture:
            st.success(f"✅ Photo Captured & Geotagged for {input_worker}!")
            st.image(picture, caption="Verified Verification Record", width=220)
            
    with col_m2:
        st.subheader("📊 Live Site Attendance Counter")
        st.metric("Total Site Workers", "25")
        st.metric("Verified Present Today", "22", delta="+1 Just Logged")
        st.metric("Unverified / Absent", "3", delta="-1 Alert", delta_color="inverse")
        
        st.markdown("---")
        st.markdown("#### 🏛️ Station Status: **ONLINE**")
        st.caption("Connected to State Vigilance Command & Monitoring Hub")
        
        
        
    
    
    
    
        
        
        
    
  
