import streamlit as st
import pandas as pd
import urllib.parse

st.set_page_config(page_title="AI Vigilance Grid (AIVG)", page_icon="🛡️", layout="wide")

st.title("🛡️ AI Vigilance Grid (AIVG)")
st.caption("Odiaprenuer 3.0 Smart Odisha Hackathon | Cyber Security from Corruption")

st.markdown("---")

# Sidebar Configuration
st.sidebar.header("📱 Higher Officer Dispatch Settings")
officer_phone = st.sidebar.text_input("Officer Mobile (Country Code e.g., 919876543210):", value="919876543210")

menu = st.sidebar.selectbox("Select System Data Feed", ["Payroll & Salary Logs", "Tender Overpricing Audit"])

if menu == "Payroll & Salary Logs":
    st.header("📊 Real-Time Multi-Employee Audit Module")
    st.info("💡 **Interactive Demo:** Edit any employee's salary or biometric status directly in the table to see the AI Status update instantly!")

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

    # 1. Interactive input table for edits
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
            "Salary (INR)": st.column_config.NumberColumn(
                "Salary (INR)",
                min_value=10000,
                max_value=500000,
                step=5000,
                format="₹%d",
                width="small"
            )
        },
        use_container_width=True,
        num_rows="dynamic"
    )

    # 2. Compute dynamic AI Status column in real time
    def calculate_status(row):
        if row["Salary (INR)"] > 80000 or row["Biometric Status"] == "Unverified ❌":
            return "FLAGGED 🚨"
        return "Normal ✅"

    display_df = edited_df.copy()
    display_df["AI Status"] = display_df.apply(calculate_status, axis=1)

    # 3. Show live table with the AI Status column included
    st.subheader("📋 Live Audit Output")
    st.dataframe(
        display_df,
        column_config={
            "AI Status": st.column_config.TextColumn("AI Status", width="medium")
        },
        use_container_width=True,
        hide_index=True
    )

    # 4. Trigger alert banners and WhatsApp buttons if any record is flagged
    flagged_employees = display_df[display_df["AI Status"] == "FLAGGED 🚨"]

    if not flagged_employees.empty:
        st.error(f"🚨 **AUTOMATED VIGILANCE ALERT DETECTED ({len(flagged_employees)} Anomaly Found)!**")
        
        for _, row in flagged_employees.iterrows():
            st.warning(f"⚠️ **Flagged Record:** {row['Employee ID']} ({row['Name']}) | Salary: ₹{row['Salary (INR)']:,} | Status: {row['Biometric Status']}")
        
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
            "Tender ID": st.column_config.TextColumn("Tender ID", width="small"),
            "Department": st.column_config.TextColumn("Department", width="medium"),
            "Budget (Lakhs)": st.column_config.NumberColumn("Budget (Lakhs)", format="₹%d Lakhs", width="small"),
            "Winning Bid (Lakhs)": st.column_config.NumberColumn("Winning Bid (Lakhs)", format="₹%d Lakhs", width="small"),
        },
        use_container_width=True,
        num_rows="dynamic"
    )

    edited_tenders["Increase %"] = ((edited_tenders["Winning Bid (Lakhs)"] - edited_tenders["Budget (Lakhs)"]) / edited_tenders["Budget (Lakhs)"]) * 100
    edited_tenders["AI Status"] = edited_tenders["Increase %"].apply(lambda x: "FLAGGED 🚨" if x > 40 else "Normal ✅")

    st.subheader("📋 Live Audit Output")
    st.dataframe(edited_tenders, use_container_width=True, hide_index=True)

    flagged_tenders = edited_tenders[edited_tenders["AI Status"] == "FLAGGED 🚨"]

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
    
        
        
        
    
  
