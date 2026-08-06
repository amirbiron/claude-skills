---
skill: tech-guide-design
src_sha: 3487e929f517b823
---

# מערכת עיצוב למדריכים טכניים

מערכת עיצוב מקיפה ליצירת מדריכים טכניים ותיעוד עם אסתטיקה מודרנית כהה.

## לוח צבעים

### צבעים ראשיים
- **Primary**: `#0088cc` — כותרות H2, קישורים, כפתורים ראשיים
- **Secondary**: `#2ecc71` — כותרות H3, הודעות הצלחה
- **Warning**: `#f39c12` — כותרות H4, אזהרות
- **Danger**: `#e74c3c` — שגיאות קריטיות, התראות חמורות
- **Purple**: `#9b59b6` — אנומליות, סטטוס מיוחד

### צבעי רקע
- **רקע העמוד**: `linear-gradient(135deg, #1a1a2e 0%, #0f0f23 100%)`
- **רקע כרטיס / סקציה**: `#16213e`
- **רקע קוד**: `#0f0f23` (כהה יותר)
- **צבע גבול**: `#3d5a80`

### צבעי טקסט
- **טקסט ראשי**: `#eee` (לבן‑שבור)
- **טקסט משני**: אטימות 0.8–0.9
- **טקסט קוד**: `#7fdbca` (קוד בתוך שורה)
- **טקסט בבלוק קוד**: `#c3cee3`

### הדגשת תחביר

```css
.comment { color: #6a9955; }     /* ירוק זית */
.keyword { color: #c586c0; }     /* סגול */
.string { color: #ce9178; }      /* כתום */
.function { color: #dcdcaa; }    /* צהוב */
.variable { color: #9cdcfe; }    /* כחול בהיר */
.number { color: #b5cea8; }      /* ירוק בהיר */
.operator { color: #d4d4d4; }    /* אפור בהיר */
```

## תבנית משתני CSS

תמיד מתחילים במשתני CSS בתוך `:root`:

```css
:root {
    --primary-color: #0088cc;
    --secondary-color: #2ecc71;
    --warning-color: #f39c12;
    --danger-color: #e74c3c;
    --dark-bg: #1a1a2e;
    --card-bg: #16213e;
    --text-color: #eee;
    --code-bg: #0f0f23;
    --border-color: #3d5a80;
}
```

## מבנה הפריסה

### פריסה כללית
- **כיוון**: `dir="rtl"` (עברית)
- **רוחב מכולה**: `max-width: 1200px` ממורכז
- **משפחת גופנים**: 'Segoe UI', Tahoma, Arial, sans-serif
- **גובה שורה**: `1.8` (קריאות מיטבית)
- **מרווחים**: `40px` בין סקציות, `20px` בין אלמנטים

### עיצוב ה‑body

```css
body {
    font-family: 'Segoe UI', Tahoma, Arial, sans-serif;
    background: linear-gradient(135deg, var(--dark-bg) 0%, #0f0f23 100%);
    color: var(--text-color);
    line-height: 1.8;
    min-height: 100vh;
}
```

## רכיב הכותרת העליונה

### עיצוב
- **ריפוד**: `60px 20px`
- **רקע**: `linear-gradient(135deg, #0088cc 0%, #005577 100%)`
- **עיגול פינות**: `0 0 30px 30px` (פינות עגולות רק בתחתית)
- **צל**: `0 10px 40px rgba(0, 136, 204, 0.3)`

### טיפוגרפיה
- **H1**: `2.8em` עם `text-shadow: 2px 2px 4px rgba(0,0,0,0.3)`
- **כותרת משנה**: `1.3em` עם `opacity: 0.9`

### דוגמה

```css
header {
    text-align: center;
    padding: 60px 20px;
    background: linear-gradient(135deg, var(--primary-color) 0%, #005577 100%);
    margin-bottom: 40px;
    border-radius: 0 0 30px 30px;
    box-shadow: 0 10px 40px rgba(0, 136, 204, 0.3);
}
```

## רכיבי סקציה וכרטיס

### סקציה סטנדרטית
- **רקע**: `#16213e`
- **גבול**: `1px solid #3d5a80`
- **עיגול פינות**: `15px`
- **ריפוד**: `35px`
- **מרווח תחתון**: `30px`
- **צל**: `0 5px 25px rgba(0,0,0,0.3)`

### דוגמה

```css
section {
    background: var(--card-bg);
    border-radius: 15px;
    padding: 35px;
    margin-bottom: 30px;
    border: 1px solid var(--border-color);
    box-shadow: 0 5px 25px rgba(0,0,0,0.3);
}
```

## היררכיה טיפוגרפית

### H2 (כותרות ראשיות)

```css
h2 {
    color: var(--primary-color);
    font-size: 1.8em;
    margin-bottom: 25px;
    padding-bottom: 15px;
    border-bottom: 3px solid var(--primary-color);
    display: flex;
    align-items: center;
    gap: 15px;
}
```

- גודל אייקון: `1.2em`
- גבול תחתון: `3px solid`

### H3 (כותרות משניות)

```css
h3 {
    color: var(--secondary-color);
    font-size: 1.3em;
    margin: 25px 0 15px 0;
}
```

### H4 (כותרות שלישוניות)

```css
h4 {
    color: var(--warning-color);
    margin: 20px 0 10px 0;
}
```

## רכיבי קוד

### קוד בתוך שורה

```css
code {
    background: var(--code-bg);
    padding: 3px 8px;
    border-radius: 5px;
    font-family: 'Consolas', 'Monaco', monospace;
    font-size: 0.9em;
    color: #7fdbca;
}
```

### בלוקי קוד

```css
pre {
    background: var(--code-bg);
    padding: 20px;
    border-radius: 10px;
    overflow-x: auto;
    margin: 20px 0;
    border: 1px solid var(--border-color);
    direction: ltr;
    text-align: left;
}

pre code {
    padding: 0;
    background: none;
    color: #c3cee3;
    line-height: 1.6;
}
```

**חשוב**: לבלוקי קוד תמיד יש `direction: ltr` ו‑`text-align: left`.

## רכיבי טבלה

### מבנה

```css
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    background: var(--code-bg);
    border-radius: 10px;
    overflow: hidden;
}

th, td {
    padding: 15px;
    text-align: right;
    border-bottom: 1px solid var(--border-color);
}

th {
    background: var(--primary-color);
    color: white;
    font-weight: 600;
}

tr:hover {
    background: rgba(0, 136, 204, 0.1);
}
```

## תיבות התראה

### מבנה
- **פריסה**: Flexbox עם `gap: 15px`
- **ריפוד**: `20px`
- **עיגול פינות**: `10px`
- **גבול ימני**: `4px solid` (צבע לפי סוג)
- **אייקון**: אימוג'י בגודל `1.5em`–`2em`

### סוגי התראות

#### התראת מידע

```css
.alert-info {
    background: rgba(0, 136, 204, 0.15);
    border-right: 4px solid var(--primary-color);
}
/* אייקון: 💡 או ℹ️ */
```

#### התראת הצלחה

```css
.alert-success {
    background: rgba(46, 204, 113, 0.15);
    border-right: 4px solid var(--secondary-color);
}
/* אייקון: ✅ */
```

#### התראת אזהרה

```css
.alert-warning {
    background: rgba(243, 156, 18, 0.15);
    border-right: 4px solid var(--warning-color);
}
/* אייקון: ⚠️ */
```

#### התראת סכנה

```css
.alert-danger {
    background: rgba(231, 76, 60, 0.15);
    border-right: 4px solid var(--danger-color);
}
/* אייקון: ❌ */
```

### דוגמת HTML

```html
<div class="alert-box alert-info">
    <span style="font-size: 1.5em;">💡</span>
    <div>
        <strong>טיפ:</strong> תוכן ההתראה כאן
    </div>
</div>
```

## רכיבי תגית

### עיצוב

```css
.badge {
    display: inline-block;
    padding: 5px 15px;
    border-radius: 20px;
    font-size: 0.85em;
    font-weight: bold;
    color: white;
    margin: 5px 5px 5px 0;
}

.badge-primary { background: #0088cc; }
.badge-success { background: #2ecc71; }
.badge-warning { background: #f39c12; }
.badge-danger { background: #e74c3c; }
.badge-purple { background: #9b59b6; }
```

**מאפיינים מרכזיים**:
- צורת גלולה (pill shape)
- צבע רקע מלא (לא שקוף)
- טקסט לבן תמיד

## מערכת גריד

### פריסת CSS Grid

```css
.grid-2 {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
    margin: 20px 0;
}
```

### כרטיסי תכונה (בתוך הגריד)

```css
.feature-card {
    background: var(--code-bg);
    padding: 25px;
    border-radius: 10px;
    border: 1px solid var(--border-color);
}
```

## רכיבים מיוחדים

### תרשימי ארכיטקטורה

```css
.architecture-diagram {
    background: var(--code-bg);
    padding: 30px;
    border-radius: 15px;
    margin: 25px 0;
    direction: ltr;
    text-align: center;
    font-family: monospace;
    font-size: 0.95em;
    line-height: 1.4;
    overflow-x: auto;
    white-space: pre;
}
```

### עץ קבצים

```css
.file-tree {
    background: var(--code-bg);
    padding: 20px;
    border-radius: 10px;
    font-family: monospace;
    direction: ltr;
    text-align: left;
}

.file-tree .folder { color: #f39c12; }
.file-tree .file { color: #3498db; }
```

### תוכן עניינים

```css
.toc {
    background: var(--code-bg);
    padding: 25px;
    border-radius: 10px;
    margin-bottom: 30px;
}

.toc ul {
    list-style: none;
    margin: 0;
}

.toc li {
    padding: 8px 0;
    border-bottom: 1px solid var(--border-color);
}

.toc a {
    color: var(--primary-color);
    text-decoration: none;
    transition: color 0.3s;
}

.toc a:hover {
    color: var(--secondary-color);
}
```

### כרטיסי נקודות קצה של API

```css
.endpoint-card {
    background: var(--code-bg);
    border-radius: 10px;
    margin: 15px 0;
    overflow: hidden;
    border: 1px solid var(--border-color);
}

.endpoint-header {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px 20px;
    background: rgba(0, 136, 204, 0.1);
}

.method {
    padding: 5px 12px;
    border-radius: 5px;
    font-weight: bold;
    font-size: 0.85em;
}

.method-get { background: #2ecc71; color: white; }
.method-post { background: #3498db; color: white; }

.endpoint-path {
    font-family: monospace;
    color: var(--text-color);
    direction: ltr;
}
```

## עיצוב רספונסיבי

### נקודת שבירה לנייד (max-width: 768px)

```css
@media (max-width: 768px) {
    header h1 {
        font-size: 2em;
    }

    section {
        padding: 20px;
    }

    .grid-2 {
        grid-template-columns: 1fr;
    }
}
```

## רשימות

### עיצוב

```css
ul, ol {
    margin: 15px 30px;
    line-height: 1.8;
}

li {
    margin: 8px 0;
}
```

## הוראות שימוש

### תבנית מבנה המסמך

```html
<!DOCTYPE html>
<html dir="rtl" lang="he">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>מדריך טכני</title>
    <style>
        /* כאן נכנסים כל משתני ה-CSS והסגנונות */
    </style>
</head>
<body>
    <header>
        <h1>כותרת המדריך</h1>
        <p>תיאור קצר</p>
        <div>
            <span class="badge badge-primary">טכנולוגיה 1</span>
            <span class="badge badge-success">טכנולוגיה 2</span>
        </div>
    </header>

    <div class="container">
        <nav class="toc">
            <h3>תוכן עניינים</h3>
            <ul>
                <li><a href="#section1">1. נושא ראשון</a></li>
            </ul>
        </nav>

        <section id="section1">
            <h2><span class="icon">📊</span> נושא ראשון</h2>
            <!-- תוכן כאן -->
        </section>
    </div>
</body>
</html>
```

### עקרונות מרכזיים

1. **תמיד RTL**: ‏`dir="rtl"` על אלמנט ה‑`<html>`
2. **משתני CSS קודם**: הגדר את כל הצבעים כמשתני CSS
3. **HTML סמנטי**: השתמש באלמנטים סמנטיים של HTML5
4. **כיוון הקוד**: כל בלוקי הקוד צריכים להיות `ltr`
5. **מרווחים עקביים**: עקוב אחר הנחיות המרווחים בהקפדה
6. **שילוב אייקונים**: השתמש באימוג'י בכותרות H2 (רשות, אך מומלץ)
7. **שיפור מדורג**: עיצוב רספונסיבי בגישת mobile‑first

### דפוסים נפוצים

#### דפוס 1: סקציה עם התראה

```html
<section id="overview">
    <h2><span class="icon">📊</span> סקירה כללית</h2>
    <p>תוכן הסקירה...</p>

    <div class="alert-box alert-info">
        <span style="font-size: 1.5em;">💡</span>
        <div>
            <strong>טיפ:</strong> מידע שימושי
        </div>
    </div>
</section>
```

#### דפוס 2: גריד עם כרטיסי תכונה

```html
<div class="grid-2">
    <div class="feature-card">
        <h4>תכונה 1</h4>
        <p>תיאור התכונה</p>
    </div>
    <div class="feature-card">
        <h4>תכונה 2</h4>
        <p>תיאור התכונה</p>
    </div>
</div>
```

#### דפוס 3: בלוק קוד עם הדגשת תחביר

```html
<pre><code><span class="comment"># Comment</span>
<span class="keyword">def</span> <span class="function">example</span>():
    <span class="variable">result</span> = <span class="string">"Hello"</span>
    <span class="keyword">return</span> result</code></pre>
```

## שיטות עבודה מומלצות

1. **חיסכון בטוקנים**: צמצם סגנונות inline, השתמש במחלקות CSS
2. **קריאוּת**: שמור על ניגודיות גבוהה ומרווחים נדיבים
3. **עקביות**: השתמש באותם דפוסים לאורך כל המסמך
4. **נגישות**: הקפד על ניגודיות צבעים תקינה ועל HTML סמנטי
5. **ביצועים**: מזער סגנונות inline, השתמש במשתני CSS
6. **תחזוקתיות**: שמות מחלקות ברורים, מבנה הגיוני

## מתי **לא** להשתמש בסקיל הזה

- מסמכי טקסט פשוטים בלי קוד או תוכן טכני
- טפסים או אפליקציות אינטראקטיביות (השתמש בסקילים של webapp במקום)
- מסמכים מותאמים להדפסה (זה מותאם למסך)
- תיעוד בערכה בהירה (זה כהה)
