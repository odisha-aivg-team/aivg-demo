import streamlit as st
import pandas as pd
import urllib.parse

# 1. Page Configuration MUST be the first Streamlit command
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

# 3. Sidebar Configuration
st.sidebar.header("📱 Vigilance Officer Contact")
officer_phone = st.sidebar.text_input("Officer Mobile Number (with 91 prefix):", value="919876543210")

# =========================================================
# BOX 1: SITE WORK PROGRESS TRACKER
# =========================================================
with st.container(border=True):
    st.header("🏗️ Box 1: Site Work Progress Tracker")
    st.info("💡 **Site Work Inspection:** Verifies physical progress completed on site against registered attendance days.")

    site_data = pd.DataFrame([
        {"Worker ID": "WRK_101", "Name": "Ramesh Mohanty", "Site Assigned": "Gosani Road Project", "Days Reported": 26, "Physical Progress (%)": 100, "Site Engineer Verification": "Verified ✅"},
        {"Worker ID": "WRK_102", "Name": "Sita Das", "Site Assigned": "Lingipur Canal Works", "Days Reported": 24, "Physical Progress (%)": 95, "Site Engineer Verification": "Verified ✅"},
        {"Worker ID": "WRK_103", "Name": "Prakash Naik", "Site Assigned": "Gajapati School Building", "Days Reported": 25, "Physical Progress (%)": 40, "Site Engineer Verification": "Verified ✅"},
        {"Worker ID": "WRK_104", "Name": "Ananya Patnaik", "Site Assigned": "Gosani Community Hall", "Days Reported": 22, "Physical Progress (%)": 85, "Site Engineer Verification": "Unverified ❌"},
        {"Worker ID": "WRK_105", "Name": "Soumya Ranjan", "Site Assigned": "Lingipur Health Sub-Centre", "Days Reported": 26, "Physical Progress (%)": 100, "Site Engineer Verification": "Verified ✅"},
    ])

    edited_site = st.data_editor(
        site_data,
        column_config={
            "Worker ID": st.column_config.TextColumn("Worker ID", width="small"),
            "Name": st.column_config.TextColumn("Worker Name", width="medium"),
            "Days Reported": st.column_config.NumberColumn("Days Reported", min_value=0, max_value=31, step=1, width="small"),
            "Physical Progress (%)": st.column_config.NumberColumn("Physical Progress (%)", min_value=0, max_value=100, step=5, format="%d%%", width="small"),
            "Site Engineer Verification": st.column_config.SelectboxColumn("Verification Status", options=["Verified ✅", "Unverified ❌"], width="medium")
        },
        use_container_width=True,
        num_rows="dynamic",
        key="editor_site"
    )

    display_site = edited_site.copy()
    display_site["AI Progress Status"] = display_site.apply(
        lambda r: "UNVERIFIED ATTENDANCE / LOW PROGRESS ALERT 🚨" if (r["Days Reported"] > 20 and r["Physical Progress (%)"] < 50) or r["Site Engineer Verification"] == "Unverified ❌" else "Normal ✅",
        axis=1
    )

    st.dataframe(display_site, use_container_width=True, hide_index=True)

    flagged_site = display_site[display_site["AI Progress Status"].str.contains("🚨")]
    if not flagged_site.empty:
        st.error(f"🚨 **SITE PROGRESS DISCREPANCY DETECTED ({len(flagged_site)} Anomaly Flagged)!**")
        summary_text = "\n".join([f"- {r['Worker ID']} ({r['Name']}): {r['Days Reported']} Days | Work: {r['Physical Progress (%)']}% | Status: {r['Site Engineer Verification']}" for _, r in flagged_site.iterrows()])
        wa_text = f"🚨 *AIVG SITE PROGRESS BREACH ALERT*\n\n*School:* OAV Lingipur, Gosani\n*Module:* Site Progress Tracker\n\n*Flagged Records:*\n{summary_text}"
        wa_url = f"https://wa.me/{officer_phone}?text={urllib.parse.quote(wa_text)}"
        st.link_button("🚨 Dispatch Site Anomaly Alert via WhatsApp", wa_url)
    else:
        st.success("🟢 **BOX 1 NORMAL:** All site work progress matches attendance records.")

# =========================================================
# BOX 2: BASE PAYROLL AUDIT TABLE
# =========================================================
with st.container(border=True):
    st.header("📊 Box 2: Base Payroll Audit Table")
    st.info("💡 **Payroll Inspector:** Calculates base salary automatically (`Daily Rate × Days Worked`) and flags salary over-allocations.")

    initial_payroll = pd.DataFrame([
        {"Employee ID": "EMP_001", "Name": "Ramesh Mohanty", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1500, "Days Worked": 26},
        {"Employee ID": "EMP_002", "Name": "Sita Das", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1800, "Days Worked": 24},
        {"Employee ID": "EMP_003", "Name": "Prakash Naik", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1400, "Days Worked": 25},
        {"Employee ID": "EMP_004", "Name": "Ananya Patnaik", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1600, "Days Worked": 22},
        {"Employee ID": "EMP_005", "Name": "Soumya Ranjan", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1500, "Days Worked": 26},
        {"Employee ID": "EMP_006", "Name": "Priya Mishra", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 2000, "Days Worked": 20},
        {"Employee ID": "EMP_007", "Name": "Manas Swain", "Biometric Status": "Verified ✅", "Daily Rate (₹)": 1300, "Days Worked": 28},
    ])

    edited_payroll = st.data_editor(
        initial_payroll,
        column_config={
            "Employee ID": st.column_config.TextColumn("Employee ID", width="small"),
            "Name": st.column_config.TextColumn("Employee Name", width="medium"),
            "Biometric Status": st.column_config.SelectboxColumn("Biometric Status", options=["Verified ✅", "Unverified ❌"], required=True, width="medium"),
            "Daily Rate (₹)": st.column_config.NumberColumn("Daily Rate (₹)", min_value=500, max_value=10000, step=100, format="₹%d", width="small"),
            "Days Worked": st.column_config.NumberColumn("Days Worked", min_value=0, max_value=31, step=1, width="small")
        },
        use_container_width=True,
        num_rows="dynamic",
        key="editor_payroll"
    )

    display_payroll = edited_payroll.copy()
    display_payroll["Calculated Base Pay (₹)"] = display_payroll["Daily Rate (₹)"] * display_payroll["Days Worked"]
    display_payroll["AI Status"] = display_payroll.apply(
        lambda r: "PAYROLL ALERT 🚨" if r["Calculated Base Pay (₹)"] > 80000 or r["Biometric Status"] == "Unverified ❌" else "Normal ✅",
        axis=1
    )

    st.dataframe(
        display_payroll,
        column_config={"Calculated Base Pay (₹)": st.column_config.NumberColumn("Calculated Base Pay (₹)", format="₹%d")},
        use_container_width=True,
        hide_index=True
    )

    flagged_payroll = display_payroll[display_payroll["AI Status"] == "PAYROLL ALERT 🚨"]
    if not flagged_payroll.empty:
        st.error(f"🚨 **PAYROLL ANOMALY DETECTED ({len(flagged_payroll)} Flagged)!**")
        summary_text = "\n".join([f"- {r['Employee ID']} ({r['Name']}): ₹{r['Calculated Base Pay (₹)']} Pay | Bio: {r['Biometric Status']}" for _, r in flagged_payroll.iterrows()])
        wa_text = f"🚨 *AIVG BASE PAYROLL BREACH ALERT*\n\n*School:* OAV Lingipur, Gosani\n*Flagged Records:*\n{summary_text}"
        wa_url = f"https://wa.me/{officer_phone}?text={urllib.parse.quote(wa_text)}"
        st.link_button("🚨 Dispatch Base Payroll Case File via WhatsApp", wa_url)
    else:
        st.success("🟢 **BOX 2 NORMAL:** Base payroll calculations verified clean.")

# =========================================================
# BOX 3: POST-SALARY EXTRA DISBURSEMENT INSPECTOR
# =========================================================
with st.container(border=True):
    st.header("🔍 Box 3: Post-Salary Extra Disbursement Inspector")
    st.info("💡 **Leakage Detector:** Audits if any person receives extra funds/kickbacks after their official base salary has been credited.")

    extra_data = pd.DataFrame([
        {"Employee ID": "EMP_001", "Name": "Ramesh Mohanty", "Approved Base Salary (₹)": 39000, "Post-Salary Extra Funds (₹)": 0, "Disbursal Channel": "Treasury Direct"},
        {"Employee ID": "EMP_002", "Name": "Sita Das", "Approved Base Salary (₹)": 43200, "Post-Salary Extra Funds (₹)": 0, "Disbursal Channel": "Treasury Direct"},
        {"Employee ID": "EMP_003", "Name": "Prakash Naik", "Approved Base Salary (₹)": 35000, "Post-Salary Extra Funds (₹)": 0, "Disbursal Channel": "Treasury Direct"},
        {"Employee ID": "EMP_004", "Name": "Ananya Patnaik", "Approved Base Salary (₹)": 35200, "Post-Salary Extra Funds (₹)": 0, "Disbursal Channel": "Treasury Direct"},
        {"Employee ID": "EMP_005", "Name": "Soumya Ranjan", "Approved Base Salary (₹)": 39000, "Post-Salary Extra Funds (₹)": 0, "Disbursal Channel": "Treasury Direct"},
    ])

    edited_extra = st.data_editor(
        extra_data,
        column_config={
            "Employee ID": st.column_config.TextColumn("Employee ID", width="small"),
            "Name": st.column_config.TextColumn("Employee Name", width="medium"),
            "Approved Base Salary (₹)": st.column_config.NumberColumn("Approved Base Salary (₹)", format="₹%d", width="medium"),
            "Post-Salary Extra Funds (₹)": st.column_config.NumberColumn("Post-Salary Extra Funds (₹)", min_value=0, max_value=500000, step=1000, format="₹%d", width="medium"),
            "Disbursal Channel": st.column_config.SelectboxColumn("Disbursal Channel", options=["Treasury Direct", "Vendor Account", "Third-Party Transfer", "Unlinked Disbursal"], width="medium")
        },
        use_container_width=True,
        num_rows="dynamic",
        key="editor_extra"
    )

    display_extra = edited_extra.copy()
    display_extra["Total Disbursed (₹)"] = display_extra["Approved Base Salary (₹)"] + display_extra["Post-Salary Extra Funds (₹)"]
    display_extra["AI Detection Status"] = display_extra["Post-Salary Extra Funds (₹)"].apply(
        lambda extra: "EXTRA MONEY ALERT 🚨" if extra > 0 else "Normal ✅"
    )

    st.dataframe(display_extra, use_container_width=True, hide_index=True)

    flagged_extra = display_extra[display_extra["AI Detection Status"] == "EXTRA MONEY ALERT 🚨"]
    if not flagged_extra.empty:
        st.error(f"🚨 **UNAUTHORIZED EXTRA MONEY DETECTED ({len(flagged_extra)} Violation Flagged)!**")
        extra_summary = "\n".join([f"- {r['Employee ID']} ({r['Name']}): Base ₹{r['Approved Base Salary (₹)']} + Extra ₹{r['Post-Salary Extra Funds (₹)']} via {r['Disbursal Channel']}" for _, r in flagged_extra.iterrows()])
        wa_text = f"🚨 *AIVG EXTRA MONEY BREACH ALERT*\n\n*School:* OAV Lingipur, Gosani\n*Module:* Post-Salary Leakage Inspector\n\n*Unauthorized Payments Detected:*\n{extra_summary}"
        wa_url = f"https://wa.me/{officer_phone}?text={urllib.parse.quote(wa_text)}"
        st.link_button("🚨 Dispatch Extra Money Breach Alert via WhatsApp", wa_url)
    else:
        st.success("🟢 **BOX 3 NORMAL:** No post-salary unauthorized extra payments detected.")

# =========================================================
# BOX 4: GOVERNMENT WELFARE & MULTIPLE BENEFITS AUDIT
# =========================================================
with st.container(border=True):
    st.header("🎁 Box 4: Government Welfare & Multiple Benefit Detector")
    st.info("💡 **Benefit Fraud Detector:** Flags any beneficiary receiving **more than 2 government scheme benefits**.")

    welfare_data = pd.DataFrame([
        {"Beneficiary Aadhaar ID": "AADHAAR_9001", "Citizen Name": "Ramesh Mohanty", "Scheme 1": "Kalia Yojana ✅", "Scheme 2": "Madhu Babu Pension ✅", "Scheme 3": "None", "Total Active Benefits": 2},
        {"Beneficiary Aadhaar ID": "AADHAAR_9002", "Citizen Name": "Sita Das", "Scheme 1": "Subhadra Yojana ✅", "Scheme 2": "None", "Scheme 3": "None", "Total Active Benefits": 1},
        {"Beneficiary Aadhaar ID": "AADHAAR_9003", "Citizen Name": "Prakash Naik", "Scheme 1": "Kalia Yojana ✅", "Scheme 2": "Mo Kudia Housing ✅", "Scheme 3": "Subhadra Yojana ✅", "Total Active Benefits": 3},
        {"Beneficiary Aadhaar ID": "AADHAAR_9004", "Citizen Name": "Ananya Patnaik", "Scheme 1": "Madhu Babu Pension ✅", "Scheme 2": "Subhadra Yojana ✅", "Scheme 3": "Biju Swasthya Kalyan ✅", "Total Active Benefits": 3},
        {"Beneficiary Aadhaar ID": "AADHAAR_9005", "Citizen Name": "Soumya Ranjan", "Scheme 1": "Kalia Yojana ✅", "Scheme 2": "None", "Scheme 3": "None", "Total Active Benefits": 1},
    ])

    edited_welfare = st.data_editor(
        welfare_data,
        column_config={
            "Beneficiary Aadhaar ID": st.column_config.TextColumn("Aadhaar / Citizen ID", width="medium"),
            "Citizen Name": st.column_config.TextColumn("Citizen Name", width="medium"),
            "Total Active Benefits": st.column_config.NumberColumn("Total Active Benefits", min_value=0, max_value=10, step=1, width="small")
        },
        use_container_width=True,
        num_rows="dynamic",
        key="editor_welfare"
    )

    display_welfare = edited_welfare.copy()
    display_welfare["AI Welfare Status"] = display_welfare["Total Active Benefits"].apply(
        lambda benefits: "MULTIPLE SCHEME FRAUD ALERT 🚨 (>2 Benefits)" if benefits > 2 else "Approved ✅"
    )

    st.dataframe(display_welfare, use_container_width=True, hide_index=True)

    flagged_welfare = display_welfare[display_welfare["AI Welfare Status"].str.contains("🚨")]
    if not flagged_welfare.empty:
        st.error(f"🚨 **MULTIPLE BENEFIT FRAUD DETECTED ({len(flagged_welfare)} Beneficiary Flagged)!**")
        welfare_summary = "\n".join([f"- {r['Beneficiary Aadhaar ID']} ({r['Citizen Name']}): Enrolled in {r['Total Active Benefits']} Government Schemes" for _, r in flagged_welfare.iterrows()])
        wa_text = f"🚨 *AIVG MULTIPLE SCHEME BENEFIT FRAUD ALERT*\n\n*School:* OAV Lingipur, Gosani\n*Violations Detected:*\n{welfare_summary}"
        wa_url = f"https://wa.me/{officer_phone}?text={urllib.parse.quote(wa_text)}"
        st.link_button("🚨 Dispatch Benefit Fraud Case File via WhatsApp", wa_url)
    else:
        st.success("🟢 **BOX 4 NORMAL:** All citizens are within the allowed limit of government benefits.")

# =========================================================
# BOX 5: PROCUREMENT & TENDER AUDIT
# =========================================================
with st.container(border=True):
    st.header("📊 Box 5: Real-Time Procurement & Tender Audit Module")
    st.info("💡 **Tender Audit:** Detects overpricing and inflated bids exceeding 40% of the estimated budget.")

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
        num_rows="dynamic",
        key="editor_tenders"
    )

    edited_tenders["Inflation (%)"] = ((edited_tenders["Winning Bid (Lakhs INR)"] - edited_tenders["Budget (Lakhs INR)"]) / edited_tenders["Budget (Lakhs INR)"]) * 100
    edited_tenders["AI Status"] = edited_tenders["Inflation (%)"].apply(lambda x: "TENDER FLAGGED 🚨" if x > 40 else "Normal ✅")

    st.dataframe(edited_tenders, use_container_width=True, hide_index=True)

    flagged_tenders = edited_tenders[edited_tenders["AI Status"] == "TENDER FLAGGED 🚨"]
    if not flagged_tenders.empty:
        st.error(f"🚨 **TENDER INFLATION BREACH DETECTED ({len(flagged_tenders)} Tender Flagged)!**")
        tender_summary = "\n".join([f"- {r['Tender ID']} ({r['Department']}): Budget ₹{r['Budget (Lakhs INR)']}L vs Bid ₹{r['Winning Bid (Lakhs INR)']}L (+{r['Inflation (%)']:.1f}%)" for _, r in flagged_tenders.iterrows()])
        wa_text = f"🚨 *AIVG TENDER BREACH ALERT*\n\n*School:* OAV Lingipur, Gosani\n*Flagged Tenders:*\n{tender_summary}"
        wa_url = f"https://wa.me/{officer_phone}?text={urllib.parse.quote(wa_text)}"
        st.link_button("🚨 Dispatch Tender Case File via WhatsApp", wa_url)
    else:
        st.success("🟢 **BOX 5 NORMAL:** All submitted bids are within safe budget variance limits (<40% deviation).")
    
