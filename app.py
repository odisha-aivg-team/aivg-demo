import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="AI Vigilance Grid (AIVG)", page_icon="🛡️", layout="wide")

st.title("🛡️ AI Vigilance Grid (AIVG)")
st.caption("Odiaprenuer 3.0 Smart Odisha Hackathon | Cyber Security & Site Tracking")

st.markdown("---")

# Sidebar Configuration
st.sidebar.header("📱 Higher Officer Dispatch Settings")
officer_phone = st.sidebar.text_input("Officer Mobile (Country Code e.g., 919876543210):", value="919876543210")

menu = st.sidebar.selectbox("Select System Data Feed", ["Site Work & Payroll Tracker", "Tender Overpricing Audit"])

if menu == "Site Work & Payroll Tracker":
    st.header("📊 Site Progress & Automated Payroll Audit")
    st.info("💡 **Interactive Sheet:** Edit 'Daily Rate', 'Days Worked', or 'Site Work Done (%)' directly in the table to calculate total payout in real-time!")

    # Initial employee site & payroll dataset
    initial_data = pd.DataFrame([
        {"Employee ID": "EMP_001", "Name": "Ramesh Mohanty", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1500, "Days Worked": 26, "Site Work Done (%)": 100},
        {"Employee ID": "EMP_002", "Name": "Sita Das", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1800, "Days Worked": 24, "Site Work Done (%)": 95},
        {"Employee ID": "EMP_003", "Name": "Prakash Naik", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1400, "Days Worked": 25, "Site Work Done (%)": 90},
        {"Employee ID": "EMP_004", "Name": "Ananya Patnaik", "Biometric Status": "Verified ✅", "Salary (INR)": 48000, "Daily Rate (₹)": 1600, "Days Worked": 22, "Site Work Done (%)": 85},
        {"Employee ID": "EMP_005", "Name": "Soumya Ranjan", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1500, "Days Worked": 26, "Site Work Done (%)": 100},
        {"Employee ID": "EMP_006", "Name": "Priya Mishra", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 2000, "Days Worked": 20, "Site Work Done (%)": 80},
        {"Employee ID": "EMP_007", "Name": "Manas Swain", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1300, "Days Worked": 28, "Site Work Done (%)": 100},
    ])

    # 1. Interactive data editor
    edited_df = st.data_editor(
        initial_data,
        column_config={
            "Employee ID": st.column_config.TextColumn("Employee ID", width="small"),
            "Name": st.column_config.TextColumn("Name", width="medium"),
            "Biometric Status": st.column_config.SelectboxColumn(
                "Biometric Status",
                options=["Verified ✅", "Unverified ❌"],
                required=True,
                width="medium"
            ),
            "Daily Rate (₹)": st.column_config.NumberColumn("Daily Rate (₹)", min_value=500, max_value=10000, step=100, format="₹%d"),
            "Days Worked": st.column_config.NumberColumn("Days Worked", min_value=0, max_value=31, step=1),
            "Site Work Done (%)": st.column_config.NumberColumn("Site Work Done (%)", min_value=0, max_value=100, step=5, format="%d%%")
        },
        use_container_width=True,
        num_rows="dynamic"
    )

    # 2. Automated Salary Calculation: Payout = Daily Rate * Days Worked
    display_df = edited_df.copy()
    display_df["Calculated Payout (₹)"] = display_df["Daily Rate (₹)"] * display_df["Days Worked"]

    # 3. AI Detection Rules:
    # - Flagged if Payout > ₹80,000
    # - Flagged if Biometrics are Unverified
    # - Flagged if Site Work Done is below 50% despite 20+ days worked (Ghost Worker/Corruption Indicator)
    def check_ai_status(row):
        if row["Calculated Payout (₹)"] > 80000 or row["Biometric Status"] == "Unverified ❌":
            return "FLAGGED 🚨"
        if row["Days Worked"] > 20 and row["Site Work Done (%)"] < 50:
            return "FLAGGED 🚨"
        return "Normal ✅"

    display_df["AI Status"] = display_df.apply(check_ai_status, axis=1)

    # Reorder columns for clean display
    cols = ["Employee ID", "Name", "Biometric Status", "Daily Rate (₹)", "Days Worked", "Site Work Done (%)", "Calculated Payout (₹)", "AI Status"]
    display_df = display_df[[c for c in cols if c in display_df.columns]]

    st.subheader("📋 Dynamic Site Audit & Calculated Pay Sheet")
    st.dataframe(
        display_df,
        column_config={
            "Calculated Payout (₹)": st.column_config.NumberColumn("Calculated Payout (₹)", format="₹%d"),
            "AI Status": st.column_config.TextColumn("AI Status", width="medium")
        },
        use_container_width=True,
        hide_index=True
    )

    # 4. Trigger Alerts if any row is flagged
    flagged_records = display_df[display_df["AI Status"] == "FLAGGED 🚨"]

    if not flagged_records.empty:
        st.error(f"🚨 **AUTOMATED VIGILANCE ALERT DETECTED ({len(flagged_records)} Anomaly Found)!**")
        
        for _, row in flagged_records.iterrows():
            st.warning(f"⚠️ **Flagged:** {row['Employee ID']} ({row['Name']}) | Payout: ₹{row['Calculated Payout (₹)']:,} | Site Work: {row['Site Work Done (%)']}% | Bio: {row['Biometric Status']}")
        
        summary_text = "\n".join([f"- {r['Employee ID']} ({r['Name']}): {r['Days Worked']} Days | Work: {r['Site Work Done (%)']}% | Pay: ₹{r['Calculated Payout (₹)']}" for _, r in flagged_records.iterrows()])
        wa_text = f"🚨 *AIVG SITE WORK & PAYROLL BREACH ALERT*\n\nSite Anomalies Flagged:\n{summary_text}\n\n*Action Required:* Field audit verification needed."
        encoded_text = urllib.parse.quote(wa_text)
        wa_url = f"https://wa.me/{officer_phone}?text={encoded_text}"
        
        st.markdown("---")
        st.link_button("🚨 Dispatch Real-Time WhatsApp Alert to Officer", wa_url)
    else:
        st.success("🟢 **SYSTEM NORMAL:** All attendance, site progress logs, and calculated payouts are verified.")

elif menu == "Tender Overpricing Audit":
    st.header("📊 Real-Time Procurement Audit Module")
    # ... (Keep existing tender module logic)
    
    
        
        
        
    
  
