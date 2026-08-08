import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="AI Vigilance Grid (AIVG)", page_icon="🛡️")

st.title("🛡️ AI Vigilance Grid (AIVG)")
st.caption("Odiaprenuer 3.0 Smart Odisha Hackathon | Cyber Security from Corruption")

st.markdown("---")

# Sidebar Configuration
st.sidebar.header("📱 Higher Officer Dispatch Settings")
officer_phone = st.sidebar.text_input("Officer Mobile (Country Code e.g., 919876543210):", value="919876543210")

menu = st.sidebar.selectbox("Select System Data Feed", ["Payroll & Salary Logs", "Tender Overpricing Audit"])

if menu == "Payroll & Salary Logs":
    st.header("📊 Real-Time Multi-Employee Audit Module")
    st.info("💡 **Interactive Demo:** Click inside any row below to directly edit salary amounts or biometric verification status!")

    # Initial employee table data
    initial_data = pd.DataFrame([
        {"Employee ID": "EMP_001", "Name": "Ramesh Mohanty", "Biometric Status": "Verified ✅", "Salary (INR)": 45000},
        {"Employee ID": "EMP_002", "Name": "Sita Das", "Biometric Status": "Verified ✅", "Salary (INR)": 50000},
        {"Employee ID": "EMP_003", "Name": "Prakash Naik", "Biometric Status": "Verified ✅", "Salary (INR)": 42000},
        {"Employee ID": "EMP_004", "Name": "Ananya Patnaik", "Biometric Status": "Verified ✅", "Salary (INR)": 48000},
        {"Employee ID": "EMP_005", "Name": "Soumya Ranjan", "Biometric Status": "Verified ✅", "Salary (INR)": 46000},
        {"Employee ID": "EMP_006", "Name": "Priya Mishra", "Biometric Status": "Verified ✅", "Salary (INR)": 51000},
        {"Employee ID": "EMP_007", "Name": "Manas Swain", "Biometric Status": "Verified ✅", "Salary (INR)": 44000},
    ])

    # Make the whole table interactive/editable
    edited_df = st.data_editor(
        initial_data,
        column_config={
            "Biometric Status": st.column_config.SelectboxColumn(
                "Biometric Status",
                options=["Verified ✅", "Unverified ❌"],
                required=True
            ),
            "Salary (INR)": st.column_config.NumberColumn(
                "Salary (INR)",
                min_value=10000,
                max_value=500000,
                step=5000,
                format="₹%d"
            )
        },
        use_container_width=True,
        num_rows="dynamic"  # Allows you to add/delete rows live if needed!
    )

    # Real-Time Anomaly Detection Engine across ALL employees
    flagged_employees = edited_df[
        (edited_df["Salary (INR)"] > 70000) | (edited_df["Biometric Status"] == "Unverified ❌")
    ]

    if not flagged_employees.empty:
        st.error(f"🚨 **AUTOMATED VIGILANCE ALERT DETECTED ({len(flagged_employees)} Anomaly Found)!**")
        
        # Display each flagged record details
        for _, row in flagged_employees.iterrows():
            st.warning(f"⚠️ **Flagged Record:** {row['Employee ID']} ({row['Name']}) | Salary: ₹{row['Salary (INR)']:,} | Status: {row['Biometric Status']}")
        
        # WhatsApp Pre-filled Alert Message
        summary_text = "\n".join([f"- {r['Employee ID']} ({r['Name']}): ₹{r['Salary (INR)']} [{r['Biometric Status']}]" for _, r in flagged_employees.iterrows()])
        wa_text = f"🚨 *AIVG EMERGENCY VIGILANCE ALERT*\n\nAnomalies detected in Payroll Feed:\n{summary_text}\n\n*Action Required:* Immediate audit review."
        encoded_text = urllib.parse.quote(wa_text)
        wa_url = f"https://wa.me/{officer_phone}?text={encoded_text}"
        
        st.markdown("---")
        st.link_button("🚨 Dispatch Real-Time WhatsApp Alert to Officer", wa_url)
    else:
        st.success("🟢 **SYSTEM NORMAL:** All payroll amounts and biometrics are verified within safe limits.")

elif menu == "Tender Overpricing Audit":
    st.header("📊 Real-Time Procurement Audit Module")
    st.info("💡 **Interactive Demo:** Click inside any tender row to edit estimated budgets or winning bids!")

    initial_tenders = pd.DataFrame([
        {"Tender ID": "TEN_101", "Department": "Roads & Building", "Budget (Lakhs)": 50, "Winning Bid (Lakhs)": 52},
        {"Tender ID": "TEN_102", "Department": "Water Resources", "Budget (Lakhs)": 60, "Winning Bid (Lakhs)": 64},
        {"Tender ID": "TEN_103", "Department": "Rural Development", "Budget (Lakhs)": 40, "Winning Bid (Lakhs)": 41},
        {"Tender ID": "TEN_104", "Department": "Health Infrastructure", "Budget (Lakhs)": 100, "Winning Bid (Lakhs)": 105},
    ])

    edited_tenders = st.data_editor(
        initial_tenders,
        column_config={
            "Budget (Lakhs)": st.column_config.NumberColumn(format="₹%d Lakhs"),
            "Winning Bid (Lakhs)": st.column_config.NumberColumn(format="₹%d Lakhs"),
        },
        use_container_width=True,
        num_rows="dynamic"
    )

    # Calculate percentage deviation for all tenders
    edited_tenders["Increase %"] = ((edited_tenders["Winning Bid (Lakhs)"] - edited_tenders["Budget (Lakhs)"]) / edited_tenders["Budget (Lakhs)"]) * 100
    flagged_tenders = edited_tenders[edited_tenders["Increase %"] > 40]

    if not flagged_tenders.empty:
        st.error(f"🚨 **PROCUREMENT BREACH ALERT ({len(flagged_tenders)} Tender Flagged)!**")
        
        for _, row in flagged_tenders.iterrows():
            st.warning(f"🚨 **Tender ID:** {row['Tender ID']} ({row['Department']}) | Budget: ₹{row['Budget (Lakhs)']}L | Bid: ₹{row['Winning Bid (Lakhs)']}L (+{row['Increase %']:.1f}% inflation)")

        wa_text = f"🚨 *AIVG PROCUREMENT BREACH ALERT*\n\nSuspicious tender inflation detected. Forwarded to Vigilance Department."
        encoded_text = urllib.parse.quote(wa_text)
        wa_url = f"https://wa.me/{officer_phone}?text={encoded_text}"
        
        st.markdown("---")
        st.link_button("🚨 Dispatch Real-Time WhatsApp Alert to Officer", wa_url)
    else:
        st.success("🟢 **TENDERS APPROVED:** All winning bids are within safe threshold limits (<40% deviation).")
        
        
    
  
