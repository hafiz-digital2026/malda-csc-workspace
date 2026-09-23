import pandas as pd
import pywhatkit as kit
import time
import os
import random

# --- CONFIGURATION SETTINGS ---
EXCEL_PATH = r"C:\csc_Hafizcomputerlink\COMPLETE_70K_DATABASE.csv"
LOG_FILE = r"C:\csc_Hafizcomputerlink\sent_log.txt"
LOG_FILE = "sent_log.txt"                 # Kinko message gaya uski history
DAILY_LIMIT = 19                          # Har din kitne logo ko bhejna hai

# --- 1. LOG FILE LOAD KAREIN (HISTORY CHECK) ---
sent_numbers = set()
if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        sent_numbers = set(line.strip() for line in f if line.strip())

print(f"📋 Pehle se bheje gaye total contacts: {len(sent_numbers)}")


# --- 2. DATA LOAD KAREIN ---
if EXCEL_PATH.endswith(".csv"):
    df = pd.read_csv(EXCEL_PATH)
else:
    df = pd.read_excel(EXCEL_PATH)

# Clean Mobile numbers
df['Mobile'] = df['Mobile'].astype(str).str.replace(r'\D', '', regex=True)

# --- 3. JINHE MESSAGE NAHI GAYA UNHE FILTER KAREIN ---
pending_df = df[~df['Mobile'].isin(sent_numbers)]

print(f"📊 Baki bache total contacts: {len(pending_df)}")

if pending_df.empty:
    print("✅ Sabhi logon ko message bheja ja chuka hai!")
    exit()

# Aaj ke 19 logo ko select karein
today_batch = pending_df.head(DAILY_LIMIT)

print(f"🚀 Aaj total {len(today_batch)} logon ko message bheja jayega...\n")

# --- 4. AUTOMATIC SENDING LOOP ---
count = 0
for index, row in today_batch.iterrows():
    name = row['Name']
    mobile = row['Mobile']
    
    # 10 digit Indian number formatting (+91 add karna)
    if len(mobile) == 10:
        phone_no = f"+91{mobile}"
    elif len(mobile) == 12 and mobile.startswith("91"):
        phone_no = f"+{mobile}"
    else:
        print(f"⚠️ Invalid Mobile Number: {mobile}, skipping...")
        continue

    # Bengali Message Template
    bengali_msg = (
        f"প্রিয় {name},\n\n"
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

    try:
        count += 1
        print(f"[{count}/{len(today_batch)}] Bhej rahe hain: {name} ({phone_no})...")
        
        # PyWhatKit se Instant Message Bhejna
        # wait_time = 15 second tak Chrome khol kar wait karega, close_time = 3 second baad tab band hoga
        kit.sendwhatmsg_instantly(phone_no, bengali_msg, wait_time=15, tab_close=True, close_time=3)
        
        # History File (`sent_log.txt`) me Number Note karna
        with open(LOG_FILE, "a") as f:
            f.write(f"{mobile}\n")
            
        print(f"✅ Success: {name} ko message bhej diya aur log file me save kar diya.")
        
        # Safety Pause (25 se 35 seconds delay) taaki account safe rahe
        delay = random.randint(25, 35)
        print(f"⏳ Security Delay: Agle message ke liye {delay} seconds ruk rahe hain...\n")
        time.sleep(delay)
        
    except Exception as e:
        print(f"❌ Error {name} ko bhejne me: {e}\n")

print("🎉 Aaj ka 19 messages ka target pura ho gaya hai!")