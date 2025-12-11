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

## הוספת סקריפטים חדשים
- צור תיקייה נפרדת לכל סקריפט עם `README` מקומי קצר (מה הוא עושה, איך להריץ).
- שמור קלטים/פלטים (CSV, לוגים) בתוך התיקייה המקומית כדי לא להתערבב עם אחרים.