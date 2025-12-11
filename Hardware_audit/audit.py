import csv
import logging
from datetime import datetime

# נסה לייבא את WMI. אם נכשל (למשל בלינוקס/מק), נרוץ במצב סימולציה  # Attempt WMI import; fallback to simulation on non-Windows
try:
    import wmi
    WMI_AVAILABLE = True
except ImportError:
    WMI_AVAILABLE = False

# --- Configuration ---  # הגדרות כלליות
LOG_FILE = "audit_log.log"
REPORT_FILE = "Upgrade_Required_Report.csv"

# הגדרות סף (Thresholds)  # ערכי מינימום לחומרה
MIN_RAM_GB = 8
MIN_DISK_FREE_GB = 20

# רשימת מחשבים לסריקה  # Computer list to audit
# בבית נבדוק את localhost. בעבודה אמיתית הרשימה תגיע מ-AD.  # At home use localhost; במציאות מהרשאות AD/CMDB
TARGET_COMPUTERS = ["localhost", "HR-PC-01", "FINANCE-SRV-02", "SALES-LAPTOP-05"]

# Setup Logging  # הגדרת לוג לקובץ
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def get_remote_info(computer_name):
    """
    מנסה להתחבר למחשב אמיתי. אם נכשל או המחשב פיקטיבי, מחזיר נתונים מדומים לדוח.
    Attempts real WMI query; if fails or host is dummy, returns simulated data.
    """
    if computer_name == "localhost" and WMI_AVAILABLE:
        try:
            c = wmi.WMI()
            os_info = c.Win32_OperatingSystem()[0]
            # המרה מ-KB ל-GB
            ram_gb = round(int(os_info.TotalVisibleMemorySize) / (1024 * 1024), 2)
            return ram_gb, "Online"
        except Exception as e:
            return 0, f"Error: {str(e)}"
    
    # --- SIMULATION FOR PORTFOLIO ---  # סימולציה עבור תיק עבודות
    # כאן אנחנו מדמים מה היה קורה ברשת אמיתית עבור מחשבים שאין לנו גישה אליהם בבית  # Mock results for unreachable lab hosts
    if computer_name == "HR-PC-01": return 4.0, "Online"  # מחשב ישן (יכנס לדוח)
    if computer_name == "FINANCE-SRV-02": return 16.0, "Online" # מחשב תקין
    if computer_name == "SALES-LAPTOP-05": return 6.0, "Online" # מחשב ישן (יכנס לדוח)
    
    return 0, "Unreachable"

def main():
    print(f"--- Starting Fleet Hardware Audit ---")
    print(f"Critiera: RAM < {MIN_RAM_GB}GB\n")
    
    outdated_machines = []

    for computer in TARGET_COMPUTERS:
        print(f"Scanning: {computer}...", end=" ")
        
        ram_gb, status = get_remote_info(computer)
        
        if status != "Online":
            print(f"[ERROR] {status}")
            logging.error(f"{computer}: Connection failed - {status}")
            continue

        # בדיקת תקינות  # Compliance check against threshold
        if ram_gb < MIN_RAM_GB:
            print(f"-> [ALERT] Outdated! Found only {ram_gb}GB RAM")
            logging.warning(f"{computer} is outdated. RAM: {ram_gb}GB")
            
            outdated_machines.append({
                "Computer Name": computer,
                "Issue": "Low RAM",
                "Current Value": f"{ram_gb}GB",
                "Required": f"{MIN_RAM_GB}GB"
            })
        else:
            print(f"-> [OK] ({ram_gb}GB)")
            logging.info(f"{computer} passed audit.")

    # ייצוא דוח  # Export report to CSV if יש מכונות שחורגות
    if outdated_machines:
        print(f"\n[SUMMARY] Found {len(outdated_machines)} machines requiring upgrade.")
        try:
            with open(REPORT_FILE, "w", newline="", encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["Computer Name", "Issue", "Current Value", "Required"])
                writer.writeheader()
                writer.writerows(outdated_machines)
            print(f"Report generated successfully: {REPORT_FILE}")
        except Exception as e:
            print(f"Failed to write report: {e}")
    else:
        print("\nAll machines meet the hardware requirements.")

if __name__ == "__main__":
    main()