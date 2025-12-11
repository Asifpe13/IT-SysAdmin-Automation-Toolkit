# IT-SysAdmin-Automation-Toolkit

מבנה הרפו: כל תיקייה היא סקריפט/אוטומציה נפרדת. כאן תמצא תיאור קצר לכל אחת.

## onboarding_script
- **מה הסקריפט עושה**: קורא `employees.csv`, יוצר תיקיית משתמש (`company_data/users/<Name_ID>`), כותב `welcome.txt` אישי, ומדמה פקודות הרשאות (`icacls`) לפי מחלקה. כותב לוג ב-`onboarding_log.log`.
- **איך להריץ**:
  1) ודא שקיים `onboarding_script/employees.csv` עם העמודות `Name,ID,Department`.
  2) בטרמינל מתוך שורש הרפו:
     ```
     python onboarding_script/main.py
     ```
  3) תוצרים: תיקיות וקבצי welcome תחת `onboarding_script/company_data/users/` ולוג מלא ב-`onboarding_script/onboarding_log.log`.
- **למה זה שימושי**: מדמה אוטומציה של קליטת עובדים (תיקיית בית, קובץ קבלת פנים, פקודות הרשאה) שניתן להתאים בקלות להרצה אמיתית ב-Windows Server.

## Hardware_audit
- **מה הסקריפט עושה**: סורק רשימת מחשבים (מדומה/מקומית), בודק RAM מול מינימום, כותב לוג ב-`Hardware_audit/audit_log.log`, ומפיק דוח חוסרים ב-`Hardware_audit/Upgrade_Required_Report.csv`.
- **תלויות**: מודול `wmi` (נדרש להרצה אמיתית ב-Windows). ללא WMI הסקריפט רץ במצב סימולציה.
- **איך להריץ**:
  1) אופציונלי: `pip install -r Hardware_audit/requirements.txt`
  2) בטרמינל מתוך שורש הרפו:
     ```
     python Hardware_audit/audit.py
     ```
  3) פלט: לוג ב-`Hardware_audit/audit_log.log`, ודוח מחשבים הדורשים שדרוג ב-`Hardware_audit/Upgrade_Required_Report.csv` (אם נמצאו).
- **למה זה שימושי**: מדגים אודיט ציוד עם תיעוד חריגות וייצוא דוח, וניתן להחליף רשימת מחשבים לרשימה אמיתית (AD/CMDB) ולחבר לפקודות הפצה.

## הוספת סקריפטים חדשים
- צור תיקייה נפרדת לכל סקריפט עם `README` מקומי קצר (מה הוא עושה, איך להריץ).
- שמור קלטים/פלטים (CSV, לוגים) בתוך התיקייה המקומית כדי לא להתערבב עם אחרים.