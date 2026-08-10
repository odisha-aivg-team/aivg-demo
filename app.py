import urllib.parse  # Make sure this is imported at the top of your app.py

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
            
            # WhatsApp Dispatch Setup
            msg3 = f"🚨 *AIVG ALERT: EXTRA DISBURSEMENT OVERRUN*\nTransaction: {row['Transaction ID']}\nApproved: ₹{row['Approved Amount (₹)']}\nDisbursed: ₹{row['Disbursed Amount (₹)']}\nImmediate Action Required."
            url3 = f"https://api.whatsapp.com/send?phone=919000000000&text={urllib.parse.quote(msg3)}"
            st.link_button("📲 Send WhatsApp Alert", url3, key=f"wa_3_{idx}")

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
    st.subheader("🚨 Scheme Audit Alert")
    low_dbt = df4[df4["DBT Success Rate (%)"] < 80]
    if not low_dbt.empty:
        st.error("🚨 HIGH BENEFICIARY MISMATCH RISK")
        st.warning("Housing Grant B shows abnormal drop in successful direct transfers.")
        
        # WhatsApp Dispatch Setup
        msg4 = "🚨 *AIVG ALERT: SCHEME BENEFICIARY ANOMALY*\nHousing Grant B DBT Success Rate dropped below safe threshold (62.0%). Please inspect portal logs."
        url4 = f"https://api.whatsapp.com/send?phone=919000000000&text={urllib.parse.quote(msg4)}"
        st.link_button("📲 Send WhatsApp Alert", url4, key="wa_4")

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
        
        # WhatsApp Dispatch Setup
        msg5 = "🚨 *AIVG ALERT: TENDER COLLUSION RISK*\nTender TND_502 flagged for identical bidder IP submission addresses. Potential cartel activity."
        url5 = f"https://api.whatsapp.com/send?phone=919000000000&text={urllib.parse.quote(msg5)}"
        st.link_button("📲 Send WhatsApp Alert", url5, key="wa_5")
        
        
    
            
        
        
        
    
    
    
    
        
        
        
    
  
