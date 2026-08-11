# =========================================================
# BOX 5: PROCUREMENT & TENDER AUDIT
# =========================================================
with st.container(border=True):
    st.header("📊 Box 5: Real-Time Procurement & Tender Audit Module")
    st.info("💡 **Tender Audit:** Detects overpricing and inflated bids exceeding 40% of the estimated budget.")

    initial_tenders = pd.DataFrame([
        {"Tender ID": "TEN_101", "Department": "Roads & Building", "Budget (Lakhs INR)": 50, "Winning Bid (Lakhs INR)": 52},
        {"Tender ID": "TEN_102", "Department": "Water Resources", "Budget (Lakhs INR)": 60, "Winning Bid (Lakhs INR)": 90},
        {"Tender ID": "TEN_103", "Department": "Rural Development", "Budget (Lakhs INR)": 40, "Winning Bid (Lakhs INR)": 41},
        {"Tender ID": "TEN_104", "Department": "Health Infrastructure", "Budget (Lakhs INR)": 100, "Winning Bid (Lakhs INR)": 150},
    ])

    edited_tenders = st.data_editor(
        initial_tenders,
        column_config={
            "Tender ID": st.column_config.TextColumn("Tender ID", width="medium"),
            "Department": st.column_config.TextColumn("Department", width="medium"),
            "Budget (Lakhs INR)": st.column_config.NumberColumn("Budget (Lakhs)", format="₹%d L", width="medium"),
            "Winning Bid (Lakhs INR)": st.column_config.NumberColumn("Winning Bid (Lakhs)", format="₹%d L", width="medium"),
        },
        use_container_width=True,
        num_rows="dynamic",
        key="editor_tenders"
    )

    edited_tenders["Inflation (%)"] = ((edited_tenders["Winning Bid (Lakhs INR)"] - edited_tenders["Budget (Lakhs INR)"]) / edited_tenders["Budget (Lakhs INR)"]) * 100
    edited_tenders["AI Status"] = edited_tenders["Inflation (%)"].apply(lambda x: "⚠️ HIGH VARIANCE" if x > 40 else "NORMAL ✅")

    if filter_option == "Flagged Anomalies Only 🚨":
        view_tenders = edited_tenders[edited_tenders["AI Status"] != "NORMAL ✅"]
    elif filter_option == "Normal Only ✅":
        view_tenders = edited_tenders[edited_tenders["AI Status"] == "NORMAL ✅"]
    else:
        view_tenders = edited_tenders

    st.dataframe(
        view_tenders,
        column_config={
            "Tender ID": st.column_config.TextColumn("Tender ID", width="medium"),
            "AI Status": st.column_config.TextColumn("AI Status", width="medium")
        },
        use_container_width=True,
        hide_index=True
    )

    flagged_tenders = edited_tenders[edited_tenders["AI Status"] == "⚠️ HIGH VARIANCE"]
    if not flagged_tenders.empty:
        st.error(f"🚨 **TENDER INFLATION BREACH DETECTED ({len(flagged_tenders)} Tender Flagged)!**")
        tender_summary = "\n".join([
            f"- {r['Tender ID']} ({r['Department']}): Budget ₹{r['Budget (Lakhs INR)']}L vs Bid ₹{r['Winning Bid (Lakhs INR)']}L" 
            for _, r in flagged_tenders.iterrows()
        ])
        wa_text = "🚨 *AIVG TENDER BREACH*\n\n*Target:* Gosani Block\n" + tender_summary
        wa_url = f"https://wa.me/{officer_phone}?text={urllib.parse.quote(wa_text)}"
        
        col_btn1, col_btn2 = st.columns([1, 1])
        with col_btn1:
            st.link_button("🚨 Dispatch Case File", wa_url)
        with col_btn2:
            st.download_button(
                label="📥 Export Audit CSV",
                data=edited_tenders.to_csv(index=False).encode('utf-8'),
                file_name="AIVG_Tender_Audit.csv",
                mime="text/csv",
                key="dl_tenders"
            )
    else:
        st.success("🟢 **BOX 5 NORMAL:** All submitted bids are within safe budget variance limits (<40% deviation).")
        
