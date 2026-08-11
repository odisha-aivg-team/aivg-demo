import streamlit as st
import pandas as pd
import urllib.parse

# =========================================================
# 1. Page Configuration (MUST be the first Streamlit command)
# =========================================================
st.set_page_config(
    page_title="AIVG - AI Vigilance Grid", 
    page_icon="🛡️", 
    layout="wide"
)

# =========================================================
# 2. Custom CSS & Styling
# =========================================================
st.markdown("""
    <style>
    .stAlert {
        border-radius: 8px;
    }
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# =========================================================
# 3. Header & Branding
# =========================================================
st.title("🛡️ AI Vigilance Grid (AIVG)")
st.caption("Odiaprenuer 3.0 | Odisha Adarsha Vidyalaya, Lingipur, Gosani, Gajapati | Smart Odisha Hackathon")
st.markdown("**Theme:** Cyber Security from Corruption — *An AI-Based Automatic Corruption Inquiry System*")

st.markdown("---")

# =========================================================
# 4. Top-Level KPI Dashboard Banner
# =========================================================
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric(label="Total Active Workers", value="105", delta="5 New")
with col2:
    st.metric(label="Active Procurement Bids", value="₹2.5 Cr", delta="4 Pending")
with col3:
    st.metric(label="Total Anomalies Flagged", value="4 Flags", delta="-2 Resolved", delta_color="inverse")
with col4:
    st.metric(label="System Security Index", value="98.2%", delta="Optimal ✅")

st.markdown("---")

# =========================================================
# 5. Sidebar Configuration
# =========================================================
st.sidebar.header("📱 Vigilance Officer Contact")
officer_phone = st.sidebar.text_input("Officer Mobile Number (with 91 prefix):", value="919876543210")

st.sidebar.markdown("---")
st.sidebar.header("🔍 Global Audit View")
filter_option = st.sidebar.radio("Display Filter:", ["All Records", "Flagged Anomalies Only 🚨", "Normal Only ✅"])

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
        {"Worker ID": "WRK_104", "Name": "Ananya Patnaik", "Site Assigned": "Gosani Community Hall", "Days Reported": 8, "Physical Progress (%)": 85, "Site Engineer Verification": "Unverified ❌"},
        {"Worker ID": "WRK_105", "Name": "Soumya Ranjan", "Site Assigned": "Lingipur Health Sub-Centre", "Days Reported": 26, "Physical Progress (%)": 100, "Site Engineer Verification": "Verified ✅"},
    ])

    edited_site = st.data_editor(
        site_data,
        column_config={
            "Worker ID": st.column_config.TextColumn("Worker ID", width="medium"),
            "Name": st.column_config.TextColumn("Worker Name", width="medium"),
            "Days Reported": st.column_config.NumberColumn("Days Reported", min_value=0, max_value=31, step=1, width="medium"),
            "Physical Progress (%)": st.column_config.NumberColumn("Physical Progress (%)", min_value=0, max_value=100, step=5, format="%d%%", width="medium"),
            "Site Engineer Verification": st.column_config.SelectboxColumn("Verification Status", options=["Verified ✅", "Unverified ❌"], width="medium")
        },
        use_container_width=True,
        num_rows="dynamic",
        key="editor_site"
    )

    display_site = edited_site.copy()

    def evaluate_site_status(row):
        if row["Site Engineer Verification"] == "Unverified ❌" or row["Days Reported"] < 10:
            return "🚨 LOW ATTENDANCE"
        elif row["Days Reported"] > 20 and row["Physical Progress (%)"] < 50:
            return "⚠️ PROGRESS LAG"
        else:
            return "Normal ✅"

    display_site["AI Status"] = display_site.apply(evaluate_site_status, axis=1)

    # Sidebar Filter Application
    if filter_option == "Flagged Anomalies Only 🚨":
        view_site = display_site[display_site["AI Status"] != "Normal ✅"]
    elif filter_option == "Normal Only ✅":
        view_site = display_site[display_site["AI Status"] == "Normal ✅"]
    else:
        view_site = display_site

    st.dataframe(
        view_site,
        column_config={
            "Worker ID": st.column_config.TextColumn("Worker ID", width="medium"),
            "Days Reported": st.column_config.NumberColumn("Days Reported", width="medium"),
            "Physical Progress (%)": st.column_config.NumberColumn("Physical Progress (%)", format="%d%%", width="medium"),
            "AI Status": st.column_config.TextColumn("AI Status", width="medium")
        },
        use_container_width=True,
        hide_index=True
    )

    flagged_site = display_site[display_site["AI Status"] != "Normal ✅"]
    if not flagged_site.empty:
        st.error(f"🚨 **SITE ANOMALIES DETECTED ({len(flagged_site)} Records Flagged)!**")
        summary_text = "\n".join([f"- {r['Worker ID']} ({r['Name']}): {r['Days Reported']} Days | Work: {r['Physical Progress (%)']}% | Issue: {r['AI Status']}" for _, r in flagged_site.iterrows()])
        wa_text = f"🚨 *AIVG SITE ANOMALY REPORT*\n\n*School:* OAV Lingipur, Gosani\n*Module:* Site Progress Tracker\n\n*Flagged Records:*\n{summary_text}"
        wa_url = f"https://wa.me/{officer_phone}?text={urllib.parse.quote(wa_text)}"
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            st.link_button("🚨 Dispatch Site Anomaly Alert via WhatsApp", wa_url)
        with col_btn2:
            st.download_button(
                label="📥 Export Site Audit CSV",
                data=display_site.to_csv(index=False).encode('utf-8'),
                file_name="AIVG_Site_Progress_Audit.csv",
                mime="text/csv",
                key="dl_site"
            )
    else:
        st.success("🟢 **BOX 1 NORMAL:** All site work progress and attendance records are verified.")

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
            "Employee ID": st.column_config.TextColumn("Employee ID", width="medium"),
            "Name": st.column_config.TextColumn("Employee Name", width="medium"),
            "Biometric Status": st.column_config.SelectboxColumn("Biometric Status", options=["Verified ✅", "Unverified ❌"], required=True, width="medium"),
            "Daily Rate (₹)": st.column_config.NumberColumn("Daily Rate (₹)", min_value=500, max_value=10000, step=100, format="₹%d", width="medium"),
            "Days Worked": st.column_config.NumberColumn("Days Worked", min_value=0, max_value=31, step=1, width="medium")
        },
        use_container_width=True,
        num_rows="dynamic",
        key="editor_payroll"
    )

    display_payroll = edited_payroll.copy()
    display_payroll["Calculated Base Pay (₹)"] = display_payroll["Daily Rate (₹)"] * display_payroll["Days Worked"]
    display_payroll["AI Status"] = display_payroll.apply(
        lambda r: "🚨 PAY OVERRUN" if r["Calculated Base Pay (₹)"] > 80000 or r["Biometric Status"] == "Unverified ❌" else "Normal ✅",
        axis=1
    )

    # Sidebar Filter Application
    if filter_option == "Flagged Anomalies Only 🚨":
        view_payroll = display_payroll[display_payroll["AI Status"] != "Normal ✅"]
    elif filter_option == "Normal Only ✅":
        view_payroll = display_payroll[display_payroll["AI Status"] == "Normal ✅"]
    else:
        view_payroll = display_payroll

    st.dataframe(
        view_payroll,
        column_config={
            "Employee ID": st.column_config.TextColumn("Employee ID", width="medium"),
            "Daily Rate (₹)": st.column_config.NumberColumn("Daily Rate (₹)", format="₹%d", width="medium"),
            "Days Worked": st.column_config.NumberColumn("Days Worked", width="medium"),
            "Calculated Base Pay (₹)": st.column_config.NumberColumn("Calculated Base Pay (₹)", format="₹%d", width="medium"),
            "AI Status": st.column_config.TextColumn("AI Status", width="medium")
        },
        use_container_width=True,
        hide_index=True
    )

    flagged_payroll = display_payroll[display_payroll["AI Status"] == "🚨 PAY OVERRUN"]
    if not flagged_payroll.empty:
        st.error(f"🚨 **PAYROLL ANOMALY DETECTED ({len(flagged_payroll)} Flagged)!**")
        summary_text = "\n".join([f"- {r['Employee ID']} ({r['Name']}): ₹{r['Calculated Base Pay (₹)']} Pay | Bio: {r['Biometric Status']}" for _, r in flagged_payroll.iterrows()])
        wa_text = f"🚨 *AIVG BASE PAYROLL BREACH ALERT*\n\n*School:* OAV Lingipur, Gosani\n*Flagged Records:*\n{summary_text}"
        wa_url = f"https://wa.me/{officer_phone}?text={urllib.parse.quote(wa_text)}"
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            st.link_button("🚨 Dispatch Base Payroll Case File via WhatsApp", wa_url)
        with col_btn2:
            st.download_button(
                label="📥 Export Payroll Audit CSV",
                data=display_payroll.to_csv(index=False).encode('utf-8'),
                file_name="AIVG_Base_Payroll_Audit.csv",
                mime="text/csv",
                key="dl_payroll"
            )
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
            "Employee ID": st.column_config.TextColumn("Employee ID", width="medium"),
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
        lambda extra: "⚠️ UNAPPROVED DISBURSAL" if extra > 0 else "Normal ✅"
    )

    # Sidebar Filter Application
    if filter_option == "Flagged Anomalies Only 🚨":
        view_extra = display_extra[display_extra["AI Detection Status"] != "Normal ✅"]
    elif filter_option == "Normal Only ✅":
        view_extra = display_extra[display_extra["AI Detection Status"] == "Normal ✅"]
    else:
        view_extra = display_extra

    st.dataframe(
        view_extra,
        column_config={
            "Employee ID": st.column_config.TextColumn("Employee ID", width="medium"),
            "AI Detection Status": st.column_config.TextColumn("AI Detection Status", width="medium")
        },
        use_container_width=True,
        hide_index=True
    )

    flagged_extra = display_extra[display_extra["AI Detection Status"] == "⚠️ UNAPPROVED DISBURSAL"]
    if not flagged_extra.empty:
        st.error(f"🚨 **UNAUTHORIZED EXTRA MONEY DETECTED ({len(flagged_extra)} Violation Flagged)!**")
        extra_summary = "\n".join([f"- {r['Employee ID']} ({r['Name']}): Base ₹{r['Approved Base Salary (₹)']} + Extra ₹{r['Post-Salary Extra Funds (₹)']} via {r['Disbursal Channel']}" for _, r in flagged_extra.iterrows()])
        wa_text = f"🚨 *AIVG EXTRA MONEY BREACH ALERT*\n\n*School:* OAV Lingipur, Gosani\n*Module:* Post-Salary Leakage Inspector\n\n*Unauthorized Payments Detected:*\n{extra_summary}"
        wa_url = f"https://wa.me/{officer_phone}?text={urllib.parse.quote(wa_text)}"
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            st.link_button("🚨 Dispatch Extra Money Breach Alert via WhatsApp", wa_url)
        with col_btn2:
            st.download_button(
                label="📥 Export Extra Funds Audit CSV",
                data=display_extra.to_csv(index=False).encode('utf-8'),
                file_name="AIVG_Extra_Disbursement_Audit.csv",
                mime="text/csv",
                key="dl_extra"
            )
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
            "Total Active Benefits": st.column_config.NumberColumn("Total Active Benefits", min_value=0, max_value=10, step=1, width="medium")
        },
        use_container_width=True,
        num_rows="dynamic",
        key="editor_welfare"
    )

    display_welfare = edited_welfare.copy()
    display_welfare["AI Welfare Status"] = display_welfare["Total Active Benefits"].apply(
        lambda benefits: "🚨 OVER-ENROLLED (>2 Schemes)" if benefits > 2 else "Approved ✅"
    )

    # Sidebar Filter Application
    if filter_option == "Flagged Anomalies Only 🚨":
        view_welfare = display_welfare[display_welfare["AI Welfare Status"].str.contains("🚨")]
    elif filter_option == "Normal Only ✅":
        view_welfare = display_welfare[~display_welfare["AI Welfare Status"].str.contains("🚨")]
    else:
        view_welfare = display_welfare

    st.dataframe(
        view_welfare,
        column_config={
            "Total Active Benefits": st.column_config.NumberColumn("Total Active Benefits", width="medium"),
            "AI Welfare Status": st.column_config.TextColumn("AI Welfare Status", width="medium")
        },
        use_container_width=True,
        hide_index=True
    )

    flagged_welfare = display_welfare[display_welfare["AI Welfare Status"].str.contains("🚨")]
    if not flagged_welfare.empty:
        st.error(f"🚨 **MULTIPLE BENEFIT FRAUD DETECTED ({len(flagged_welfare)} Beneficiary Flagged)!**")
        welfare_summary = "\n".join([f"- {r['Beneficiary Aadhaar ID']} ({r['Citizen Name']}): Enrolled in {r['Total Active Benefits']} Government Schemes" for _, r in flagged_welfare.iterrows()])
        wa_text = f"🚨 *AIVG MULTIPLE SCHEME BENEFIT FRAUD ALERT*\n\n*School:* OAV Lingipur, Gosani\n*Violations Detected:*\n{welfare_summary}"
        wa_url = f"https://wa.me/{officer_phone}?text={urllib.parse.quote(wa_text)}"
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            st.link_button("🚨 Dispatch Benefit Fraud Case File via WhatsApp", wa_url)
        with col_btn2:
            )
            st.download_button(
                label="📥 Export Welfare Audit CSV"
    
    
