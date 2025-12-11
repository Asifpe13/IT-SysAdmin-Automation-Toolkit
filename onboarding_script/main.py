import csv
import os
import logging
from datetime import datetime

# --- Configuration ---  # הגדרות כלליות
# In a real environment, this would be a network path like r"\\FileServer\Users"  # בסביבה אמיתית זה היה נתיב רשת, כאן זה תיקייה מקומית לדוגמה
BASE_DIR = "company_data" 
LOG_FILE = "onboarding_log.log"
INPUT_FILE = "employees.csv"

# Setup Logging  # הגדרת מנגנון לוגים לקובץ
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def setup_user_environment(name, employee_id, department):
    """
    Creates a user folder and simulates permission assignment based on department.
    יוצרת תיקיית משתמש ומדמה הרשאות לפי מחלקה.
    """
    # Sanitize folder name (remove spaces, handle special chars)  # ניקוי שם תיקייה מרווחים/תווים מיוחדים
    safe_folder_name = f"{name.replace(' ', '_')}_{employee_id}"
    user_path = os.path.join(BASE_DIR, "users", safe_folder_name)
    
    print(f"\n[PROCESSING] User: {name} | Dept: {department}")

    try:
        # 1. Create User Directory  # יצירת תיקיית משתמש אם לא קיימת
        if not os.path.exists(user_path):
            os.makedirs(user_path)
            logging.info(f"Created directory: {user_path}")
            print(f"   [OK] Folder created at: {user_path}")
        else:
            logging.warning(f"Directory already exists: {user_path}")
            print(f"   [SKIP] Folder already exists.")

        # 2. Generate 'Welcome' File  # כתיבת קובץ Welcome אישי בתיקייה
        welcome_file = os.path.join(user_path, "welcome.txt")
        with open(welcome_file, "w", encoding='utf-8') as f:
            f.write(f"Hello {name},\n")
            f.write(f"Welcome to the {department} team!\n")
            f.write(f"Your Employee ID is: {employee_id}\n")
            f.write("Please adhere to company security policies.\n")
        
        logging.info(f"Generated welcome file for {name}")

        # 3. Simulate Permissions (ACLs) - The "Enterprise" Logic  # סימולציית פקודות הרשאות כמו בארגון
        # Instead of running real 'icacls' commands (which only work on Windows Server),  # במקום להריץ icacls אמיתי (שרת Windows)
        # we print the commands to simulate the automation.  # מדפיסים את הפקודות לצורך הדגמה בלבד
        
        permission_cmd = ""
        
        if department.lower() == "finance":
            # Finance gets specific restrictive access  # מחלקת כספים מקבלת גישה מצומצמת
            permission_cmd = f'icacls "{user_path}" /grant "Finance_Group":(OI)(CI)F'
        
        elif department.lower() == "devops" or department.lower() == "it":
            # DevOps gets Admin-like access  # DevOps/IT מקבלים הרשאות מלאות
            permission_cmd = f'icacls "{user_path}" /grant "DevOps_Admins":(OI)(CI)F /grant "{name}":F'
        
        else:
            # General employees just get access to their own folder  # שאר העובדים מקבלים גישה לתיקייה האישית בלבד
            permission_cmd = f'icacls "{user_path}" /grant "{name}":(OI)(CI)M'

        # Log and Print the simulated system command  # מתעדים ומדפיסים את הפקודה הסימולטיבית
        print(f"   [SYSTEM EXEC] {permission_cmd}")
        logging.info(f"Applied permissions: {department} policy")

    except Exception as e:
        error_msg = f"Failed to setup user {name}: {str(e)}"
        print(f"   [ERROR] {error_msg}")
        logging.error(error_msg)

def main():
    print("--- STARTING AUTOMATED ONBOARDING ---")
    
    # Check if CSV exists  # בדיקה שהקובץ הראשי של העובדים קיים
    if not os.path.exists(INPUT_FILE):
        print(f"[CRITICAL] Input file '{INPUT_FILE}' not found!")
        return

    try:
        with open(INPUT_FILE, mode='r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            
            for row in reader:
                # Clean up data (strip whitespace)  # ניקוי רווחים כדי למנוע תקלות בשם/מחלקה/ת"ז
                name = row['Name'].strip()
                emp_id = row['ID'].strip()
                dept = row['Department'].strip()
                
                setup_user_environment(name, emp_id, dept)
                
    except Exception as e:
        print(f"[CRITICAL ERROR] Failed to read CSV: {e}")

    print("\n--- ONBOARDING COMPLETE ---")
    print(f"Check '{LOG_FILE}' for full audit trail.")

if __name__ == "__main__":
    main()