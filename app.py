import streamlit as st
import pandas as pd

st.set_page_config(page_title="AI Vigilance Grid (AIVG)", page_icon="🛡️")

st.title("🛡️ AI Vigilance Grid (AIVG)")
st.caption("Odiaprenuer 3.0 Smart Odisha Hackathon | Cyber Security from Corruption")

st.markdown("---")

# Sidebar navigation
menu = st.sidebar.selectbox("Select System Data Feed", ["Payroll & Salary Logs", "Tender Overpricing Audit"])

if menu == "Payroll & Salary Logs":
    st.header("📊 Real-Time Payroll Audit Module")
    st.write("Test the AI engine live by changing the salary or biometric status below:")

    # Interactive Live Demo Inputs
    col1, col2 = st.columns(2)
    with col1:
        salary_input = st.number_input("Enter Salary Amount (INR):", min_value=10000, max_value=500000, value=85000, step=5000)
    with col2:
        bio_status = st.selectbox("Biometric Status:", ["Unverified ❌", "Verified ✅"])

    # Base table data
    data = [
        {"Employee ID": "EMP_001", "Name": "Ramesh Mohanty", "Biometric Status": "Verified ✅", "Salary Credited": "₹45,000", "AI Status": "Normal ✅"},
        {"Employee ID": "EMP_002", "Name": "Sita Das", "Biometric Status": "Verified ✅", "Salary Credited": "₹50,000", "AI Status": "Normal ✅"},
        {"Employee ID": "EMP_003", "Name": "Prakash Naik", "Biometric Status": "Verified ✅", "Salary Credited": "₹42,000", "AI Status": "Normal ✅"},
    ]

    # Real-time logic check
    is_anomaly = (salary_input > 70000) or (bio_status == "Unverified ❌")
    status_tag = "FLAGGED ⚠️" if is_anomaly else "Normal ✅"

    # Add the test user record
    data.append({
        "Employee ID": "EMP_004 (Live Test)",
        "Name": "Test Employee Record",
        "Biometric Status": bio_status,
        "Salary Credited": f"₹{salary_input:,}",
        "AI Status": status_tag
    })

    st.dataframe(pd.DataFrame(data), use_container_width=True)

    # Real-Time Alert Trigger
    if is_anomaly:
        st.error("🚨 **AUTOMATED INQUIRY ALERT DETECTED IN REAL-TIME!**")
        st.warning(f"Digital Case File #104: Salary ₹{salary_input:,} with status '{bio_status}' flagged as suspicious anomaly. Forwarded to Vigilance Department.")
    else:
        st.success("🟢 **SYSTEM NORMAL:** No anomalies detected. Transaction marked safe.")


elif menu == "Tender Overpricing Audit":
    st.header("📊 Real-Time Procurement Audit Module")
    st.write("Test the AI engine live by entering the estimated budget vs winning bid:")

    col1, col2 = st.columns(2)
    with col1:
        est_budget = st.number_input("Estimated Budget (Lakhs INR):", min_value=10, max_value=500, value=50, step=10)
    with col2:
        winning_bid = st.number_input("Winning Bid Amount (Lakhs INR):", min_value=10, max_value=1000, value=120, step=10)

    # Calculate percentage increase live
    price_increase = ((winning_bid - est_budget) / est_budget) * 100
    is_tender_flagged = price_increase > 40  # Flag if bid is 40%+ above estimated budget

    tenders = [
        {"Tender ID": "TEN_101", "Department": "Roads & Building", "Estimated Budget": "₹50 Lakhs", "Winning Bid": "₹52 Lakhs", "AI Status": "Normal ✅"},
        {"Tender ID": "TEN_102 (Live Test)", "Department": "Water Resources", "Estimated Budget": f"₹{est_budget} Lakhs", "Winning Bid": f"₹{winning_bid} Lakhs", "AI Status": "FLAGGED 🚨" if is_tender_flagged else "Normal ✅"}
    ]

    st.dataframe(pd.DataFrame(tenders), use_container_width=True)

    # Real-Time Alert Output
    if is_tender_flagged:
        st.error(f"🚨 **REAL-TIME ALERT: SUSPICIOUS TENDER INFLATION (+{price_increase:.1f}%)**")
        st.info(f"Winning bid of ₹{winning_bid} Lakhs exceeds budget of ₹{est_budget} Lakhs by over 40%. Generated Digital Inquiry File.")
    else:
        st.success(f"🟢 **TENDER APPROVED:** Bid is within safe budget limits (+{price_increase:.1f}% deviation).")
        
    
  
