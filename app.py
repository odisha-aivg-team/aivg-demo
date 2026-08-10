import streamlit as st
import pandas as pd
import datetime

# ---------------------------------------------------------
# PAGE CONFIGURATION & HEADER
# ---------------------------------------------------------
st.set_page_config(
    page_title="AI Vigilance Grid (AIVG)",
    page_icon="🛡️",
    layout="wide"
)

st.title("🛡️ AI Vigilance Grid (AIVG)")
st.caption("AI-Powered Automatic Corruption Inquiry System | Odisha Adarsha Vidyalaya")
st.markdown("---")

# =========================================================
# BOX 1: SITE WORK PROGRESS & ATTENDANCE TRACKER
# =========================================================
st.header("📦 Box 1: Site Work Progress & Attendance Tracker")

col1_main, col1_side = st.columns([3, 1])

with col1_main:
    data_box1 = {
        "Worker ID": ["WRK_101", "WRK_102", "WRK_103", "WRK_104"],
        "Worker Name": ["Ramesh Mohanty", "Suresh Panda", "Anil Swain", "Bikash Sahoo"],
        "Attendance Days": [25, 24, 22, 10],
        "Physical Progress (%)": [30, 85, 90, 45],
        "Disbursement (₹)": [18000, 17200, 16000, 7500]
    }
    df1 = pd.DataFrame(data_box1)
    st.dataframe(df1, use_container_width=True)

with col1_side:
    st.subheader("🚨 Vigilance Alert")
    for idx, row in df1.iterrows():
        attendance_days = row["Attendance Days"]
        physical_progress = row["Physical Progress (%)"]
        
        # Line 54: Clean conditional check without wrapping quotes
        if physical_progress < 50 and attendance_days > 20:
            st.error("🚨 BIOMETRIC vs. WORK PROGRESS ANOMALY DETECTED")
            st.warning(f"Flagged {row['Worker ID']} ({row['Worker Name']}): High attendance ({attendance_days} days) but site progress is under {physical_progress}%.")

st.markdown("---")

# =========================================================
# BOX 2: PAYROLL & GHOST EMPLOYEE DETECTION
# =========================================================
st.header("📦 Box 2: Payroll & Ghost Employee Detection")

col2_main, col2_side = st.columns([3, 1])

with col2_main:
    data_box2 = {
        "Employee ID": ["EMP_201", "EMP_202", "EMP_203", "EMP_204"],
        "Name": ["Prakash Rout", "Kavita Das", "Manoj Tripathy", "Sunil Jena"],
        "Aadhaar Status": ["Verified", "Verified", "Unlinked / Duplicate", "Verified"],
        "Bank Account": ["SBIN0001", "SBIN0002", "SBIN0001 (Duplicate)", "SBIN0004"],
        "Monthly Salary (₹)": [45000, 48000, 45000, 42000]
    }
    df2 = pd.DataFrame(data_box2)
    st.dataframe(df2, use_container_width=True)

with col2_side:
    st.subheader("🚨 Payroll Alert")
    ghost_records = df2[df2["Aadhaar Status"].str.contains("Duplicate")]
    if not ghost_records.empty:
        st.error("🚨 DUPLICATE BANK ACCOUNT / UNLINKED AADHAAR DETECTED")
        st.warning("Potential ghost employee flagged in payroll processing.")

st.markdown("---")

# =========================================================
# BOX 3: EXTRA DISBURSEMENTS & FUNDS MONITORING
# =========================================================
st.header("📦 Box 3: Extra Disbursements & Emergency Fund Audit")

col3_main, col3_side = st.columns([3, 1])

with col3_main:
    data_box3 = {
        "Transaction ID": ["TXN_901", "TXN_902", "TXN_903"],
        "Purpose": ["Material Supply", "Emergency Contingency", "Equipment Hire"],
        "Approved Amount (₹)": [100000, 50000, 75000],
        "Disbursed Amount (₹)": [100000, 180000, 75000],
        "Approval Officer": ["Officer A", "Officer B", "Officer A"]
    }
    df3 = pd.DataFrame(data_box3)
    st.dataframe(df3, use_container_width=True)

with col3_side:
    st.subheader("🚨 Disbursement Alert")
    for idx, row in df3.iterrows():
        if row["Disbursed Amount (₹)"] > row["Approved Amount (₹)"]:
            st.error("🚨 UNAUTHORIZED BUDGET OVERRUN DETECTED")
            st.warning(f"Transaction {row['Transaction ID']} exceeds approved sanction by ₹{row['Disbursed Amount (₹)'] - row['Approved Amount (₹)']}.")

st.markdown("---")

# =========================================================
# BOX 4: WELFARE SCHEMES & BENEFICIARY AUDIT
# =========================================================
st.header("📦 Box 4: Welfare Schemes & Direct Benefit Transfer (DBT)")

col4_main, col4_side = st.columns([3, 1])

with col4_main:
    data_box4 = {
        "Scheme Name": ["Scholarship A", "Housing Grant B", "Agriculture Subsidy C"],
        "Total Beneficiaries": [1200, 450, 3100],
        "DBT Success Rate (%)": [98.5, 62.0, 99.1],
        "Flagged Duplicate Claims": [0, 38, 2]
    }
    df4 = pd.DataFrame(data_box4)
    st.dataframe(df4, use_container_width=True)

with col4_side:
    st.subheader("🚨 Scheme Audit")
    low_dbt = df4[df4["DBT Success Rate (%)"] < 80]
    if not low_dbt.empty:
        st.error("🚨 HIGH BENEFICIARY MISMATCH RISK")
        st.warning("Housing Grant B shows abnormal drop in successful direct transfers.")

st.markdown("---")

# =========================================================
# BOX 5: PROCUREMENT & TENDER FRAUD MONITORING
# =========================================================
st.header("📦 Box 5: Procurement & Bidding Pattern Analysis")

col5_main, col5_side = st.columns([3, 1])

with col5_main:
    data_box5 = {
        "Tender ID": ["TND_501", "TND_502", "TND_503"],
        "Project Name": ["School Building Renovation", "Smart Lab Equipment", "Road Construction"],
        "Bidders Count": [4, 2, 5],
        "IP Address Match": ["Unique", "SAME IP DETECTED (Collusion Risk)", "Unique"],
        "Winning Bid (₹)": [1200000, 850000, 4500000]
    }
    df5 = pd.DataFrame(data_box5)
    st.dataframe(df5, use_container_width=True)

with col5_side:
    st.subheader("🚨 Procurement Alert")
    collusion = df5[df5["IP Address Match"].str.contains("SAME IP")]
    if not collusion.empty:
        st.error("🚨 BIDDER COLLUSION DETECTED")
        st.warning("Multiple bid submissions received from identical IP addresses.")
        
    
            
        
        
        
    
    
    
    
        
        
        
    
  
