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
# AI RISK ANALYSIS FUNCTION
# =========================================================

def ai_risk_analysis(data, module_name):

    if "OPENAI_API_KEY" not in st.secrets:
        return "⚠️ OPENAI_API_KEY is not configured in Streamlit Secrets."

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

Analyze the records and provide:

1. Risk Level: LOW / MEDIUM / HIGH
2. Risk Score: 0-100
3. Main anomaly detected
4. Three warning indicators
5. Recommended next step

Important:
- Do not claim that corruption has definitely occurred.
- These are only risk indicators.
- Recommend human verification.
- Keep the report concise and professional.
"""

        response = client.responses.create(
            model="gpt-5-mini",
            input=prompt
        )

        return response.output_text

    except Exception as e:
        return f"⚠️ AI analysis error: {str(e)}"


# =========================================================
# HEADER
# =========================================================

st.title(
    "🛡️ AI Vigilance Grid (AIVG) - Core Audit Platform"
)

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
    value="919556545988"
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
    "🤖 **AI Agent Active:** Monitoring feeds and flagging irregularities."
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
        "💡 Flags projects where reported attendance exceeds "
        "physical progress by >30%."
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
            f"🚨 GHOST WORKER BREACH DETECTED "
            f"({len(flagged_site)} Project Flagged)!"
        )

        site_summary = "\n".join([
            f"- {r['Project ID']} ({r['Site Location']}): "
            f"{r['Reported Days Worked']} days logged, "
            f"{r['Physical Progress (%)']}% progress"
            for _, r in flagged_site.iterrows()
        ])

        wa_text = (
            "🚨 AIVG SITE PROGRESS ALERT\n\n"
            "School: OAV Lingipur, Gosani\n"
            f"{site_summary}"
        )

        wa_url = (
            f"https://wa.me/{officer_phone}"
            f"?text={urllib.parse.quote(wa_text)}"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.link_button(
                "🚨 Dispatch Site Alert",
                wa_url
            )

        with col2:
            st.download_button(
                "📥 Export Site Audit CSV",
                edited_site.to_csv(
                    index=False
                ).encode("utf-8"),
                "AIVG_Site_Progress_Audit.csv",
                "text/csv",
                key="dl_site"
            )

    else:

        st.success(
            "🟢 BOX 1 NORMAL: Attendance logs match physical progress."
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
        "💡 Detects salary disbursals exceeding sanctioned limits."
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
        use_container_width=True,
        num_rows="dynamic",
        key="editor_payroll"
    )

    edited_payroll["Excess Amount (INR)"] = (
        edited_payroll["Disbursed Salary (INR)"]
        - edited_payroll["Sanctioned Salary (INR)"]
    )

    edited_payroll["AI Status"] = (
        edited_payroll["Excess Amount (INR)"].apply(
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
            f"🚨 PAYROLL OVERRUN DETECTED "
            f"({len(flagged_payroll)} Employee Flagged)!"
        )

        payroll_summary = "\n".join([
            f"- {r['Employee ID']} ({r['Name']}): "
            f"Excess ₹{r['Excess Amount (INR)']}"
            for _, r in flagged_payroll.iterrows()
        ])

        wa_text = (
            "🚨 AIVG PAYROLL ALERT\n\n"
            f"{payroll_summary}"
        )

        wa_url = (
            f"https://wa.me/{officer_phone}"
            f"?text={urllib.parse.quote(wa_text)}"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.link_button(
                "🚨 Dispatch Payroll Alert",
                wa_url
            )

        with col2:
            st.download_button(
                "📥 Export Payroll CSV",
                edited_payroll.to_csv(
                    index=False
                ).encode("utf-8"),
                "AIVG_Payroll_Audit.csv",
                "text/csv",
                key="dl_payroll"
            )

    else:

        st.success(
            "🟢 BOX 2 NORMAL: Salaries match sanctioned amounts."
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
        "💡 Flags secondary unapproved financial transfers."
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
        use_container_width=True,
        num_rows="dynamic",
        key="editor_transfers"
    )

    edited_transfers["AI Status"] = (
        edited_transfers["Approval Status"].apply(
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
            f"🚨 UNAPPROVED TRANSFER DETECTED "
            f"({len(flagged_transfers)} Transfer Flagged)!"
        )

        transfer_summary = "\n".join([
            f"- {r['Transfer ID']}: "
            f"₹{r['Amount (INR)']} "
            f"({r['Transfer Type']})"
            for _, r in flagged_transfers.iterrows()
        ])

        wa_text = (
            "🚨 AIVG EXTRA DISBURSAL ALERT\n\n"
            f"{transfer_summary}"
        )

        wa_url = (
            f"https://wa.me/{officer_phone}"
            f"?text={urllib.parse.quote(wa_text)}"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.link_button(
                "🚨 Dispatch Disbursal Alert",
                wa_url
            )

        with col2:
            st.download_button(
                "📥 Export Disbursal CSV",
                edited_transfers.to_csv(
                    index=False
                ).encode("utf-8"),
                "AIVG_Extra_Disbursal_Audit.csv",
                "text/csv",
                key="dl_transfers"
            )

    else:

        st.success(
            "🟢 BOX 3 NORMAL: All transfers have approval clearance."
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
        "💡 Flags individuals enrolled in more than 2 schemes."
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
        use_container_width=True,
        num_rows="dynamic",
        key="editor_welfare"
    )

    edited_welfare["AI Status"] = (
        edited_welfare["Enrolled Count"].apply(
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
            f"🚨 WELFARE OVER-ENROLLMENT DETECTED "
            f"({len(flagged_welfare)} Beneficiary Flagged)!"
        )

        welfare_summary = "\n".join([
            f"- {r['Beneficiary ID']}: "
            f"{r['Enrolled Count']} schemes"
            for _, r in flagged_welfare.iterrows()
        ])

        wa_text = (
            "🚨 AIVG WELFARE ALERT\n\n"
            f"{welfare_summary}"
        )

        wa_url = (
            f"https://wa.me/{officer_phone}"
            f"?text={urllib.parse.quote(wa_text)}"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.link_button(
                "🚨 Dispatch Welfare Alert",
                wa_url
            )

        with col2:
            st.download_button(
                "📥 Export Welfare CSV",
                edited_welfare.to_csv(
                    index=False
                ).encode("utf-8"),
                "AIVG_Welfare_Fraud_Audit.csv",
                "text/csv",
                key="dl_welfare"
            )

    else:

        st.success(
            "🟢 BOX 4 NORMAL: No over-enrollment detected."
        )

st.markdown("---")

# =========================================================
# BOX 5
# PROCUREMENT & TENDER AUDIT
# =========================================================

with st.container(border=True):

    st.header(
        "📊 Box 5: Procurement & Tender Audit"
    )

    st.info(
        "💡 Detects bids exceeding 40% of estimated budget."
    )

    initial_tenders = pd.DataFrame([
        {
            "Tender ID": "TEN_101",
            "Department": "Roads & Building",
            "Budget (Lakhs INR)": 50,
            "Winning Bid (Lakhs INR)": 52
        },
        {
            "Tender ID": "TEN_102",
            "Department": "Water Resources",
            "Budget (Lakhs INR)": 60,
            "Winning Bid (Lakhs INR)": 90
        },
        {
            "Tender ID": "TEN_103",
            "Department": "Rural Development",
            "Budget (Lakhs INR)": 40,
            "Winning Bid (Lakhs INR)": 41
        },
        {
            "Tender ID": "TEN_104",
            "Department": "Health Infrastructure",
            "Budget (Lakhs INR)": 100,
            "Winning Bid (Lakhs INR)": 150
        }
    ])

    edited_tenders = st.data_editor(
        initial_tenders,
        use_container_width=True,
        num_rows="dynamic",
        key="editor_tenders"
    )

    edited_tenders["Inflation (%)"] = (
        (
            edited_tenders["Winning Bid (Lakhs INR)"]
            - edited_tenders["Budget (Lakhs INR)"]
        )
        / edited_tenders["Budget (Lakhs INR)"]
    ) * 100

    edited_tenders["AI Status"] = (
        edited_tenders["Inflation (%)"].apply(
            lambda x:
            "⚠️ HIGH VARIANCE"
            if x > 40
            else "NORMAL ✅"
        )
    )

    if filter_option == "Flagged Anomalies Only 🚨":

        view_tenders = edited_tenders[
            edited_tenders["AI Status"] != "NORMAL ✅"
        ]

    elif filter_option == "Normal Only ✅":

        view_tenders = edited_tenders[
            edited_tenders["AI Status"] == "NORMAL ✅"
        ]

    else:

        view_tenders = edited_tenders

    st.dataframe(
        view_tenders,
        use_container_width=True,
        hide_index=True
    )

    flagged_tenders = edited_tenders[
        edited_tenders["AI Status"]
        == "⚠️ HIGH VARIANCE"
    ]

    if not flagged_tenders.empty:

        st.error(
            f"🚨 TENDER VARIANCE DETECTED "
            f"({len(flagged_tenders)} Tender Flagged)!"
        )

        tender_summary = "\n".join([
            f"- {r['Tender ID']} ({r['Department']}): "
            f"Budget ₹{r['Budget (Lakhs INR)']}L vs "
            f"Bid ₹{r['Winning Bid (Lakhs INR)']}L "
            f"(+{r['Inflation (%)']:.1f}%)"
            for _, r in flagged_tenders.iterrows()
        ])

        wa_text = (
            "🚨 AIVG TENDER ALERT\n\n"
            f"{tender_summary}"
        )

        wa_url = (
            f"https://wa.me/{officer_phone}"
            f"?text={urllib.parse.quote(wa_text)}"
        )

        col1, col2 = st.columns(2)

        with col1:
            st.link_button(
                "🚨 Dispatch Tender Alert",
                wa_url
            )

        with col2:
            st.download_button(
                "📥 Export Tender CSV",
 
