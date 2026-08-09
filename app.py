import streamlit as st
import pandas as pd
import urllib.parse

# 1. Page Configuration (Wide Layout to avoid cut-offs)
st.set_page_config(
    page_title="AIVG - AI Vigilance Grid", 
    page_icon="🛡️", 
    layout="wide"
)

# 2. Header & Branding
st.title("🛡️ AI Vigilance Grid (AIVG)")
st.caption("Odiaprenuer 3.0 | Odisha Adarsha Vidyalaya, Lingipur, Gosani, Gajapati | Smart Odisha Hackathon")
st.markdown("**Theme:** Cyber Security from Corruption — *An AI-Based Automatic Corruption Inquiry System*")

st.markdown("---")

# 3. Sidebar Officer Dispatch Configuration
st.sidebar.header("📱 Vigilance Officer Contact Settings")
officer_phone = st.sidebar.text_input("Officer Mobile Number (with 91 country code):", value="919876543210")

menu = st.sidebar.selectbox("Select Data Feed Module", ["Site Progress & Payroll Audit", "Procurement & Tender Audit"])

# ---------------------------------------------------------
# MODULE 1: SITE PROGRESS & PAYROLL AUDIT
# ---------------------------------------------------------
if menu == "Site Progress & Payroll Audit":
    st.header("📊 Site Work & Automated Payroll Audit Module")
    st.info("💡 **Interactive Editor:** Edit 'Daily Rate', 'Days Worked', 'Site Work Done (%)', or 'Biometric Status' inside any cell to trigger real-time AI anomaly detection.")

    # Base Dataset with Team Members & Workers
    initial_payroll = pd.DataFrame([
        {"Employee ID": "EMP_001", "Name": "Ramesh Mohanty", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1500, "Days Worked": 26, "Site Work Done (%)": 100},
        {"Employee ID": "EMP_002", "Name": "Sita Das", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1800, "Days Worked": 24, "Site Work Done (%)": 95},
        {"Employee ID": "EMP_003", "Name": "Prakash Naik", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1400, "Days Worked": 25, "Site Work Done (%)": 90},
        {"Employee ID": "EMP_004", "Name": "Ananya Patnaik", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1600, "Days Worked": 22, "Site Work Done (%)": 85},
        {"Employee ID": "EMP_005", "Name": "Soumya Ranjan", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1500, "Days Worked": 26, "Site Work Done (%)": 100},
        {"Employee ID": "EMP_006", "Name": "Priya Mishra", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 2000, "Days Worked": 20, "Site Work Done (%)": 80},
        {"Employee ID": "EMP_007", "Name": "Manas Swain", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1300, "Days Worked": 28, "Site Work Done (%)": 100},
    ])

    # Interactive Spreadsheet View
    edited_payroll = st.data_editor(
        initial_payroll,
        column_config={
            "Employee ID": st.column_config.TextColumn("Employee ID", width="small"),
            "Name": st.column_config.TextColumn("Employee Name", width="medium"),
            "Biometric Status": st.column_config.SelectboxColumn(
                "Biometric Status",
                options=["Verified ✅", "Unverified ❌"],
                required=True,
                width="medium"
            ),
            "Daily Rate (₹)": st.column_config.NumberColumn("Daily Rate (₹)", min_value=500, max_value=10000, step=100, format="₹%d", width="small"),
            "Days Worked": st.column_config.NumberColumn("Days Worked", min_value=0, max_value=31, step=1, width="small"),
            "Site Work Done (%)": st.column_config.NumberColumn("Site Work Done (%)", min_value=0, max_value=100, step=5, format="%d%%", width="small")
        },
        use_container_width=True,
        num_rows="dynamic"
    )

    # Automated Payout Calculation: Rate * Days
    display_payroll = edited_payroll.copy()
    display_payroll["Calculated Payout (₹)"] = display_payroll["Daily Rate (₹)"] * display_payroll["Days Worked"]

    # AI Detection Logic
    def check_payroll_anomaly(row):
        # Rule 1: High Payout (> ₹80,000)
        if row["Calculated Payout (₹)"] > 80000:
            return "FLAGGED 🚨"
        # Rule 2: Unverified Biometrics
        if row["Biometric Status"] == "Unverified ❌":
            return "FLAGGED 🚨"
        # Rule 3: Mismatch between Days Worked (>20) and Site Work Completed (<50%)
        if row["Days Worked"] > 20 and row["Site Work Done (%)"] < 50:
            return "FLAGGED 🚨"
        return "Normal ✅"

    display_payroll["AI Status"] = display_payroll.apply(check_payroll_anomaly, axis=1)

    # Rearrange for display table
    ordered_cols = ["Employee ID", "Name", "Biometric Status", "Daily Rate (₹)", "Days Worked", "Site Work Done (%)", "Calculated Payout (₹)", "AI Status"]
    final_payroll_table = display_payroll[[col for col in ordered_cols if col in display_payroll.columns]]

    st.subheader("📋 Dynamic Audit Output & Calculated Pay Sheet")
    st.dataframe(
        final_payroll_table,
        column_config={
            "Calculated Payout (₹)": st.column_config.NumberColumn("Calculated Payout (₹)", format="₹%d", width="medium"),
            "AI Status": st.column_config.TextColumn("AI Status", width="small")
        },
        use_container_width=True,
        hide_index=True
    )

    # Flagged Alerts Handling
    flagged_workers = final_payroll_table[final_payroll_table["AI Status"] == "FLAGGED 🚨"]

    if not flagged_workers.empty:
        st.error(f"🚨 **AUTOMATED INQUIRY ALERT TRIGGERED ({len(flagged_workers)} Anomaly Detected)!**")
        
        for _, r in flagged_workers.iterrows():
            st.warning(f"⚠️ **Digital Case File Generated:** {r['Employee ID']} ({r['Name']}) | Payout: ₹{r['Calculated Payout (₹)']:,} | Work Done: {r['Site Work Done (%)']}% | Status: {r['Biometric Status']}")

        # WhatsApp Pre-filled Case File Alert
        alert_details = "\n".join([f"- {r['Employee ID']} ({r['Name']}): ₹{r['Calculated Payout (₹)']} Pay | Work: {r['Site Work Done (%)']}% | Bio: {r['Biometric Status']}" for _, r in flagged_workers.iterrows()])
        wa_text = f"🚨 *AIVG DIGITAL CASE FILE ALERT*\n\n*School:* OAV Lingipur, Gosani\n*Module:* Payroll & Site Audit\n\n*Flagged Records:*\n{alert_details}\n\n*Action Required:* Immediate human verification requested."
        
        encoded_msg = urllib.parse.quote(wa_text)
        wa_url = f"https://wa.me/{officer_phone}?text={encoded_msg}"

        st.markdown("---")
        st.subheader("📲 Instant Dispatch System")
        st.link_button("🚨 Dispatch Digital Case File to Vigilance Officer via WhatsApp", wa_url)
    else:
        st.success("🟢 **SYSTEM NORMAL:** All attendance logs, site progress, and calculated payouts are verified clean.")

# ---------------------------------------------------------
# MODULE 2: PROCUREMENT & TENDER AUDIT
# ---------------------------------------------------------
elif menu == "Procurement & Tender Audit":
    st.header("📊 Real-Time Procurement & Tender Audit Module")
    st.info("💡 **Interactive Editor:** Modify Estimated Budget or Winning Bid to test tender inflation detection!")

    initial_tenders = pd.DataFrame([
        {"Tender ID": "TEN_101", "Department": "Roads & Building", "Budget (Lakhs INR)": 50, "Winning Bid (Lakhs INR)": 52},
        {"Tender ID": "TEN_102", "Department": "Water Resources", "Budget (Lakhs INR)": 60, "Winning Bid (Lakhs INR)": 64},
        {"Tender ID": "TEN_103", "Department": "Rural Development", "Budget (Lakhs INR)": 40, "Winning Bid (Lakhs INR)": 41},
        {"Tender ID": "TEN_104", "Department": "Health Infrastructure", "Budget (Lakhs INR)": 100, "Winning Bid (Lakhs INR)": 105},
    ])

    edited_tenders = st.data_editor(
        initial_tenders,
        column_config={
            "Tender ID": st.column_config.TextColumn("Tender ID", width="small"),
            "Department": st.column_config.TextColumn("Department", width="medium"),
            "Budget (Lakhs INR)": st.column_config.NumberColumn("Budget (Lakhs)", format="₹%d L", width="small"),
            "Winning Bid (Lakhs INR)": st.column_config.NumberColumn("Winning Bid (Lakhs)", format="₹%d L", width="small"),
        },
        use_container_width=True,
        num_rows="dynamic"
    )

    # Calculate Inflation Percentage
    edited_tenders["Inflation (%)"] = ((edited_tenders["Winning Bid (Lakhs INR)"] - edited_tenders["Budget (Lakhs INR)"]) / edited_tenders["Budget (Lakhs INR)"]) * 100
    edited_tenders["AI Status"] = edited_tenders["Inflation (%)"].apply(lambda x: "FLAGGED 🚨" if x > 40 else "Normal ✅")

    st.subheader("📋 Dynamic Procurement Audit Sheet")
    st.dataframe(
        edited_tenders,
        column_config={
            "Inflation (%)": st.column_config.NumberColumn("Inflation (%)", format="%.1f%%", width="small"),
            "AI Status": st.column_config.TextColumn("AI Status", width="small")
        },
        use_container_width=True,
        hide_index=True
    )

    flagged_tenders = edited_tenders[edited_tenders["AI Status"] == "FLAGGED 🚨"]

    if not flagged_tenders.empty:
        st.error(f"🚨 **TENDER INFLATION BREACH DETECTED ({len(flagged_tenders)} Tender Flagged)!**")
        
        for _, r in flagged_tenders.iterrows():
            st.warning(f"🚨 **Tender Case File:** {r['Tender ID']} ({r['Department']}) | Budget: ₹{r['Budget (Lakhs INR)']}L | Bid: ₹{r['Winning Bid (Lakhs INR)']}L (+{r['Inflation (%)']:.1f}% deviation)")

        tender_summary = "\n".join([f"- {r['Tender ID']} ({r['Department']}): Budget ₹{r['Budget (Lakhs INR)']}L vs Bid ₹{r['Winning Bid (Lakhs INR)']}L (+{r['Inflation (%)']:.1f}%)" for _, r in flagged_tenders.iterrows()])
        wa_text = f"🚨 *AIVG TENDER BREACH ALERT*\n\n*School:* OAV Lingipur, Gosani\n*Module:* Tender Audit\n\n*Flagged Tenders:*\n{tender_summary}\n\n*Action Required:* Forwarded to Vigilance Department for verification."
        
        encoded_msg = urllib.parse.quote(wa_text)
        wa_url = f"https://wa.me/{officer_phone}?text={encoded_msg}"

        st.markdown("---")
        st.subheader("📲 Instant Dispatch System")
        st.link_button("🚨 Dispatch Tender Case File to Vigilance Officer via WhatsApp", wa_url)
    else:
        st.success("🟢 **TENDERS APPROVED:** All submitted bids are within safe budget variance limits (<40% deviation).")
        
    
    
        
        
        
    
  
