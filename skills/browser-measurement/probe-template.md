# שלד הארנס מדידה

פתח את הקובץ הזה כשאתה כותב מדידה חדשה. הוא לא ספרייה — הוא תבנית להעתיק ולקצץ.

## המבנה

הארנס טוב הוא רשימת טענות שכל אחת מדפיסה מה נמדד, לא רק אם עברה. הפירוט הוא מה שמאפשר לאבחן כישלון בלי להריץ שוב.

```python
results = []

def check(name, ok, detail=''):
    results.append((name, ok, detail))
    print("%-4s %-50s %s" % ("OK" if ok else "XX", name, detail))
```

בסוף: הדפס `N/M עברו` ורשימת השמות שנפלו, וצא עם קוד יציאה שאינו אפס אם משהו נפל. בלי זה אי אפשר להשתמש בהארנס בלולאת מוטציות.

## מגע אמיתי דרך CDP

`TouchEvent` שנבנה ב-JS אינו מפעיל גלילה מקורית. להחלקה אמיתית צריך את צינור הקלט של הדפדפן:

```python
cdp = context.new_cdp_session(page)

def swipe(cdp, x, y, dx, dy, steps=10):
    cdp.send('Input.dispatchTouchEvent',
             {'type': 'touchStart', 'touchPoints': [{'x': x, 'y': y}]})
    for i in range(1, steps + 1):
        cdp.send('Input.dispatchTouchEvent', {'type': 'touchMove', 'touchPoints': [
            {'x': x + dx * i / steps, 'y': y + dy * i / steps}]})
    cdp.send('Input.dispatchTouchEvent', {'type': 'touchEnd', 'touchPoints': []})
```

הקשר חייב `has_touch=True`. לגלילה, האות הנמדד הוא `window.scrollY` אחרי המתנה קצרה.

## ספירת בקשות רשת

```python
seen = []
page.on('response', lambda r: seen.append(
    (r.url, r.status, int(r.headers.get('content-length') or 0))))
```

מדוד לפני ואחרי הפעולה בנפרד: שמור את אורך `seen` לפני, וחתוך משם. אחרת אתה סופר גם את מה שקרה בטעינה.

## בקרות שפיות שכדאי כמעט תמיד

לפני כל טענה, בדוק שהתנאי המקדים מתקיים:

```python
check('sanity: page is scrollable',
      page.evaluate("()=>document.documentElement.scrollHeight > window.innerHeight+200"))

hit = page.evaluate("([x,y])=>{const e=document.elementFromPoint(x,y);"
                    "return e?(e.className||e.tagName):'none';}", point)
check('sanity: point is the element I think', 'expected-class' in str(hit), hit)
```

ולמגע — היעד בפועל, לא `elementFromPoint`:

```python
page.evaluate("""()=>{window.__tt=null;
  document.addEventListener('touchstart',
    (e)=>{window.__tt=e.target.className||e.target.tagName;}, true);}""")
# dispatch a tap here, then read window.__tt
```

## איפוס מצב בין ריצות

בדיקה שלוחצת כפתורים אמיתיים משנה מצב שנשמר, וכל מה שרץ אחריה נמדד על מצב שגוי. שתי אפשרויות:

1. אפס ב-DB/API לפני כל ריצה, בסקריפט נפרד שמדפיס את המצב שאליו אופס.
2. אם רק צריך לוודא שהאירוע מגיע — בלע אותו במאזין בשלב הלכידה במקום להפעיל את ההשלכות:

```javascript
const spy = (ev) => { got = true; ev.stopImmediatePropagation(); ev.preventDefault(); };
el.addEventListener('click', spy, true);
```

## מדידה מחדש של גאומטריה

האלמנט זז בגלל הבדיקות עצמן. אל תשמור `getBoundingClientRect` בתחילת הריצה ותשתמש בו בסוף — מדוד מחדש לפני כל אינטראקציה.