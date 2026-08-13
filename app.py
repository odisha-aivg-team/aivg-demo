import streamlit as st
import pandas as pd
import urllib.parse

# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="AI Vigilance Grid (AIVG)",
    page_icon="🛡️",
    layout="wide"
)

# =========================================================
# HEADER
# =========================================================

st.title("🛡️ AI Vigilance Grid (AIVG)")
st.subheader("Core Audit & Risk Monitoring Platform")

st.caption(
    "Automated Multi-Vector Anti-Corruption & Fraud Detection System"
)

st.markdown(
    """
    **System Status:** 🟢 Active Monitoring

    **Target Jurisdiction:** Block Development Office, Gosani, Gajapati

    **Function:** Prototype system for identifying unusual patterns
    in project progress, payroll, transfers, welfare schemes and procurement.
    """
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("⚙️ Vigilance Controls")

officer_phone = st.sidebar.text_input(
    "Vigilance Officer WhatsApp Number",
    value="919556545988"
)

st.sidebar.markdown("---")

filter_option = st.sidebar.radio(
    "Audit Filter",
    [
        "Show All Records 📋",
        "Flagged Anomalies Only 🚨",
        "Normal Only ✅"
    ]
)

st.sidebar.markdown("---")

st.sidebar.info(
    "🤖 AI Agent Status: Ready for risk analysis"
)

# =========================================================
# BOX 1
# SITE WORKER & PROGRESS
# =========================================================

st.markdown("## 🏗️ Box 1: Site Worker & Progress Audit")

with st.container(border=True):

    st.info(
        "Flags projects where reported working days indicate "
        "a significant mismatch with physical progress."
    )

    initial_site = pd.DataFrame(
        [
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
        ]
    )

    edited_site = st.data_editor(
        initial_site,
        use_container_width=True,
        num_rows="dynamic",
        key="site_editor"
    )

    edited_site["Expected Progress (%)"] = (
        edited_site["Reported Days Worked"] / 30
    ) * 100

    edited_site["Lag Gap (%)"] = (
        edited_site["Expected Progress (%)"]
        - edited_site["Physical Progress (%)"]
    )

    edited_site["AI Status"] = edited_site["Lag Gap (%)"].apply(
        lambda x: "⚠️ PROGRESS LAG"
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
            f"🚨 {len(flagged_site)} project(s) flagged for review."
        )

        site_summary = "\n".join(
            [
                f"- {row['Project ID']} | "
                f"{row['Site Location']} | "
                f"Progress: {row['Physical Progress (%)']}%"
                for _, row in flagged_site.iterrows()
            ]
        )

        whatsapp_text = (
            "AIVG SITE AUDIT ALERT\n\n"
            + site_summary
        )

        whatsapp_url = (
            "https://wa.me/"
            + officer_phone
            + "?text="
            + urllib.parse.quote(whatsapp_text)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.link_button(
                "🚨 Send WhatsApp Alert",
                whatsapp_url
            )

        with col2:

            st.download_button(
                label="📥 Download Site Audit",
                data=edited_site.to_csv(
                    index=False
                ).encode("utf-8"),
                file_name="AIVG_Site_Audit.csv",
                mime="text/csv",
                key="site_download"
            )

    else:

        st.success(
            "🟢 No site progress anomalies detected."
        )

# =========================================================
# BOX 2
# PAYROLL
# =========================================================

st.markdown("---")
st.markdown("## 💰 Box 2: Employee Payroll Audit")

with st.container(border=True):

    st.info(
        "Detects differences between sanctioned and disbursed salary."
    )

    initial_payroll = pd.DataFrame(
        [
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
                "Role": "Technical Assistant",
                "Sanctioned Salary (INR)": 38000,
                "Disbursed Salary (INR)": 52000
            }
        ]
    )

    edited_payroll = st.data_editor(
        initial_payroll,
        use_container_width=True,
        num_rows="dynamic",
        key="payroll_editor"
    )

    edited_payroll["Excess Amount (INR)"] = (
        edited_payroll["Disbursed Salary (INR)"]
        - edited_payroll["Sanctioned Salary (INR)"]
    )

    edited_payroll["AI Status"] = (
        edited_payroll["Excess Amount (INR)"].apply(
            lambda x: "⚠️ EXTRA MONEY"
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
            f"🚨 {len(flagged_payroll)} payroll record(s) flagged."
        )

        payroll_text = "\n".join(
            [
                f"- {row['Employee ID']} | "
                f"Excess: ₹{row['Excess Amount (INR)']}"
                for _, row in flagged_payroll.iterrows()
            ]
        )

        whatsapp_text = (
            "AIVG PAYROLL ALERT\n\n"
            + payroll_text
        )

        whatsapp_url = (
            "https://wa.me/"
            + officer_phone
            + "?text="
            + urllib.parse.quote(whatsapp_text)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.link_button(
                "🚨 Send Payroll Alert",
                whatsapp_url
            )

        with col2:

            st.download_button(
                label="📥 Download Payroll Audit",
                data=edited_payroll.to_csv(
                    index=False
                ).encode("utf-8"),
                file_name="AIVG_Payroll_Audit.csv",
                mime="text/csv",
                key="payroll_download"
            )

    else:

        st.success(
            "🟢 No payroll anomalies detected."
        )

# =========================================================
# BOX 3
# EXTRA DISBURSAL
# =========================================================

st.markdown("---")
st.markdown("## 💸 Box 3: Extra Disbursal Audit")

with st.container(border=True):

    st.info(
        "Flags secondary transfers that do not have approval."
    )

    initial_transfers = pd.DataFrame(
        [
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
        ]
    )

    edited_transfers = st.data_editor(
        initial_transfers,
        use_container_width=True,
        num_rows="dynamic",
        key="transfer_editor"
    )

    edited_transfers["AI Status"] = (
        edited_transfers["Approval Status"].apply(
            lambda x: "⚠️ UNAPPROVED TRANSFER"
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
            f"🚨 {len(flagged_transfers)} transfer(s) flagged."
        )

        transfer_text = "\n".join(
            [
                f"- {row['Transfer ID']} | "
                f"₹{row['Amount (INR)']} | "
                f"{row['Transfer Type']}"
                for _, row in flagged_transfers.iterrows()
            ]
        )

        whatsapp_text = (
            "AIVG EXTRA DISBURSAL ALERT\n\n"
            + transfer_text
        )

        whatsapp_url = (
            "https://wa.me/"
            + officer_phone
            + "?text="
            + urllib.parse.quote(whatsapp_text)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.link_button(
                "🚨 Send Disbursal Alert",
                whatsapp_url
            )

        with col2:

            st.download_button(
                label="📥 Download Disbursal Audit",
                data=edited_transfers.to_csv(
                    index=False
                ).encode("utf-8"),
                file_name="AIVG_Disbursal_Audit.csv",
                mime="text/csv",
                key="transfer_download"
            )

    else:

        st.success(
            "🟢 No unapproved transfers detected."
        )

# =========================================================
# BOX 4
# WELFARE
# =========================================================

st.markdown("---")
st.markdown("## 📋 Box 4: Welfare Scheme Audit")

with st.container(border=True):

    st.info(
        "Flags beneficiaries enrolled in more than two schemes."
    )

    initial_welfare = pd.DataFrame(
        [
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
        ]
    )

    edited_welfare = st.data_editor(
        initial_welfare,
        use_container_width=True,
        num_rows="dynamic",
        key="welfare_editor"
    )

    edited_welfare["AI Status"] = (
        edited_welfare["Enrolled Count"].apply(
            lambda x: "⚠️ OVER-ENROLLED"
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
            f"🚨 {len(flagged_welfare)} beneficiary record(s) flagged."
        )

        welfare_text = "\n".join(
            [
                f"- {row['Beneficiary ID']} | "
                f"{row['Enrolled Count']} schemes"
                for _, row in flagged_welfare.iterrows()
            ]
        )

        whatsapp_text = (
            "AIVG WELFARE ALERT\n\n"
            + welfare_text
        )

        whatsapp_url = (
            "https://wa.me/"
            + officer_phone
            + "?text="
            + urllib.parse.quote(whatsapp_text)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.link_button(
                "🚨 Send Welfare Alert",
                whatsapp_url
            )

        with col2:

            st.download_button(
                label="📥 Download Welfare Audit",
                data=edited_welfare.to_csv(
                    index=False
                ).encode("utf-8"),
                file_name="AIVG_Welfare_Audit.csv",
                mime="text/csv",
                key="welfare_download"
            )

    else:

        st.success(
            "🟢 No welfare over-enrollment detected."
        )

# =========================================================
# BOX 5
# PROCUREMENT & TENDER
# =========================================================

st.markdown("---")
st.markdown("## 📊 Box 5: Procurement & Tender Audit")

with st.container(border=True):

    st.info(
        "Flags winning bids that exceed the estimated budget by more than 40%."
    )

    initial_tenders = pd.DataFrame(
        [
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
        ]
    )

    edited_tenders = st.data_editor(
        initial_tenders,
        use_container_width=True,
        num_rows="dynamic",
        key="tender_editor"
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
            lambda x: "⚠️ HIGH VARIANCE"
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
            f"🚨 {len(flagged_tenders)} tender(s) flagged."
        )

        tender_text = "\n".join(
            [
                f"- {row['Tender ID']} | "
                f"Budget ₹{row['Budget (Lakhs INR)']}L | "
                f"Bid ₹{row['Winning Bid (Lakhs INR)']}L | "
                f"Variance {row['Inflation (%)']:.1f}%"
                for _, row in flagged_tenders.iterrows()
            ]
        )

        whatsapp_text = (
            "AIVG TENDER ALERT\n\n"
            + tender_text
        )

        whatsapp_url = (
            "https://wa.me/"
            + officer_phone
            + "?text="
            + urllib.parse.quote(whatsapp_text)
        )

        col1, col2 = st.columns(2)

        with col1:

            st.link_button(
                "🚨 Send Tender Alert",
                whatsapp_url
            )

        with col2:

            st.download_button(
                label="📥 Download Tender Audit",
                data=edited_tenders.to_csv(
                    index=False
                ).encode("utf-8"),
                file_name="AIVG_Tender_Audit.csv",
                mime="text/csv",
                key="tender_download"
            )

    else:

        st.success(
            "🟢 No tender variance above the defined threshold."
        )

# =========================================================
# BOX 6
# AI RISK ANALYSIS
# =========================================================

st.markdown("---")
st.markdown("## 🤖 Box 6: AI Risk Analysis Engine")
 with st.container(border=True):

    st.info(
        "This prototype converts detected anomalies into "
        "a risk assessment for human review."
    )

    selected_module = st.selectbox(
        "Select Module for Risk Analysis",
        [
            "Site Worker & Progress",
            "Payroll",
            "Extra Disbursal",
            "Welfare Scheme",
            "Procurement & Tender"
        ],
        key="ai_module"
    )
