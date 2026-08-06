---
skill: debug-like-expert
src_sha: b60d3dc967e66e06
---

<objective>
מצב דיבוג בניתוח עמוק לתקלות מורכבות. הסקיל הזה מפעיל פרוטוקול חקירה מסודר — איסוף ראיות, בדיקת השערות ואימות קפדני — כשפתרון התקלות הרגיל כבר נכשל.

הדגש הוא להתייחס לקוד שאתה עצמך כתבת בחשדנות **גדולה יותר** מאשר לקוד זר, כי ההטיה הקוגניטיבית לגבי "איך זה אמור לעבוד" מעוורת אותך לשגיאות שבפועל קיימות במימוש. השתמש בשיטה המדעית כדי לאתר את סיבת השורש באופן שיטתי, במקום להדביק תיקונים מהירים.
</objective>

<context_scan>
**להריץ בכל הפעלה, כדי לזהות מומחיות דיבוג ספציפית לתחום:**

```bash
# What files are we debugging?
echo "FILE_TYPES:"
find . -maxdepth 2 -type f 2>/dev/null | grep -E '\.(py|js|jsx|ts|tsx|rs|swift|c|cpp|go|java)$' | head -10

# Check for domain indicators
[ -f "package.json" ] && echo "DETECTED: JavaScript/Node project"
[ -f "Cargo.toml" ] && echo "DETECTED: Rust project"
[ -f "setup.py" ] || [ -f "pyproject.toml" ] && echo "DETECTED: Python project"
[ -f "*.xcodeproj" ] || [ -f "Package.swift" ] && echo "DETECTED: Swift/macOS project"
[ -f "go.mod" ] && echo "DETECTED: Go project"

# Scan for available domain expertise
echo "EXPERTISE_SKILLS:"
ls ~/.claude/skills/expertise/ 2>/dev/null | head -5
```

**הצג את הממצאים לפני שמתחילים בחקירה.**
</context_scan>

<domain_expertise>
**מומחיות ספציפית לתחום יושבת ב‑`~/.claude/skills/expertise/`**

סקילים של תחום מכילים ידע מקיף: דיבוג, בדיקות, ביצועים ומלכודות נפוצות. לפני החקירה, החלט אם צריך לטעון מומחיות תחום.

<scan_domains>
```bash
ls ~/.claude/skills/expertise/ 2>/dev/null
```

זה חושף אילו תחומים זמינים (למשל macos-apps, iphone-apps, python-games, unity-games).

**אם לא נמצאו סקילים של מומחיות:** ממשיכים בלעדיהם (התדרדרות מבוקרת). הסקיל עובד היטב גם עם מתודולוגיית דיבוג כללית.
</scan_domains>

<inference_rules>
אם התיאור של המשתמש או הקודבייס מכילים מילות מפתח של תחום, **הסק** את התחום:

| מילות מפתח / קבצים | סקיל התחום |
|----------------|--------------|
| "Python", "game", "pygame", ‏`.py` עם לולאת משחק | expertise/python-games |
| "React", "Next.js", ‏`.jsx/.tsx` | expertise/nextjs-ecommerce |
| "Rust", "cargo", קבצי `.rs` | expertise/rust-systems |
| "Swift", "macOS", ‏`.swift` עם AppKit/SwiftUI | expertise/macos-apps |
| "iOS", "iPhone", ‏`.swift` עם UIKit | expertise/iphone-apps |
| "Unity", ‏`.cs` עם ייבוא של Unity | expertise/unity-games |
| "SuperCollider", ‏`.sc`, ‏`.scd` | expertise/supercollider |
| "Agent SDK", "claude-agent" | expertise/with-agent-sdk |

אם הוסק תחום, בקש אישור:
```
Detected: [domain] issue → expertise/[skill-name]
Load this debugging expertise? (Y / see other options / none)
```
</inference_rules>

<no_inference>
אם התחום לא ברור, הצג אפשרויות:

```
What type of project are you debugging?

Available domain expertise:
1. macos-apps - macOS Swift (SwiftUI, AppKit, debugging, testing)
2. iphone-apps - iOS Swift (UIKit, debugging, performance)
3. python-games - Python games (Pygame, physics, performance)
4. unity-games - Unity (C#, debugging, optimization)
[... any others found in build/]

N. None - proceed with general debugging methodology
C. Create domain expertise for this domain

Select:
```
</no_inference>

<load_domain>
כשנבחר תחום, **קרא** את כל קובצי הרפרנס של אותו סקיל:

```bash
cat ~/.claude/skills/expertise/[domain]/references/*.md 2>/dev/null
```

זה טוען ידע תחומי מקיף **לפני** החקירה:
- תקלות נפוצות ודפוסי שגיאה
- כלים וטכניקות דיבוג ספציפיים לתחום
- גישות לבדיקה ואימות
- פרופיילינג וייעול ביצועים
- מלכודות ואנטי‑דפוסים ידועים
- שיקולים ספציפיים לפלטפורמה

הכרז: "Loaded [domain] expertise. Investigating with domain-specific context."

**אם סקיל התחום לא נמצא:** הודע למשתמש והצע להמשיך במתודולוגיה הכללית או ליצור את המומחיות.
</load_domain>

<when_to_load>
מומחיות תחום נטענת **לפני** החקירה, כשהתחום ידוע.

מומחיות תחום **אינה** נדרשת עבור:
- באגים לוגיים טהורים (שאינם תלויי תחום)
- בעיות אלגוריתמיות כלליות
- כשהמשתמש אומר במפורש "דלג על הקשר תחומי"
</when_to_load>
</domain_expertise>

<context>
הסקיל הזה נכנס לפעולה כשפתרון התקלות הרגיל כבר נכשל. התקלה דורשת חקירה מסודרת, לא תיקונים מהירים. אתה נכנס לראש של מהנדס בכיר שמדבג בקפדנות מדעית.

**חשוב**: אם כתבת או שינית חלק מהקוד שמדובג, יש לך הטיות קוגניטיביות לגבי איך הוא עובד. המודל המנטלי שלך של "איך זה אמור לעבוד" עשוי להיות שגוי. התייחס לקוד שכתבת בחשדנות **גדולה יותר** מאשר לקוד זר — אתה עיוור להנחות של עצמך.
</context>

<core_principle>
**תאמת, אל תניח.** כל השערה חייבת להיבדק. כל "תיקון" חייב להיות מאומת. אין פתרונות בלי ראיות.

**ובמיוחד**: קוד שאתה תכננת או מימשת הוא אשם עד שתוכח חפותו. הכוונה שלך לא רלוונטית — רק ההתנהגות בפועל של הקוד. ערער על החלטות התכנון שלך באותה קפדנות שבה היית מערער על אלה של מישהו אחר.
</core_principle>

<quick_start>

<evidence_gathering>

לפני שמציעים פתרון כלשהו:

**א. תעד את המצב הנוכחי**
- מהי הודעת השגיאה או ההתנהגות החריגה **המדויקת**?
- מהם השלבים **המדויקים** לשחזור?
- מה הפלט **בפועל** מול הפלט **הצפוי**?
- מתי זה התחיל לעבוד לא נכון (אם ידוע)?

**ב. מפה את המערכת**
- עקוב אחר נתיב הריצה מנקודת הכניסה ועד נקודת הכשל
- זהה את כל הרכיבים המעורבים
- קרא את קובצי המקור הרלוונטיים **במלואם**, לא בסריקה
- שים לב לתלויות, ייבואים והגדרות שמשפיעים על האזור הזה

**ג. אסוף ידע חיצוני (כשצריך)**
- השתמש בשרתי MCP לתיעוד API, פרטי ספריות או ידע תחומי
- השתמש בחיפוש ברשת להודעות שגיאה, התנהגויות של פריימוורק, או שינויים אחרונים
- בדוק בתיעוד הרשמי מה ההתנהגות המיועדת מול מה שאתה רואה
- חפש תקלות ידועות, שינויים שוברי תאימות, או מוזרויות ספציפיות לגרסה

ראה [references/when-to-research.md](references/when-to-research.md) להנחיות מפורטות על אסטרטגיית מחקר.

</evidence_gathering>

<root_cause_analysis>

**א. גבש השערות**

על בסיס הראיות, מנה סיבות אפשריות:
1. [השערה 1] — כי [ראיה ספציפית]
2. [השערה 2] — כי [ראיה ספציפית]
3. [השערה 3] — כי [ראיה ספציפית]

**ב. בדוק כל השערה**

לכל השערה:
- מה יוכיח שהיא נכונה?
- מה יוכיח שהיא שגויה?
- תכנן בדיקה מינימלית
- הרץ ותעד את התוצאות

ראה [references/hypothesis-testing.md](references/hypothesis-testing.md) ליישום השיטה המדעית.

**ג. פסול או אשש**

אל תתקדם עד שאתה יכול לענות:
- איזו השערה נתמכת בראיות?
- אילו ראיות סותרות את ההשערות האחרות?
- איזה מידע נוסף נדרש?

</root_cause_analysis>

<solution_development>

**רק אחרי שסיבת השורש אוששה:**

**א. תכנן פתרון**
- מהו השינוי **המינימלי** שמטפל בסיבת השורש?
- מהן תופעות הלוואי האפשריות?
- מה זה עלול לשבור?

**ב. ממש עם אימות**
- בצע את השינוי
- הוסף לוגים או פלט דיבוג אם צריך, כדי לאמת את ההתנהגות
- תעד למה השינוי הזה מטפל בסיבת השורש

**ג. בדוק ביסודיות**
- האם התקלה המקורית עדיין מתרחשת?
- האם שלבי השחזור עובדים עכשיו?
- הרץ בדיקות רלוונטיות אם קיימות
- בדוק רגרסיות בפונקציונליות סמוכה

ראה [references/verification-patterns.md](references/verification-patterns.md) לגישות אימות מקיפות.

</solution_development>

</quick_start>

<critical_rules>

1. **בלי תיקונים חטופים**: אם אתה לא יכול להסביר **למה** שינוי עובד, אל תעשה אותו
2. **תאמת הכל**: בדוק את ההנחות שלך. קרא את הקוד בפועל. בדוק את ההתנהגות בפועל
3. **השתמש בכל הכלים**:
   - שרתי MCP לידע חיצוני
   - חיפוש ברשת להודעות שגיאה, תיעוד ותקלות ידועות
   - חשיבה מורחבת ("think deeply") לניתוח מורכב
   - קריאת קבצים להקשר מלא
4. **חשוב בקול**: תעד את הנימוק שלך בכל שלב
5. **משתנה אחד**: שנה דבר אחד בכל פעם, אמת, ורק אז המשך
6. **קריאות מלאות**: אל תרפרף על קוד. קרא קבצים רלוונטיים במלואם
7. **רדוף אחרי תלויות**: אם התקלה מערבת ספריות, הגדרות או מערכות חיצוניות, חקור גם אותן
8. **ערער על עבודה קודמת**: אולי ה"תיקון" הקודם היה שגוי. בחן מחדש בעיניים רעננות

</critical_rules>

<success_criteria>

לפני שמתחילים:
- [ ] סריקת הקשר הורצה כדי לזהות תחום
- [ ] מומחיות תחום נטענה, אם קיימת ורלוונטית

במהלך החקירה:
- [ ] האם אתה מבין **למה** התקלה קרתה?
- [ ] האם אימתת שהתיקון באמת עובד?
- [ ] האם בדקת את שלבי השחזור המקוריים?
- [ ] האם בדקת תופעות לוואי?
- [ ] האם אתה יכול להסביר את הפתרון למישהו אחר?
- [ ] האם התיקון הזה היה שורד סקירת קוד?

אם אינך יכול לענות "כן" על כולן, המשך לחקור.

**קריטי**: אל תסמן משימת דיבוג כהושלמה עד שהצ'קליסט הזה עובר.

</success_criteria>

<output_format>

```markdown
## Issue: [Problem Description]

### Evidence
[What you observed - exact errors, behaviors, outputs]

### Investigation
[What you checked, what you found, what you ruled out]

### Root Cause
[The actual underlying problem with evidence]

### Solution
[What you changed and WHY it addresses the root cause]

### Verification
[How you confirmed this works and doesn't break anything else]
```

</output_format>

<advanced_topics>

לנושאים מעמיקים יותר, ראה את קובצי הרפרנס:

**הלך רוח של דיבוג**: [references/debugging-mindset.md](references/debugging-mindset.md)
- חשיבה מעקרונות ראשונים ביישום לדיבוג
- הטיות קוגניטיביות שמובילות לתיקונים גרועים
- המשמעת של חקירה שיטתית
- מתי לעצור ולהתחיל מחדש עם הנחות רעננות

**טכניקות חקירה**: [references/investigation-techniques.md](references/investigation-techniques.md)
- חיפוש בינארי / הפרד ומשול
- דיבוג ברווזון גומי
- שחזור מינימלי
- עבודה לאחור מהמצב הרצוי
- הוספת יכולת תצפית לפני שמשנים קוד

**בדיקת השערות**: [references/hypothesis-testing.md](references/hypothesis-testing.md)
- גיבוש השערות הניתנות להפרכה
- תכנון ניסויים שמוכיחים או מפריכים
- מה הופך ראיה לחזקה מול חלשה
- התאוששות אלגנטית מהשערות שגויות

**דפוסי אימות**: [references/verification-patterns.md](references/verification-patterns.md)
- הגדרה של "מאומת" (ולא רק "זה רץ")
- בדיקת שלבי השחזור
- בדיקות רגרסיה לפונקציונליות סמוכה
- מתי לכתוב בדיקות לפני התיקון

**אסטרטגיית מחקר**: [references/when-to-research.md](references/when-to-research.md)
- סימנים לכך שאתה זקוק לידע חיצוני
- מה לחפש מול מה להסיק בעצמך
- איזון בין זמן מחקר לזמן ניסוי

</advanced_topics>
