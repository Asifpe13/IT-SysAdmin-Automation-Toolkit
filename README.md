# IT-SysAdmin-Automation-Toolkit

Repository layout: each folder is a separate script/automation.

## English (for recruiters/overview)

### onboarding_script (Employee Onboarding)
- What you get: per-user home folder, personalized `welcome.txt`, and simulated ACL commands per department; full log in `onboarding_log.log`.
- How it works: reads `employees.csv`, creates `company_data/users/<Name_ID>`, writes a welcome file, prints `icacls` commands by department.
- How to run:
  1) Ensure `onboarding_script/employees.csv` exists with columns Name, ID, Department.
  2) From repo root:
     ```
     python onboarding_script/main.py
     ```
  3) Outputs: folders + welcome.txt under `company_data/users/`, log in `onboarding_log.log`.
- Why it’s useful: ready-to-adapt onboarding automation that can become real Windows Server commands with minor tweaks.

### Hardware_audit (Hardware Audit)
- What you get: audit log in `Hardware_audit/audit_log.log` and an upgrade-needed report in `Upgrade_Required_Report.csv`.
- How it works: iterates over a (simulated/local) computer list, checks RAM against a minimum threshold, logs results, and writes outdated machines to CSV.
- Dependency: `wmi` for real Windows checks; without it, the script runs in simulation mode.
- How to run:
  1) Optional deps: `pip install -r Hardware_audit/requirements.txt`
  2) From repo root:
     ```
     python Hardware_audit/audit.py
     ```
  3) Outputs: `audit_log.log` and `Upgrade_Required_Report.csv` inside `Hardware_audit`.
- Why it’s useful: lightweight audit skeleton you can point at real AD/CMDB host lists and extend with deployment actions.

### uptime_monitor (Website Uptime Monitor)
- What you get: active monitoring of a demo URL (`https://www.instagram.com/`) with Telegram alerts on down/recovery; logs to `uptime_monitor/uptime.log`.
- How it works: polls the target every `CHECK_INTERVAL_SECONDS`, sends a Telegram alert on first DOWN and on recovery.
- How to run:
  1) Set env vars (or a local `.env` file) for `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, optionally `TARGET_URL`, `CHECK_INTERVAL_SECONDS`.
  2) From repo root:
     ```
     python uptime_monitor/monitor.py
     ```
  3) Outputs: log at `uptime_monitor/uptime.log`, Telegram messages for incidents.
- Why it’s useful: minimal active monitor template you can point at any internal service; swap the URL and bot/channel as needed.

### Adding new scripts
- Create a dedicated folder per script with a local README (purpose + run steps).
- Keep inputs/outputs (CSV, logs) inside that folder to avoid mixing.

## עברית (להסבר מפורט)

### onboarding_script (קליטת עובדים)
- מה מקבלים: תיקיית בית לכל עובד, קובץ welcome.txt אישי ופקודות הרשאה מדומות לפי מחלקה, עם לוג מלא ב-`onboarding_log.log`.
- איך זה עובד: קורא את `employees.csv`, יוצר תיקיות תחת `company_data/users/<Name_ID>`, כותב קובץ ברכה ומדפיס icacls לפי המחלקה.
- איך להריץ:
  1) לוודא שהקובץ `onboarding_script/employees.csv` קיים עם העמודות Name, ID, Department.
  2) מהשורש של הרפו להריץ:
     ```
     python onboarding_script/main.py
     ```
  3) אחרי הריצה: תיקיות + welcome.txt ב-`company_data/users/`, ולוג ב-`onboarding_log.log`.
- למה זה טוב: בסיס מוכן לאוטומציית אונבורדינג שאפשר להפוך לפקודות ייצור ב-Windows Server עם התאמות מינימליות.

### Hardware_audit (אודיט ציוד)
- מה מקבלים: לוג אודיט ב-`Hardware_audit/audit_log.log` ודוח מחשבים שדורשים שדרוג RAM ב-`Upgrade_Required_Report.csv`.
- איך זה עובד: עובר על רשימת מחשבים (סימולציה/מקומי), בודק RAM מול סף מינימלי, מתעד בלוג ומוסיף חורגים לדוח CSV.
- תלות: מודול `wmi` לבדיקה אמיתית ב-Windows; בלי WMI הסקריפט רץ במצב סימולציה.
- איך להריץ:
  1) אופציונלי: `pip install -r Hardware_audit/requirements.txt`
  2) מהשורש של הרפו:
     ```
     python Hardware_audit/audit.py
     ```
  3) פלט: `audit_log.log` ו-`Upgrade_Required_Report.csv` בתיקיית `Hardware_audit`.
- למה זה טוב: שלד קצר לאודיט ציוד שאפשר לחבר לרשימת AD/CMDB אמיתית ולהרחיב לפעולות הפצה.

### uptime_monitor (ניטור זמינות אתר)
- מה מקבלים: ניטור פעיל ל-`https://www.instagram.com/` (דמו) עם התראות טלגרם על נפילה/חזרה; לוג ב-`uptime_monitor/uptime.log`.
- איך זה עובד: שולח בדיקה כל `CHECK_INTERVAL_SECONDS`; בהתראה ראשונה על נפילה ובחזרה לעבודה שולח הודעה.
- איך להריץ:
  1) להגדיר משתני סביבה (או `.env` מקומי) עבור `TELEGRAM_BOT_TOKEN`, `TELEGRAM_CHAT_ID`, ואופציונלית `TARGET_URL`, `CHECK_INTERVAL_SECONDS`.
  2) מהשורש של הרפו:
     ```
     python uptime_monitor/monitor.py
     ```
  3) פלט: לוג ב-`uptime_monitor/uptime.log`, הודעות בטלגרם על אירועים.
- למה זה טוב: תבנית קלה לניטור שירותים (חיצוניים או פנימיים) עם ערוץ התראות גמיש; רק להחליף URL ובוט.

### הוספת סקריפטים חדשים
- צור תיקייה נפרדת לכל סקריפט עם README מקומי (מטרה ושלבי הרצה).
- שמור קלטים/פלטים בתוך התיקייה המקומית כדי לא להתערבב.