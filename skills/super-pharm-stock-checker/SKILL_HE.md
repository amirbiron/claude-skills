---
name: super-pharm-stock-checker
description: >-
  Checks real-time product stock availability at Super-Pharm branches across Israel via browser automation.
  Use when user asks to check Super-Pharm stock, "bdika melay sofer pharm", "האם יש מלאי בסופר-פארם",
  "soofer pharm melay", "sofer pharm stock", or any request to find a product at a nearby Super-Pharm branch.
  Supports Hebrew and English product names. Searches by product name and filters results by city.
  Do NOT use for Maccabi pharmacy stock (use maccabi-pharm-search instead).
license: MIT
compatibility: >-
  Requires Claude in Chrome MCP (browser automation). Works with Claude Code and Claude.ai with Chrome
  extension enabled. Does NOT work with OpenClaw or agents without Claude in Chrome MCP support.
metadata:
  author: BarMalka
  version: 1.1.0
  category: health-services
  tags:
    he:
      - סופר-פארם
      - בדיקת-מלאי
      - בית-מרקחת
      - ישראל
    en:
      - super-pharm
      - stock-check
      - pharmacy
      - israel
  display_name:
    he: "בודק מלאי סופר-פארם"
    en: Super-Pharm Stock Checker
  display_description:
    he: "בודק זמינות מוצרים בזמן אמת בסניפי סופר-פארם ברחבי ישראל — ללא פתיחת דפדפן."
    en: >-
      Checks real-time product stock availability at Super-Pharm branches across Israel using browser
      automation. No browser window needed — runs API calls directly via Claude in Chrome MCP.
  supported_agents:
    - claude-code
    - cursor
    - github-copilot
    - windsurf
    - opencode
    - codex
    # openclaw not supported — skill requires Claude in Chrome MCP
---

# בודק מלאי סופר-פארם

בדיקת **מלאי בזמן אמת** בסניפי סופר-פארם ברחבי ישראל — ללא פתיחת חלון דפדפן.

> **כתב ויתור**: כלי לא רשמי, אינו קשור לסופר-פארם ישראל ואינו מאושר על ידה. המידע עשוי שלא לשקף את המלאי
> בפועל. יש לאמת מול הסניף לפני הגעה.

## דרישות מוקדמות

הסקיל משתמש ב-**Claude in Chrome** — תוסף לדפדפן Chrome שמאפשר לקלוד לשלוט בטאב ולהריץ בו JavaScript.
ללא התוסף, שלב 1 להלן לא יפעל.

**התקנה:**
1. התקן את [תוסף Claude in Chrome](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome)
   — עקוב אחר מדריך ההתקנה בדף התמיכה של Anthropic.
2. פתח את Chrome וודא שהתוסף פעיל — אייקון Claude אמור להופיע בסרגל הכלים.
3. בסשן Claude Code / Cowork שלך, כלי `mcp__Claude_in_Chrome__*` יהיו זמינים כעת.

אם אינך מעוניין להשתמש בתוסף Chrome, ראה את **חלופת ה-CLI** בתחתית הקובץ.

## הוראות

### שלב 1: פתיחת אפליקציית בדיקת המלאי בדפדפן

השתמש ב-`mcp__Claude_in_Chrome__tabs_context_mcp` (עם `createIfEmpty: true`) לקבלת מזהה טאב, ולאחר מכן נווט:

```
mcp__Claude_in_Chrome__navigate → https://spinventoryapp.super-pharm.co.il/?v12
```

המתן עד שכותרת הדף תציג "STOCK CHECK" לפני שממשיכים.

### שלב 2: חיפוש המוצר

הרץ את קוד ה-JavaScript הבא דרך `mcp__Claude_in_Chrome__javascript_tool`:

```javascript
fetch('/api/InventoryCheck/SearchProduct', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ SearchString: '<שאילתה>', Page: 1, Department: '' })
})
.then(r => r.json())
.then(data => { window._spSearch = data; });
'done'
```

לאחר מכן קרא את התוצאות:

```javascript
JSON.stringify(
  (window._spSearch?.productsSearch?.products || [])
    .map(p => ({ id: p.productId, name: p.productName, brand: p.productTitle, barcode: p.primaryBarcode, superposID: p.superposID }))
)
```

בחר את המוצר הרלוונטי ביותר ושמור את ה-`productId` וה-`superposID` שלו.

> **קישור למוצר**: ה-`superposID` מאפשר לבנות קישור ישיר לדף המוצר באתר סופר-פארם:
> `https://shop.super-pharm.co.il/p/<superposID>` — מבצע redirect לדף המוצר המלא.
> שמור קישור זה לשימוש בשלב 5.

טיפים לחיפוש:

- השתמש במונחים קצרים: "מי חמצן" ולא "מי חמצן 3 אחוז"
- שמות בעברית עובדים: "אקמול", "נורופן", "מי חמצן"
- שמות באנגלית גם עובדים: "acamol", "nurofen", "ibuprofen"
- אם יש מספר תוצאות — הצג את הרשימה למשתמש ובקש ממנו לבחור

### שלב 3: קבלת רשימת הסניפים בעיר המבוקשת

```javascript
fetch('/api/InventoryCheck/GetBranchesAndCitys')
  .then(r => r.json())
  .then(data => { window._spBranches = data; });
'done'
```

סינון לפי עיר:

```javascript
JSON.stringify(
  window._spBranches.filter(b =>
    b.branchCity.includes('<עיר>') || b.branchName.includes('<עיר>')
  ).map(b => ({
    code: b.branchCode, name: b.branchName,
    city: b.branchCity, address: b.branchAddress,
    closeTime: b.todayCloseTime
  }))
)
```

### שלב 4: בדיקת מלאי

אפשרות א — סניפים ספציפיים (עד 5 סניפים):

```javascript
Promise.all([103, 243, 319].map(code =>
  fetch('/api/InventoryCheck/CheckInventory', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ BranchNumber: code, ProductIds: ['<PRODUCT_ID>'] })
  })
  .then(r => r.json())
  .then(data => ({ code, inStock: data.inventoryData?.items?.[0]?.availableInStock === 1 }))
))
.then(r => { window._spStock = r; });
'done'
```

אפשרות ב — כל הסניפים בעיר (מהיר יותר, מומלץ כאשר יש סניפים רבים):

```javascript
fetch('/api/InventoryCheck/NearbyBranches', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ BranchNumber: <קוד_סניף_בעיר>, ProductIds: ['<PRODUCT_ID>'] })
})
.then(r => r.json())
.then(data => { window._spNearby = data; });
'done'
```

קריאת תוצאות NearbyBranches:

```javascript
JSON.stringify(window._spNearby?.branches?.map(b => ({
  code: b.branchCode, address: b.branchAddress,
  city: b.branchCity, hours: b.branchOpeningTime,
  closeToday: b.todayCloseTime, isOpen: b.isOpen
})))
```

### שלב 5: הצגת התוצאות למשתמש

השתמש ב**תבנית הקבועה הזו בכל תגובה** — אין לאלתר את המבנה:

```
🛒 [שם המוצר] ([מותג]) | [לצפייה באתר סופר-פארם](https://shop.super-pharm.co.il/p/<superposID>)

📍 [עיר]:
✅ יש מלאי ב-X סניפים:
  • [שם סניף] — [כתובת] (סגירה: HH:MM)
  • ...

❌ אין מלאי ב-Y סניפים:
  • [שם סניף] — [כתובת]
  • ...
```

**כללים:**
- הקישור למוצר מופיע תמיד בשורה הראשונה, מיד אחרי שם המוצר — גם אם אין מלאי בסניפים (המשתמש יכול להזמין אונליין).
- הצג סניפים עם מלאי קודם, אחר כך סניפים ללא מלאי. בשימוש ב-`NearbyBranches` (שמחזיר רק סניפים עם מלאי), פשוט רשום אותם; כתוב "לא נמצאו סניפים עם מלאי" אם הרשימה ריקה.
- כלול תמיד שעת סגירה לסניפים עם מלאי.
- אם אין מלאי בכלל: הצג את שורת המוצר עם הקישור, ולאחר מכן כתוב "❌ אין מלאי בסניפים שנבדקו — ניתן להזמין דרך האתר."

עיין ב-`references/api-reference.md` לפרטים מלאים על ה-API ושדות התגובה.

## דוגמאות

### דוגמה 1: מוצר בעיר ספציפית

המשתמש שואל: "האם יש מי חמצן 3% בסניפי ראש העין?"

פעולות:
1. ניווט אל spinventoryapp.super-pharm.co.il
2. חיפוש "מי חמצן" — מציאת "מי חמצן 3%" מבית לייף
3. קבלת סניפי ראש העין — 3 סניפים (קודים 103, 243, 319)
4. שימוש ב-NearbyBranches עם קוד סניף 103
5. דיווח על תוצאות עם כתובות ושעות סגירה

תוצאה:
```
🛒 מי חמצן 3% (לייף) | [לצפייה באתר סופר-פארם](https://shop.super-pharm.co.il/p/236588)

📍 ראש העין:
✅ יש מלאי ב-3 סניפים:
  • גבעת טל — משה דיין 2 (סגירה: 22:00)
  • שבזי ראש העין — שבזי 10 (סגירה: 22:00)
  • שפיר סנטר — דרך השרון 5 (סגירה: 21:00)
```

### דוגמה 2: חיפוש עם מספר תוצאות

המשתמש שואל: "בדוק אם יש אקמול בתל אביב בסופר-פארם"

פעולות:
1. ניווט לאפליקציה
2. חיפוש "אקמול" — תוצאות מרובות (מינונים וצורות שונות)
3. הצגת הרשימה למשתמש, בקשת בחירה
4. לאחר בחירה — קבלת סניפי תל אביב, הרצת NearbyBranches
5. דיווח: סניפים עם מלאי וסניפים ללא מלאי

## חלופת CLI (ללא תוסף Chrome)

אם למשתמש אין Claude in Chrome מותקן, הסקיל כולל סקריפט Node.js שקורא לאותם API endpoints ישירות מהטרמינל:

```bash
# חיפוש מוצר
node scripts/stock-check.js search "מי חמצן"

# בדיקת מלאי לפי עיר (הדבק את productId מתוצאת החיפוש)
node scripts/stock-check.js stock 4ed182e3-f324-46e0-8e0a-65b54de38c6e "ראש העין"

# רשימת סניפים בעיר
node scripts/stock-check.js branches "תל אביב"
```

דרישות: Node.js גרסה 14 ומעלה — אין צורך ב-npm install (משתמש רק בספריות מובנות של Node.js).

השתמש בחלופת ה-CLI כאשר: המשתמש מפעיל Claude Code בסביבת טרמינל בלבד, או כאשר תוסף Chrome אינו זמין.

## משאבים מצורפים

### מסמכי עזר
- `references/api-reference.md` — מפרט מלא של נקודות ה-API, סכמות בקשה/תגובה, הגדרות שדות
  ומשמעויות ערכי `availableInStock`. עיין כאשר מאפיינים את ה-API לצורכי פתרון תקלות.

## נקודות תשומת לב

- מונחי חיפוש קצרים בלבד: "מי חמצן" עובד; "מי חמצן 3 אחוז" עלול להחזיר מוצרים לא קשורים.
- NearbyBranches מחזיר רק סניפים עם מלאי — לבדיקת סניפים ללא מלאי יש להשתמש ב-CheckInventory.
- Content-Type חובה: כל בקשות POST חייבות לכלול `Content-Type: application/json`, אחרת ה-API יחזיר שגיאה 415.
- הדף חייב להיטען תחילה — יש להמתין לכותרת "STOCK CHECK" לפני הרצת JavaScript.

## פתרון תקלות

### אין תוצאות לחיפוש

סיבה: מונח החיפוש ארוך מדי או מכיל מילים שאינן באינדקס.
פתרון: קצר את השאילתה. השתמש בשם המותג בעברית או בשם החומר הפעיל בלבד.

### CheckInventory מחזיר מערך items ריק

סיבה: ה-productId או BranchNumber עלולים להיות שגויים.
פתרון: ודא שה-productId הגיע מקריאת SearchProduct באותה הסשן. ודא את קוד הסניף מתגובת GetBranchesAndCitys.

### ה-API מחזיר שגיאה 415

סיבה: כותרת Content-Type חסרה או שגויה.
פתרון: ודא שכל בקשת POST כוללת `headers: { 'Content-Type': 'application/json' }`.

### הניווט נכשל או הדף לא נטען

סיבה: הדומיין spinventoryapp.super-pharm.co.il עשוי להיות לא זמין זמנית.
פתרון: המתן 10–15 שניות ונסה שוב. אם הבעיה נמשכת, שירות בדיקת המלאי עשוי להיות מושבת.
הפנה את המשתמש אל https://shop.super-pharm.co.il/stock-check.
