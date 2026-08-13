import streamlit as st
import pandas as pd
import urllib.parse
from openai import OpenAI

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Vigilance Grid (AIVG)",
    page_icon="🛡️",
    layout="wide"
)

# =========================================================
# AI FUNCTION
# =========================================================

def ai_risk_analysis(data, module_name):

    if "OPENAI_API_KEY" not in st.secrets:
        return "⚠️ AI API key is not configured in Streamlit Secrets."

    try:
        client = OpenAI(
            api_key=st.secrets["OPENAI_API_KEY"]
        )

        prompt = f"""
You are the AI Risk Analysis Engine of AIVG
(AI Vigilance Grid), a prototype anti-corruption
monitoring system.

Audit Module:
{module_name}

Flagged Records:
{data}

Analyze these records and provide:

1. Risk Level: LOW / MEDIUM / HIGH
2. Risk Score: 0-100
3. Main anomaly detected
4. Three warning indicators
5. Recommended next step

Important:
- Do NOT state that corruption has definitely occurred.
- These are only risk indicators.
- Recommend human verification/investigation.
- Keep the report concise and suitable for a
  government vigilance dashboard.
"""

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f"⚠️ AI analysis error: {str(e)}"


# =========================================================
# HEADER & OVERVIEW
# =========================================================

st.title("🛡️ AI Vigilance Grid (AIVG) - Core Audit Platform")

st.caption(
    "Automated Multi-Vector Anti-Corruption & Fraud Detection System"
)

st.markdown("""
> **System Status:** Active Monitoring  
> **Target Jurisdiction:** Block Development Office, Gosani, Gajapati  
> **Function:** Real-time stream auditing across project sites,
> payroll, welfare distributions, and public procurement.
""")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Vigilance Controls")

officer_phone = st.sidebar.text_input(
    "Vigilance Officer WhatsApp Number",
    value="919556545988",
    help="Enter phone number with country code."
)

st.sidebar.markdown("---")

st.sidebar.subheader("🔍 Audit Filter")

filter_option = st.sidebar.radio(
    "Filter Records across Modules:",
    [
        "Show All Records 📋",
        "Flagged Anomalies Only 🚨",
        "Normal Only ✅"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "🤖 **AI Agent Active:** Monitoring feeds and "
    "flagging irregularities in real-time."
)

# =========================================================
# BOX 1
# SITE WORKER & PROGRESS AUDIT
# =========================================================

with st.container(border=True):

    st.header(
        "🏗️ Box 1: Site Worker Attendance & Progress Lag Audit"
    )

    st.info(
        "💡 **Ghost Worker Detection:** Flags projects where "
        "reported attendance exceeds physical progress by >30%."
    )

    initial_site = pd.DataFrame([
        {
            "Project ID": "PRJ_001",
            "Site Location": "OAV Lingipur Block A",
            "Reported Days Worked": 25,
            "Physical Progress (%)": 80
        },
        {
            "Project ID": "PRJ_002",
            "Site Location": "Boundary Wall Phase 2",
            "Reported Days Worked": 30,
            "Physical Progress (%)": 20
        },
        {
            "Project ID": "PRJ_003",
            "Site Location": "Science Lab Renovation",
            "Reported Days Worked": 15,
            "Physical Progress (%)": 75
        },
        {
            "Project ID": "PRJ_004",
            "Site Location": "Playground Development",
            "Reported Days Worked": 28,
            "Physical Progress (%)": 30
        }
    ])

    edited_site = st.data_editor(
        initial_site,
        column_config={
            "Project ID": st.column_config.TextColumn(
                "Project ID",
                width="medium"
            ),
            "Site Location": st.column_config.TextColumn(
                "Site Location",
                width="medium"
            ),
            "Reported Days Worked": st.column_config.NumberColumn(
                "Reported Days",
                width="medium"
            ),
            "Physical Progress (%)": st.column_config.NumberColumn(
                "Progress (%)",
                format="%d%%",
                width="medium"
            )
        },
        use_container_width=True,
        num_rows="dynamic",
        key="editor_site"
    )

    edited_site["Expected Progress (%)"] = (
        edited_site["Reported Days Worked"] / 30
    ) * 100

    edited_site["Lag Gap (%)"] = (
        edited_site["Expected Progress (%)"]
        - edited_site["Physical Progress (%)"]
    )

    edited_site["AI Status"] = edited_site["Lag Gap (%)"].apply(
        lambda x:
        "⚠️ PROGRESS LAG"
        if x > 30
        else "NORMAL ✅"
    )

    if filter_option == "Flagged Anomalies Only 🚨":
        view_site = edited_site[
            edited_site["AI Status"] != "NORMAL ✅"
        ]

    elif filter_option == "Normal Only ✅":
        view_site = edited_site[
            edited_site["AI Status"] == "NORMAL ✅"
        ]

    else:
        view_site = edited_site

    st.dataframe(
        view_site,
        use_container_width=True,
        hide_index=True
    )

    flagged_site = edited_site[
        edited_site["AI Status"] == "⚠️ PROGRESS LAG"
    ]

    if not flagged_site.empty:

        st.error(
            f"🚨 **GHOST WORKER BREACH DETECTED "
            f"({len(flagged_site)} Project Flagged)!**"
        )

        site_summary = "\n".join([
            f"- {r['Project ID']} ({r['Site Location']}): "
            f"{r['Reported Days Worked']} days logged but only "
            f"{r['Physical Progress (%)']}% progress "
            f"(Lag: {r['Lag Gap (%)']:.1f}%)"
            for _, r in flagged_site.iterrows()
        ])

        wa_text = (
            "🚨 AIVG SITE PROGRESS ALERT\n\n"
            "School: OAV Lingipur, Gosani\n"
            "Flagged Projects:\n"
            f"{site_summary}"
        )

        wa_url = (
            f"https://wa.me/{officer_phone}"
            f"?text={urllib.parse.quote(wa_text)}"
        )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            st.link_button(
                "🚨 Dispatch Site Case File via WhatsApp",
                wa_url
            )

        with col_btn2:
            st.download_button(
                "📥 Export Site Audit CSV",
                edited_site.to_csv(index=False).encode("utf-8"),
                "AIVG_Site_Progress_Audit.csv",
                "text/csv",
                key="dl_site"
            )

    else:
        st.success(
            "🟢 **BOX 1 NORMAL:** Attendance logs match "
            "physical site progress."
        )

st.markdown("---")

# =========================================================
# BOX 2
# PAYROLL AUDIT
# =========================================================

with st.container(border=True):

    st.header(
        "💰 Box 2: Employee Payroll & Excess Salary Audit"
    )

    st.info(
        "💡 **Overpay Audit:** Detects salary disbursals "
        "exceeding sanctioned monthly limits."
    )

    initial_payroll = pd.DataFrame([
        {
            "Employee ID": "EMP_101",
            "Name": "Ramesh Kumar",
            "Role": "Staff",
            "Sanctioned Salary (INR)": 35000,
            "Disbursed Salary (INR)": 35000
        },
        {
            "Employee ID": "EMP_102",
            "Name": "Suresh Mohanty",
            "Role": "Supervisor",
            "Sanctioned Salary (INR)": 45000,
            "Disbursed Salary (INR)": 60000
        },
        {
            "Employee ID": "EMP_103",
            "Name": "Anita Panda",
            "Role": "Accountant",
            "Sanctioned Salary (INR)": 40000,
            "Disbursed Salary (INR)": 40000
        },
        {
            "Employee ID": "EMP_104",
            "Name": "Prakash Swain",
            "Role": "Technical Asst",
            "Sanctioned Salary (INR)": 38000,
            "Disbursed Salary (INR)": 52000
        }
    ])

    edited_payroll = st.data_editor(
        initial_payroll,
        column_config={
            "Employee ID": st.column_config.TextColumn(
                "Emp ID"
            ),
            "Name": st.column_config.TextColumn(
                "Name"
            ),
            "Sanctioned Salary (INR)": st.column_config.NumberColumn(
                "Sanctioned Salary",
                format="₹%d"
            ),
            "Disbursed Salary (INR)": st.column_config.NumberColumn(
                "Disbursed Salary",
                format="₹%d"
            )
        },
        use_container_width=True,
        num_rows="dynamic",
        key="editor_payroll"
    )

    edited_payroll["Excess Amount (INR)"] = (
        edited_payroll["Disbursed Salary (INR)"]
        - edited_payroll["Sanctioned Salary (INR)"]
    )

    edited_payroll["AI Status"] = (
        edited_payroll["Excess Amount (INR)"]
        .apply(
            lambda x:
            "⚠️ EXTRA MONEY"
            if x > 0
            else "NORMAL ✅"
        )
    )

    if filter_option == "Flagged Anomalies Only 🚨":

        view_payroll = edited_payroll[
            edited_payroll["AI Status"] != "NORMAL ✅"
        ]

    elif filter_option == "Normal Only ✅":

        view_payroll = edited_payroll[
            edited_payroll["AI Status"] == "NORMAL ✅"
        ]

    else:
        view_payroll = edited_payroll

    st.dataframe(
        view_payroll,
        use_container_width=True,
        hide_index=True
    )

    flagged_payroll = edited_payroll[
        edited_payroll["AI Status"] == "⚠️ EXTRA MONEY"
    ]

    if not flagged_payroll.empty:

        st.error(
            f"🚨 **PAYROLL OVERRUN BREACH DETECTED "
            f"({len(flagged_payroll)} Employee Flagged)!**"
        )

        payroll_summary = "\n".join([
            f"- {r['Employee ID']} ({r['Name']}): "
            f"Disbursed ₹{r['Disbursed Salary (INR)']} "
            f"vs Sanctioned ₹{r['Sanctioned Salary (INR)']} "
            f"(Excess: +₹{r['Excess Amount (INR)']})"
            for _, r in flagged_payroll.iterrows()
        ])

        wa_text = (
            "🚨 AIVG PAYROLL BREACH ALERT\n\n"
            "School: OAV Lingipur, Gosani\n"
            "Flagged Payroll:\n"
            f"{payroll_summary}"
        )

        wa_url = (
            f"https://wa.me/{officer_phone}"
            f"?text={urllib.parse.quote(wa_text)}"
        )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            st.link_button(
                "🚨 Dispatch Payroll Case File via WhatsApp",
                wa_url
            )

        with col_btn2:
            st.download_button(
                "📥 Export Payroll Audit CSV",
                edited_payroll.to_csv(index=False).encode("utf-8"),
                "AIVG_Payroll_Audit.csv",
                "text/csv",
                key="dl_payroll"
            )

    else:

        st.success(
            "🟢 **BOX 2 NORMAL:** Disbursed salaries "
            "match sanctioned amounts."
        )

st.markdown("---")

# =========================================================
# BOX 3
# EXTRA DISBURSAL AUDIT
# =========================================================

with st.container(border=True):

    st.header(
        "💸 Box 3: Post-Salary Extra Disbursal Audit"
    )

    st.info(
        "💡 **Kickback Detection:** Flags secondary "
        "unapproved financial transfers."
    )

    initial_transfers = pd.DataFrame([
        {
            "Transfer ID": "TRX_801",
            "Employee ID": "EMP_102",
            "Transfer Type": "Bonus / Vendor Transfer",
            "Amount (INR)": 15000,
            "Approval Status": "Unapproved"
        },
        {
            "Transfer ID": "TRX_802",
            "Employee ID": "EMP_101",
            "Transfer Type": "TA / DA Reimbursement",
            "Amount (INR)": 2000,
            "Approval Status": "Approved"
        },
        {
            "Transfer ID": "TRX_803",
            "Employee ID": "EMP_104",
            "Transfer Type": "Special Allowance",
            "Amount (INR)": 12000,
            "Approval Status": "Unapproved"
        },
        {
            "Transfer ID": "TRX_804",
            "Employee ID": "EMP_103",
            "Transfer Type": "Medical Reimbursement",
            "Amount (INR)": 3500,
            "Approval Status": "Approved"
        }
    ])

    edited_transfers = st.data_editor(
        initial_transfers,
        column_config={
            "Transfer ID": st.column_config.TextColumn(
                "Transfer ID"
            ),
            "Employee ID": st.column_config.TextColumn(
                "Emp ID"
            ),
            "Amount (INR)": st.column_config.NumberColumn(
                "Amount",
                format="₹%d"
            ),
            "Approval Status": st.column_config.SelectboxColumn(
                "Approval Status",
                options=["Approved", "Unapproved"]
            )
        },
        use_container_width=True,
        num_rows="dynamic",
        key="editor_transfers"
    )

    edited_transfers["AI Status"] = (
        edited_transfers["Approval Status"]
        .apply(
            lambda x:
            "⚠️ UNAPPROVED TRANSFER"
            if x == "Unapproved"
            else "NORMAL ✅"
        )
    )

    if filter_option == "Flagged Anomalies Only 🚨":

        view_transfers = edited_transfers[
            edited_transfers["AI Status"] != "NORMAL ✅"
        ]

    elif filter_option == "Normal Only ✅":

        view_transfers = edited_transfers[
            edited_transfers["AI Status"] == "NORMAL ✅"
        ]

    else:
        view_transfers = edited_transfers

    st.dataframe(
        view_transfers,
        use_container_width=True,
        hide_index=True
    )

    flagged_transfers = edited_transfers[
        edited_transfers["AI Status"]
        == "⚠️ UNAPPROVED TRANSFER"
    ]

    if not flagged_transfers.empty:

        st.error(
            f"🚨 **UNAPPROVED DISBURSAL BREACH DETECTED "
            f"({len(flagged_transfers)} Transfer Flagged)!**"
        )

        transfer_summary = "\n".join([
            f"- {r['Transfer ID']} "
            f"(Emp {r['Employee ID']}): "
            f"₹{r['Amount (INR)']} "
            f"({r['Transfer Type']})"
            for _, r in flagged_transfers.iterrows()
        ])

        wa_text = (
            "🚨 AIVG EXTRA DISBURSAL ALERT\n\n"
            "School: OAV Lingipur, Gosani\n"
            "Flagged Transfers:\n"
            f"{transfer_summary}"
        )

        wa_url = (
            f"https://wa.me/{officer_phone}"
            f"?text={urllib.parse.quote(wa_text)}"
        )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            st.link_button(
                "🚨 Dispatch Disbursal Case File via WhatsApp",
                wa_url
            )

        with col_btn2:
            st.download_button(
                "📥 Export Extra Disbursal CSV",
                edited_transfers.to_csv(
                    index=False
                ).encode("utf-8"),
                "AIVG_Extra_Disbursal_Audit.csv",
                "text/csv",
                key="dl_transfers"
            )

    else:

        st.success(
            "🟢 **BOX 3 NORMAL:** All secondary "
            "transactions have official approval clearance."
        )

st.markdown("---")

# =========================================================
# BOX 4
# WELFARE AUDIT
# =========================================================

with st.container(border=True):

    st.header(
        "📋 Box 4: Multi-Benefit Scheme Fraud Audit"
    )

    st.info(
        "💡 **Scheme Exploitation:** Flags individuals "
        "enrolled in >2 concurrent schemes."
    )

    initial_welfare = pd.DataFrame([
        {
            "Beneficiary ID": "BEN_301",
            "Aadhaar Hash": "XXXX-XXXX-1234",
            "Schemes Enrolled": "Kalia, PM-Kisan",
            "Enrolled Count": 2
        },
        {
            "Beneficiary ID": "BEN_302",
            "Aadhaar Hash": "XXXX-XXXX-5678",
            "Schemes Enrolled":
                "Kalia, PM-Kisan, NFSA, Subhadra",
            "Enrolled Count": 4
        },
        {
            "Beneficiary ID": "BEN_303",
            "Aadhaar Hash": "XXXX-XXXX-9012",
            "Schemes Enrolled": "NFSA",
            "Enrolled Count": 1
        },
        {
            "Beneficiary ID": "BEN_304",
            "Aadhaar Hash": "XXXX-XXXX-3456",
            "Schemes Enrolled":
                "Kalia, PM-Kisan, Mo Kudia",
            "Enrolled Count": 3
        }
    ])

    edited_welfare = st.data_editor(
        initial_welfare,
        column_config={
            "Beneficiary ID": st.column_config.TextColumn(
                "Beneficiary ID"
            ),
            "Aadhaar Hash": st.column_config.TextColumn(
                "Aadhaar Hash"
            ),
            "Enrolled Count": st.column_config.NumberColumn(
                "Enrolled Count"
            )
        },
        use_container_width=True,
        num_rows="dynamic",
        key="editor_welfare"
    )

    edited_welfare["AI Status"] = (
        edited_welfare["Enrolled Count"]
        .apply(
            lambda x:
            "⚠️ OVER-ENROLLED"
            if x > 2
            else "NORMAL ✅"
        )
    )

    if filter_option == "Flagged Anomalies Only 🚨":

        view_welfare = edited_welfare[
            edited_welfare["AI Status"] != "NORMAL ✅"
        ]

    elif filter_option == "Normal Only ✅":

        view_welfare = edited_welfare[
            edited_welfare["AI Status"] == "NORMAL ✅"
        ]

    else:
        view_welfare = edited_welfare

    st.dataframe(
        view_welfare,
        use_container_width=True,
        hide_index=True
    )

    flagged_welfare = edited_welfare[
        edited_welfare["AI Status"]
        == "⚠️ OVER-ENROLLED"
    ]

    if not flagged_welfare.empty:

        st.error(
            f"🚨 **WELFARE FRAUD BREACH DETECTED "
            f"({len(flagged_welfare)} Beneficiary Flagged)!**"
        )

        welfare_summary = "\n".join([
            f"- {r['Beneficiary ID']}: "
            f"{r['Enrolled Count']} schemes "
            f"({r['Schemes Enrolled']})"
            for _, r in flagged_welfare.iterrows()
        ])

        wa_text = (
            "🚨 AIVG WELFARE FRAUD ALERT\n\n"
            "School: OAV Lingipur, Gosani\n"
            "Flagged Beneficiaries:\n"
            f"{welfare_summary}"
        )

        wa_url = (
            f"https://wa.me/{officer_phone}"
            f"?text={urllib.parse.quote(wa_text)}"
        )

        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            st.link_button(
                "🚨 Dispatch Welfare Case File via WhatsApp",
                wa_url
            )

        with col_btn2:
            st.download_button(
                "📥 Export Welfare Fraud CSV",
                edited_welfare.to_csv(
                    index=False
                ).encode("utf-8"),
                "AIVG_Welfare_Fraud_Audit.csv",
                "text/csv",
                key="dl_welfare"
            )

    else:

        st.success(
            "🟢 **BOX 4 NORMAL:** No multi-scheme "
            "over-enrollment detected."
        )

st.markdown("---")

# =========================================================
# BOX 5
# PROCUREMENT & TENDER AUDIT
# =========================================================

with st.containe        
