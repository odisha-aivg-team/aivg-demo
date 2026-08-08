import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="AI Vigilance Grid (AIVG)", page_icon="🛡️")

st.title("🛡️ AI Vigilance Grid (AIVG)")
st.caption("Odiaprenuer 3.0 Smart Odisha Hackathon | Cyber Security from Corruption")

st.markdown("---")

# 1. Authority Configuration
st.sidebar.header("📱 Vigilance Authority Contact")
authority_phone = st.sidebar.text_input("Authority Mobile Number:", value="9876543210")
fast2sms_api_key = st.sidebar.text_input("Fast2SMS API Key (Optional):", type="password")

def trigger_auto_sms(phone, message_text):
    """Sends automatic SMS via Fast2SMS API"""
    if not fast2sms_api_key:
        return False, "No API Key provided (Running Simulation Mode)"
    
    url = "https://www.fast2sms.com/dev/bulkV2"
    payload = {
        "variables_values": message_text,
        "route": "otp",
        "numbers": phone
    }
    headers = {
        'authorization': fast2sms_api_key,
        'Content-Type': "application/x-www-form-urlencoded"
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        if response.status_code == 200:
            return True, "SMS Dispatched"
        else:
            return False, response.text
    except Exception as e:
        return False, str(e)

# 2. Main Navigation
menu = st.sidebar.selectbox("Select System Data Feed", ["Payroll & Salary Logs", "Tender Overpricing Audit"])

if menu == "Payroll & Salary Logs":
    st.header("📊 Real-Time Payroll Audit Module")
    
    col1, col2 = st.columns(2)
    with col1:
        salary_input = st.number_input("Enter Salary Amount (INR):", min_value=10000, max_value=500000, value=85000, step=5000)
    with col2:
        bio_status = st.selectbox("Biometric Status:", ["Unverified ❌", "Verified ✅"])

    data = [
        {"Employee ID": "EMP_001", "Name": "Ramesh Mohanty", "Biometric Status": "Verified ✅", "Salary Credited": "₹45,000", "AI Status": "Normal ✅"},
        {"Employee ID": "EMP_002", "Name": "Sita Das", "Biometric Status": "Verified ✅", "Salary Credited": "₹50,000", "AI Status": "Normal ✅"},
        {"Employee ID": "EMP_003", "Name": "Prakash Naik", "Biometric Status": "Verified ✅", "Salary Credited": "₹42,000", "AI Status": "Normal ✅"},
    ]

    is_anomaly = (salary_input > 70000) or (bio_status == "Unverified ❌")
    status_tag = "FLAGGED ⚠️" if is_anomaly else "Normal ✅"

    data.append({
        "Employee ID": "EMP_004 (Live Test)",
        "Name": "Test Employee Record",
        "Biometric Status": bio_status,
        "Salary Credited": f"₹{salary_input:,}",
        "AI Status": status_tag
    })

    st.dataframe(pd.DataFrame(data), use_container_width=True)

    # 3. Automatic Alert Logic
    if is_anomaly:
        st.error("🚨 **AUTOMATED INQUIRY ALERT DETECTED IN REAL-TIME!**")
        st.warning(f"Digital Case File #104: Salary ₹{salary_input:,} with status '{bio_status}' flagged as suspicious anomaly.")
        
        # Check session_state so the SMS sends automatically ONCE per anomaly
        alert_identifier = f"{salary_input}_{bio_status}"
        if 'sent_alert' not in st.session_state or st.session_state.sent_alert != alert_identifier:
            sms_body = f"CRITICAL: AIVG Corruption Alert. Record EMP_004 flagged with salary INR {salary_input} and Biometric status {bio_status}. Immediate verification needed."
            
            success, msg = trigger_auto_sms(authority_phone, sms_body)
            st.session_state.sent_alert = alert_identifier
            
            if success:
                st.success(f"📲 **AUTOMATIC DISPATCH SUCCESS:** Real SMS alert delivered to Authority: {authority_phone}!")
            else:
                st.info(f"⚡ **AUTOMATED SYSTEM TRIGGERED:** System generated automated dispatch payload for Authority: **{authority_phone}**.")
    else:
        st.session_state.sent_alert = None
        st.success("🟢 **SYSTEM NORMAL:** No anomalies detected. Transaction marked safe.")

elif menu == "Tender Overpricing Audit":
    st.header("📊 Real-Time Procurement Audit Module")

    col1, col2 = st.columns(2)
    with col1:
        est_budget = st.number_input("Estimated Budget (Lakhs INR):", min_value=10, max_value=500, value=50, step=10)
    with col2:
        winning_bid = st.number_input("Winning Bid Amount (Lakhs INR):", min_value=10, max_value=1000, value=120, step=10)

    price_increase = ((winning_bid - est_budget) / est_budget) * 100
    is_tender_flagged = price_increase > 40 

    tenders = [
        {"Tender ID": "TEN_101", "Department": "Roads & Building", "Estimated Budget": "₹50 Lakhs", "Winning Bid": "₹52 Lakhs", "AI Status": "Normal ✅"},
        {"Tender ID": "TEN_102 (Live Test)", "Department": "Water Resources", "Estimated Budget": f"₹{est_budget} Lakhs", "Winning Bid": f"₹{winning_bid} Lakhs", "AI Status": "FLAGGED 🚨" if is_tender_flagged else "Normal ✅"}
    ]

    st.dataframe(pd.DataFrame(tenders), use_container_width=True)

    if is_tender_flagged:
        st.error(f"🚨 **REAL-TIME ALERT: SUSPICIOUS TENDER INFLATION (+{price_increase:.1f}%)**")
        
        tender_identifier = f"{est_budget}_{winning_bid}"
        if 'sent_tender_alert' not in st.session_state or st.session_state.sent_tender_alert != tender_identifier:
            sms_body = f"CRITICAL: AIVG Procurement Alert. Tender TEN_102 exceeds budget by {price_increase:.1f} percent. Authority verification required."
            
            success, msg = trigger_auto_sms(authority_phone, sms_body)
            st.session_state.sent_tender_alert = tender_identifier
            
            if success:
                st.success(f"📲 **AUTOMATIC DISPATCH SUCCESS:** Real SMS alert delivered to Authority: {authority_phone}!")
            else:
                st.info(f"⚡ **AUTOMATED SYSTEM TRIGGERED:** System generated automated dispatch payload for Authority: **{authority_phone}**.")
    else:
        st.session_state.sent_tender_alert = None
        st.success(f"🟢 **TENDER APPROVED:** Bid is within safe budget limits (+{price_increase:.1f}% deviation).")
        
    
  
