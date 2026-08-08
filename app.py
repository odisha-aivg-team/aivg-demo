import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Vigilance Grid (AIVG)", page_icon="🛡️")

st.title("🛡️ AI Vigilance Grid (AIVG)")
st.caption("Odiaprenuer 3.0 Smart Odisha Hackathon | Cyber Security from Corruption")

st.markdown("---")

# Sidebar navigation
menu = st.sidebar.selectbox("Select System Data Feed", ["Payroll & Salary Logs", "Tenders & Procurement"])

if menu == "Payroll & Salary Logs":
    st.header("📊 Module 1: Payroll & Beneficiary Audit")
    
    payroll_data = pd.DataFrame({
        'Employee ID': ['EMP_001', 'EMP_002', 'EMP_003', 'EMP_004 (Ghost Alert)'],
        'Name': ['Ramesh Mohanty', 'Sita Das', 'Prakash Naik', 'Unknown / Unverified'],
        'Biometric Status': ['Verified ✅', 'Verified ✅', 'Verified ✅', 'Unverified ❌'],
        'Salary Credited': ['₹45,000', '₹50,000', '₹42,000', '₹85,000'],
        'AI Status': ['Normal', 'Normal', 'Normal', 'FLAGGED ⚠️']
    })
    
    st.dataframe(payroll_data)
    
    st.error("⚠️ **AUTOMATED INQUIRY ALERT DETECTED**")
    st.warning("Digital Case File #104: High salary credited to unverified biometric record (EMP_004). Flagged for human officer review.")

elif menu == "Tenders & Procurement":
    st.header("📊 Module 2: Tender Overpricing Audit")
    
    tenders_data = pd.DataFrame({
        'Tender ID': ['TEN_101', 'TEN_102', 'TEN_103'],
        'Department': ['Roads & Building', 'Water Resources', 'Education'],
        'Estimated Budget': ['₹50 Lakhs', '₹1.2 Crore', '₹30 Lakhs'],
        'Winning Bid': ['₹52 Lakhs', '₹3.1 Crore 🚨', '₹31 Lakhs'],
        'Approval Days': [15, 1, 20]
    })
    
    st.dataframe(tenders_data)
    st.error("⚠️ **AI ANOMALY DETECTED IN TEN_102**")
    st.info("Winning bid exceeds estimated budget by 158% with suspiciously rapid 1-day approval. Sent to Vigilance Department.")
    
  
