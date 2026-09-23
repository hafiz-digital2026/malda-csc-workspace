import streamlit as st
import pandas as pd
import urllib.parse
import os

st.set_page_config(page_title="Digital Services CSC Workspace", layout="wide")

# 🔒 1. LOGIN / PASSWORD SYSTEM
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        st.title("🔐 Digital Services - Portal Login")
        user = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            # Aap apna Username aur Password yahan badal sakte hain
            if user == "digital" and password == "hafiz123":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("Galat Username ya Password!")
        return False
    return True

if check_password():
    # Database File Path
    DB_PATH = "COMPLETE_70K_DATABASE.csv"

    # Sidebar Navigation Menu (PDF Tools Hata Diya Gaya Hai)
    st.sidebar.title("📌 CSC Workspace")
    menu = st.sidebar.radio("Go to:", ["🏠 Dashboard", "🔍 Customer & Kisan Directory"])

    # --- TAB 1: DASHBOARD ---
    if menu == "🏠 Dashboard":
        st.title("📊 CSC Master Database Dashboard")
        st.write("Harishchandrapur Block-1 Kisan & Shop Customer Analytics")
        
        if os.path.exists(DB_PATH):
            df = pd.read_csv(DB_PATH)
            m1, m2, m3 = st.columns(3)
            m1.metric("Total Unique Contacts", f"{len(df):,}")
            m2.metric("Total Kisans", f"{len(df[df['Category'] == 'Kisan']):,}")
            m3.metric("Shop Visitors", f"{len(df[df['Category'] == 'Shop Visitor']):,}")
            
            st.divider()
            st.subheader("📍 GP-wise Breakdown")
            gp_counts = df['GP_Location'].value_counts()
            st.bar_chart(gp_counts)
            
            st.divider()
            st.subheader("📥 Export Complete Database")
            
            # CSV Export Button
            csv_data = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Download Complete Database (CSV - 33,789 Records)",
                data=csv_data,
                file_name="CSC_COMPLETE_33K_DATABASE.csv",
                mime="text/csv",
                type="primary"
            )
        else:
            st.error("Database CSV file nahi mili! Kripya repository me CSV file check karein.")

    # --- TAB 2: SEARCH ENGINE & WHATSAPP ---
    elif menu == "🔍 Customer & Kisan Directory":
        st.title("🔍 Customer & Kisan Directory Search Engine")
        
        if os.path.exists(DB_PATH):
            df = pd.read_csv(DB_PATH)
            
            c1, c2 = st.columns(2)
            with c1:
                query = st.text_input("Naam ya Mobile Number se search karein:")
            with c2:
                gp_list = ["ALL"] + [str(x) for x in df['GP_Location'].dropna().unique()]
                gp_filter = st.selectbox("Gram Panchayat Filter:", gp_list)
                
            filtered = df.copy()
            if gp_filter != "ALL":
                filtered = filtered[filtered['GP_Location'] == gp_filter]
                
            if query:
                filtered = filtered[
                    filtered['Name'].astype(str).str.contains(query, case=False, na=False) |
                    filtered['Mobile'].astype(str).str.contains(query, na=False)
                ]

            st.success(f"Total Matches Found: {len(filtered)}")
            
            # Download Filtered Results Button
            filtered_csv = filtered.to_csv(index=False).encode('utf-8')
            st.download_button(
                label=f"📥 Download Selected ({len(filtered)} Records)",
                data=filtered_csv,
                file_name=f"Filtered_Contacts_{gp_filter}.csv",
                mime="text/csv"
            )
            
            # Table Display
            st.dataframe(filtered[['Name', 'Father_Husband_Name', 'GP_Location', 'Mobile', 'Category']], use_container_width=True)
            
            st.divider()
            st.subheader("📱 Direct WhatsApp Links (Top 10 Results)")
            
            for idx, row in filtered.head(10).iterrows():
                col1, col2, col3, col4 = st.columns([2, 2, 2, 2])
                col1.write(f"**{row['Name']}**")
                col2.write(f"GP: {row['GP_Location']}")
                col3.write(f"📱 {row['Mobile']}")
                
                # 💬 BENGALI WHATSAPP TEMPLATE
                bengali_msg = (
                    f"প্রিয় {row['Name']},\n\n"
                    f"✨ ডিজিটাল সার্ভিসেস (CSC) - বিশেষ ঘোষণা ✨\n\n"
                    f"আপনাকে জানানো যাচ্ছে যে আমাদের কেন্দ্রে সমস্ত ধরণের সরকারি অনলাইন ফর্ম ফিলাপের কাজ খুব সহজে ও দ্রুততার সাথে করা হয়:\n\n"
                    f"🌾 কৃষি ও কিষাণ সেবা:\n"
                    f"* PM Kisan Samman Nidhi (নতুন আবেদন, e-KYC ও কিস্তির টাকা স্ট্যাটাস চেক)\n"
                    f"* বাংলা শস্য বীমা (Fasal Bima Claim & Registration)\n"
                    f"* সার ভর্তুকি / Fertilizer Subsidy আপডেট\n"
                    f"* অন্নপূর্ণা যোজনা ও রেশন কার্ড\n\n"
                    f"🆔 পরিচয়পত্র ও ভোটার সেবা:\n"
                    f"* পরিচয়পত্র ডাউনলোড ও ঠিকানা সংশোধন\n"
                    f"* ভোটার আইডি কার্ড (নতুন তৈরি ও ভুল সংশোধন)\n\n"
                    f"📍 ঠিকানা: ডিজিটাল সার্ভিসেস\n"
                    f"📞 যোগাযোগ / WhatsApp: 9126690243"
                )
                
                msg_encoded = urllib.parse.quote(bengali_msg)
                wa_url = f"https://wa.me/91{row['Mobile']}?text={msg_encoded}"
                col4.markdown(f"[💬 Send WhatsApp Message]({wa_url})", unsafe_allow_html=True)
                
        else:
            st.error("Database file missing!")