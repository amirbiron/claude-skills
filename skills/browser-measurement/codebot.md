# CodeBot — פרטי הסביבה

פתח רק כשעובדים על הריפו `amirbiron/CodeBot`. הפרטים כאן ספציפיים לו.

## שרת בדיקה

שרת Flask אמיתי מול מונגו אמיתי, עם ראוט התחברות שנוסף רק לבדיקה. הוא מייבא את `webapp.app` כמו שהוא — לא מוק.

**השמה מפורשת ל-`MONGODB_URL`, ולא `setdefault`.** ההארנס הזה **כותב** — הוא מאפס פתקים ויוצר מצב בדיקה — ו-`setdefault` משמר ערך קיים בסביבה. נמדד: עם `MONGODB_URL` שמצביע על בסיס נתונים אמיתי, `setdefault` השאיר אותו, ו-`database/manager.py` מתחבר לפי מה שיש ב-`os.environ` בזמן הריצה. כלומר ההארנס היה כותב נתוני בדיקה לפרודקשן. אותו נימוק חל על `DISABLE_DB`. ל-`BOT_TOKEN` ו-`SECRET_KEY` זה פחות קריטי, אבל אין סיבה שיהיו שונים.

הנתיב ב-`sys.path.insert` הוא של הקלון בסביבה הזו — החליפו אותו בנתיב הקלון המקומי שלכם.

```python
import os
os.environ["MONGODB_URL"] = "mongodb://127.0.0.1:27114/code_keeper_bot"
os.environ["BOT_TOKEN"] = "dummy"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["DISABLE_DB"] = "0"
import sys; sys.path.insert(0, "/home/user/CodeBot")

UID = 4242
from webapp.app import app

@app.route("/__login")
def __login():
    from flask import session, redirect, request
    session["user_id"] = UID
    session["username"] = "tester"
    return redirect(request.args.get("next", "/"))

app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5201")),
        debug=False, use_reloader=False)
```

מונגו: הורד בינארי של mongod והרץ עם `--fork --logpath`. בלי `--fork` הוא נקטל כשהפקודה שהריצה אותו מסתיימת. שם ה-DB הוא `code_keeper_bot`, ו-`board_id` בפתקים נשמר כמחרוזת ולא כ-`ObjectId`.

## מצבים שמשנים מה מרונדר

- **אדמין** — נקבע לפי משתנה הסביבה `ADMIN_USER_IDS` (רשימה מופרדת בפסיקים, `user_roles.py`). בלי שמשתמש הבדיקה שם, אלמנטים שעטופים ב-`{% if user_is_admin %}` פשוט אינם ב-DOM. מדדתי "0 בקשות" והייתי בטוח שזה תיקון — זו הייתה פשוט תבנית שלא רונדרה.
- **`?force_admin=1`** מבטל התחזות בלבד. הוא **אינו** מעניק אדמין.
- **`no-fa-icons`** — כש-FontAwesome לא נטען (למשל בסביבה בלי גישה ל-CDN), הוא מתווסף ל-`body` ומסתיר את `.qa-icon`. גדלים שנמדדים אז יוצאים 0.
- **מודאל הפתיחה** מכסה את העמוד ובולע לחיצות. הסר אותו לפני מדידה, או שלח `POST /api/welcome/ack`.

## מוסכמות טסטים בריפו

- טסטי JS: `node --test tests/*.test.js`, עם סנדבוקס `FakeEl` ידני. ל-`FakeEl` יש `closest`, `hasAttribute` ו-`classList` אמיתיים, אז אפשר לבדוק לוגיקת DOM טהורה בלי דפדפן.
- טסטי פייתון: `python3 -m pytest ... -q --no-cov`. **אל** תוסיף `-p no:cacheprovider` — ה-`conftest` של הפרויקט נשען על `config.cache` ונופל בלעדיו.
- Playwright **אינו** בתלויות הפרויקט. הארנס שנשען עליו לא ירוץ ב-CI, ולכן מה שנכנס לריפו הוא שומר טקסטואלי שקורא את הקובץ ומוודא שההחלטה לא בוטלה.

## כללי הבית שרלוונטיים למדידה

- אין לאמת תיעוד בבנייה ל-RTD. אימות מול הקוד בלבד.
- לפני שינוי CSS — לקרוא את `docs/webapp/theming_and_css.rst`. הוא עוסק בטוקני צבע; אם השינוי אינו נוגע בהם, אומרים זאת מפורשות ב-PR.
- תיאורי PR בעברית, לפי `.github/pull_request_template.md`.