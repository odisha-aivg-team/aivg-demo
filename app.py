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
        
    
        
    
            
        
        
        
    
    
    
    
        
        
        
    
  
