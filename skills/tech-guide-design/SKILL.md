---
name: tech-guide-design
description: >-
  מערכת עיצוב לארטיפקטים של הסבר בעברית RTL — מדריכים, תיעוד, סיכומים, דוחות סריקה, ניתוחים והשוואות — בעיצוב כהה, שקט ומותאם לקריאה בנייד. Use this skill whenever the deliverable is a standalone HTML explanation artifact the user will read, keep or share, including phrasings like "תבנה לי מדריך", "תעשה דף הסבר", "תסכם את זה למסמך", "תעשה מזה ארטיפקט", "דוח", "תיעוד", "מסמך אפיון", "README כדף". Trigger it also when you decide on your own initiative that an explanation earned an artifact instead of a chat answer. It covers non-technical explanations too, not only code and API docs. Do NOT use for marketing, sales or landing pages, use hebrew-landing-design instead. Do NOT use for the prose voice of an explanation, which is explanatory-writing — that skill decides how the sentences sound, this one decides how the page looks, and they are meant to run together. Do NOT use for DOCX or PDF deliverables, use hebrew-documents.
license: MIT
compatibility: אינו דורש רשת. מיועד לארטיפקטים ב-claude.ai, כולל קריאה מהנייד.
---

# מערכת עיצוב לארטיפקטים של הסבר

## למה הסקיל הזה קיים

ארטיפקט הסבר הוא מסמך שנפתח פעם אחת, נקרא ברצף, ולפעמים נשמר או נשלח הלאה. הוא לא אפליקציה ולא דף שיווקי, ולכן כל מה שנועד למשוך תשומת לב — גרדיאנטים, זוהר, כותרת ענק, אמוג'י בכל כותרת — עובד נגדו. הקורא כבר החליט לקרוא; התפקיד של העיצוב הוא רק לא להפריע לו, ולעזור לו למצוא את החלק שהוא מחפש כשהוא חוזר למסמך שבוע אחר כך.

הגרסה הקודמת של הסקיל הזה עיצבה מסמכים כמו דפי נחיתה: באנר בגובה 60 פיקסלים עם גרדיאנט כחול, `box-shadow` זוהר סביב כל סקשן, רוחב של 1200 פיקסלים, ואמוג'י מובנה בכל `h2`. זה נראה מרשים בצילום מסך ומעייף בקריאה אמיתית, ובנייד — שזה מסך הקריאה בפועל — הרוחב הרחב והפדינג הגדול פשוט מבזבזים את המקום. הגרסה הזו מחליפה את זה בעיצוב שטוח ושקט: רקע כהה אחיד, גבולות דקים במקום צללים, צבע הדגשה אחד, ורוחב עמודה שנועד לשורת טקסט נוחה ולא למסך רחב.

השינוי השני הוא בהיקף. השם `tech-guide-design` נשאר מטעמי תאימות, אבל התחום הוא כל ארטיפקט הסבר: סיכום שבועי, ניתוח החלטה, השוואה בין שתי גישות, מסמך אפיון, דוח סריקה. הימצאות קוד במסמך היא מקרה פרטי, לא תנאי כניסה.

## מתי בכלל בונים ארטיפקט הסבר

זה היה חסר עד היום, וזו הסיבה שהסקיל לא נטען כשהיה צריך. הכלל הפשוט: **בקשה מפורשת תמיד גוברת** — אם המשתמש ביקש מסמך, מדריך, דף או ארטיפקט, בונים, בלי לשקול מחדש. מעבר לזה, בנה ארטיפקט מיוזמתך כשמתקיימים לפחות שניים מהתנאים הבאים.

התשובה ארוכה משלוש-ארבע פסקאות ויש לה מבנה פנימי — כמה נושאים נפרדים שהקורא ירצה לדלג ביניהם, ולא רצף אחד. תוכן צ'אט ארוך נקרא כמפולת; אותו תוכן בכרטיסים ממוספרים נקרא כמסמך.

התוכן נועד לחיות אחרי השיחה. אם הוא ייקרא שוב, יישלח למישהו, או ישמש כהתייחסות בעוד חודש — הוא צריך צורה עצמאית. אם הוא נצרך פעם אחת ונשכח, צ'אט זה בדיוק הכלי הנכון.

יש בו טבלאות, השוואות, בלוקי קוד או פריטים חוזרים במבנה זהה. אלה בדיוק הדברים שמתפרקים בפורמט צ'אט ומתיישרים בעיצוב.

**אל תבנה ארטיפקט** כשהתשובה היא עובדה, החלטה או פסקה — ארטיפקט לשורה אחת הוא טקס מיותר שדורש הקשה נוספת כדי לקרוא. אל תבנה גם כשהתוכן עדיין בדיון ועומד להשתנות בהודעה הבאה; ארטיפקט מקבע ומייקר כל תיקון. ואל תבנה כשהמשתמש שיתף משהו רגשי או שאל שאלה קצרה — שם מסמך מעוצב הוא בדיוק התגובה הלא נכונה.

הערה על יעד השמירה: הסקיל הזה מייצר HTML לקריאה. אם הפלט אמור להישמר כמסמך מקור לעריכה מאוחרת, המקום שלו הוא Markdown-docs או CodeKeeper לפי הכללים הקבועים, ואז כותבים Markdown ולא HTML.

## שבעת העקרונות שקובעים איך זה נראה

**רקע שטוח, בלי גרדיאנטים.** הרקע הוא `#0d1117` אחיד, וכל שכבה מעליו נבדלת בגוון בלבד: פאנל `#161b22`, פאנל פנימי `#1c2430`. גרדיאנט ברקע של מסמך ארוך יוצר תחושת "עמוד נחיתה" ומקשה על העין לזהות איפה נגמר בלוק ומתחיל הבא.

**גבולות במקום צללים.** ההפרדה בין רכיבים נעשית עם `1px solid #2a323d`. אין `box-shadow` בשום מקום. צל בעיצוב כהה כמעט לא נראה ורק מוסיף עכירות סביב הקצוות.

**צבע הדגשה אחד.** `#7aa2f7` הוא הצבע היחיד שנושא משמעות: קישורים, ערכי מפתח, פס ההדגשה בקאלאאוט. ירוק `#a6e3a1` וכתום `#f0b37e` שמורים לתגיות סטטוס בלבד — "חדש" מול "עדכון". ברגע שיש ארבעה צבעים פעילים, אף אחד מהם כבר לא מסמן כלום.

**היררכיה בגודל, לא בקישוט.** `h1` הוא `1.55rem` ו-`h2` הוא `1.12rem` — פער קטן בכוונה. הכותרות מסומנות בעמדה שלהן במבנה (כותרת של כרטיס), לא בגודל דרמטי, לא בקו תחתון עבה ולא באמוג'י צמוד.

**רוחב עמודה 820 פיקסלים.** זה הרוחב שנותן שורה נוחה לקריאה. 1200 פיקסלים מייצרים שורות ארוכות שהעין מאבדת בהן את תחילת השורה הבאה — בעברית זה מורגש אפילו יותר.

**מובייל הוא ברירת המחדל, לא breakpoint.** הפדינג `22px 16px 60px`, גופן `16px`, ו-`line-height: 1.75` נכונים כבר במסך צר. אין `@media` שמתקן דברים אחר כך, כי אין מה לתקן. אם רכיב דורש media query כדי להיות קריא בנייד — הרכיב שגוי.

**אמוג'י בכותרות, לא.** מספור (`1.`, `2.`) עושה את אותה עבודה של סימון והפרדה, ונשאר קריא כשמעתיקים את הטקסט לכל מקום אחר.

## טוקנים ובסיס

```css
:root{
  --bg:#0d1117; --panel:#161b22; --panel2:#1c2430; --line:#2a323d;
  --tx:#e6edf3; --muted:#9aa7b4; --accent:#7aa2f7; --accent2:#a6e3a1; --warn:#f0b37e;
  --danger:#f7768e;
}
*{box-sizing:border-box}
body{margin:0;background:var(--bg);color:var(--tx);
  font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Noto Sans Hebrew","Heebo",Arial,sans-serif;
  line-height:1.75;font-size:16px;-webkit-text-size-adjust:100%}
.wrap{max-width:820px;margin:0 auto;padding:22px 16px 60px}
```

`--danger` הוא תוספת ולא מופיע בקובץ המקור. השתמש בו רק לשגיאה או לאזהרה אמיתית, ולא כצבע רביעי לגיוון.

## הרכיבים

### כותרת עליונה, פילים ופסקת פתיחה

הכותרת מופרדת בקו תחתון דק בלבד. מתחתיה שורת "פילים" — כמוסות קטנות עם מטא-דאטה של המסמך (תאריך, טווח, כמות פריטים), שבהן הערך בצבע ההדגשה והתווית בצבע מושתק. אחריהן פסקת lede קצרה בצבע מושתק שאומרת מה יש במסמך ומה השורה התחתונה שלו. הצירוף הזה נותן לקורא את כל ההקשר בלי לגלול.

```css
header{border-bottom:1px solid var(--line);padding-bottom:18px;margin-bottom:26px}
h1{font-size:1.55rem;margin:0 0 10px;letter-spacing:-.01em}
.meta{display:flex;flex-wrap:wrap;gap:8px;margin-top:12px}
.pill{background:var(--panel);border:1px solid var(--line);border-radius:999px;
  padding:5px 13px;font-size:.83rem;color:var(--muted)}
.pill b{color:var(--accent);font-weight:600}
.lede{color:var(--muted);font-size:.95rem;margin:14px 0 0}
```

### כרטיס — יחידת התוכן הבסיסית

כל נושא יושב בכרטיס משלו. זו היחידה שמחליפה את ה-`section` הכבד של הגרסה הקודמת: פאנל, גבול דק, פינות `14px`, ורווח `16px` בלבד בין כרטיסים. הרווח הקטן מכוון — הכרטיסים אמורים להיקרא כרשימה רציפה, לא כעמודים נפרדים.

```css
.card{background:var(--panel);border:1px solid var(--line);border-radius:14px;
  padding:20px 18px;margin-bottom:16px}
.card h2{font-size:1.12rem;margin:0 0 4px;color:var(--tx)}
.card p{margin:0 0 12px}
```

### תגיות

שורת תגיות מתחת לכותרת הכרטיס, לסיווג מהיר: סוג, רישיון, תאריך, סטטוס. הווריאנטים הצבעוניים משנים רק את צבע הטקסט והגבול, לא את הרקע — תגית עם רקע מלא צועקת חזק מדי בתוך פסקה.

```css
.tags{display:flex;flex-wrap:wrap;gap:6px;margin:10px 0 14px}
.tag{font-size:.74rem;background:var(--panel2);border:1px solid var(--line);
  border-radius:6px;padding:3px 9px;color:var(--muted)}
.tag.new{color:var(--accent2);border-color:#2d4a35}
.tag.upd{color:var(--warn);border-color:#4a3a2a}
```

### קאלאאוט — הרכיב הכי חשוב במערכת

זה מה שהחליף את ארבעת סוגי ה-alert הצבעוניים. במקום ארבעה סוגים לפי חומרה, יש רכיב אחד לפי תפקיד: הפסקה שמחברת את התוכן הכללי למקרה הספציפי של הקורא. פס ההדגשה משתמש ב-`border-inline-start`, שמתהפך נכון לבד ב-RTL — `border-right` היה נשבר במסמך אנגלי.

```css
.why{background:var(--panel2);border-inline-start:3px solid var(--accent);
  border-radius:0 8px 8px 0;padding:11px 14px;font-size:.93rem;color:#cdd7e1;margin:0 0 12px}
.why b{color:var(--accent);font-weight:600}
```

הכותרת המודגשת בתחילתו היא מה שנותן לו את התפקיד. נסח אותה כשאלה שהקורא באמת שואל — "איך זה משתלב אצלך", "מה לעשות עם זה", "למה זה חשוב כאן" — ולא כתווית גנרית כמו "הערה" או "טיפ".

### קוד

בלוקי קוד תמיד `direction:ltr` ו-`text-align:left`, אחרת סימני פיסוק וסוגריים קופצים לצד הלא נכון. הקוד ה-inline דורש טיפול נוסף שקל לפספס: `unicode-bidi:embed` יחד עם `display:inline-block` הם מה שמונע מנתיב או שם פונקציה באנגלית להתפרק באמצע משפט עברי.

```css
code{background:#0b0f14;border:1px solid var(--line);border-radius:6px;
  padding:2px 7px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
  font-size:.85rem;color:var(--accent2);direction:ltr;display:inline-block;
  unicode-bidi:embed;max-width:100%;overflow-x:auto;vertical-align:middle}
pre{background:#0b0f14;border:1px solid var(--line);border-radius:8px;padding:12px 14px;
  overflow-x:auto;direction:ltr;text-align:left;margin:0 0 12px}
pre code{border:0;padding:0;background:none;display:block;white-space:pre}
```

אל תוסיף צביעת תחביר ידנית עם `span` צבעוניים. בגרסה הקודמת זו הייתה המלצה, והיא מכפילה את נפח ה-HTML, שוברת העתקה של הקוד, ומוסיפה חמישה צבעים למסמך שהעיקרון שלו הוא צבע אחד.

### קישורים ושורת מקורות

קישור מסומן בקו תחתון דק בגוון עמום שמתבהר ב-hover, ולא בקו תחתון סטנדרטי. שורת המקורות בתחתית כרטיס היא טקסט קטן ומושתק עם `word-break:break-all`, שמונע מכתובת ארוכה לפרוץ את רוחב הכרטיס בנייד.

```css
a{color:var(--accent);text-decoration:none;border-bottom:1px solid #2f4670}
a:hover{border-bottom-color:var(--accent)}
.src{font-size:.85rem;color:var(--muted)}
.src a{word-break:break-all}
```

### תיבת הערה וכותרת תחתונה

התיבה המקווקוות היא לתוכן מסדר שני: מה לא נכנס ולמה, סייגים, מגבלות אמינות. הגבול המקווקו אומר לקורא שזה לא חלק מהרצף הראשי בלי להוסיף עוד צבע.

```css
.note{background:var(--panel);border:1px dashed var(--line);border-radius:12px;
  padding:16px 18px;color:var(--muted);font-size:.9rem;margin-top:26px}
.note h3{color:var(--tx);font-size:1rem;margin:0 0 8px}
footer{margin-top:30px;padding-top:16px;border-top:1px solid var(--line);
  color:var(--muted);font-size:.82rem}
```

### טבלאות ורשימות

הקובץ המקורי לא כלל טבלה, וזו הגזירה שלה לפלטה: בלי רקע צבעוני בשורת הכותרת, הפרדה בקווים בלבד, ועטיפה ב-`div` עם גלילה אופקית כי טבלה בעלת שלוש עמודות ומעלה תמיד תחרוג במסך צר.

```css
.table-wrap{overflow-x:auto;margin:0 0 12px}
table{width:100%;border-collapse:collapse;font-size:.92rem}
th,td{padding:9px 12px;text-align:start;border-bottom:1px solid var(--line);vertical-align:top}
th{color:var(--muted);font-weight:600;font-size:.83rem;border-bottom:1px solid #3a4552}
ul,ol{margin:0 0 12px;padding-inline-start:20px}
li{margin-bottom:5px}
```

## שלד המסמך

```html
<!doctype html>
<html lang="he" dir="rtl">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>...</title>
<style>/* tokens + components */</style>
</head>
<body>
<div class="wrap">
  <header>
    <h1>...</h1>
    <div class="meta">
      <span class="pill">label: <b>value</b></span>
    </div>
    <p class="lede">...</p>
  </header>

  <div class="card">
    <h2>1. ...</h2>
    <div class="tags"><span class="tag new">...</span><span class="tag">...</span></div>
    <p>...</p>
    <div class="why"><b>...</b> ...</div>
    <pre><code>...</code></pre>
    <p class="src">...</p>
  </div>

  <div class="note">
    <h3>...</h3>
    <p>...</p>
  </div>

  <footer>...</footer>
</div>
</body>
</html>
```

שים לב ש-`dir="rtl"` יושב על `html` ולא על `body`, ושה-CSS כולו inline בתוך `style` יחיד — ארטיפקט חייב להיות קובץ אחד עצמאי.

## אנטי-דפוסים

אלה הדברים שהופיעו בגרסה הקודמת של הסקיל ואינם חוזרים. כשאתה מוצא את עצמך כותב אחד מהם, זה סימן שגלשת חזרה לעיצוב של דף שיווקי.

באנר כותרת עם גרדיאנט, פדינג של 60 פיקסלים ופינות עגולות בתחתית. `box-shadow` בכל צורה שהיא, ובמיוחד צל צבעוני זוהר. אמוג'י מובנה בכותרות `h2`. תגיות ותוויות עם רקע צבעוני מלא וטקסט לבן. `max-width` של 1200 פיקסלים. ארבעה סוגי alert צבעוניים לפי חומרה. צביעת תחביר ידנית ב-`span`. קו תחתון של שלושה פיקסלים מתחת לכותרות. `transition` ואנימציות — במסמך קריאה הן רק מסיחות.

ודבר אחרון שאינו ויזואלי: אל תמלא רכיב רק כי הוא קיים במערכת. מסמך בלי מקורות לא צריך `.src`, ומסמך שאין בו סייגים לא צריך `.note` עם משפט ממולא בכוח.

## מתי לא להשתמש בסקיל הזה

בדף נחיתה, דף מכירה או כל עמוד שנועד לשכנע — שם המקום של `hebrew-landing-design`, וההנחיות כאן יעבדו נגדך. באפליקציה או בכלי אינטראקטיבי עם מצב ולוגיקה, שם הצורה נגזרת מהאינטראקציה ולא ממסמך. במסמך שמיועד להדפסה, כי כל המערכת הזו כהה. וכשמה שנדרש הוא סגנון הכתיבה ולא הצורה — הניסוח של ההסבר עצמו הוא `explanatory-writing`, והשניים אמורים לרוץ יחד: הוא כותב את המשפטים, זה מעצב את הדף.
