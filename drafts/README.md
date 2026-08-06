# drafts

סקילים שנכתבו כאן ועדיין לא הותקנו בחשבון ב‑claude.ai.

## למה זה לא יושב ב‑`skills/`

‏`skills/` הוא מראה של החשבון, ו‑`scripts/snapshot-skills.sh` עושה mirror ולא
merge — הוא מוחק כל מה שאין לו מקבילה ב‑`~/.claude/skills`. סקיל שנכתב כאן
ועוד לא הותקן היה נמחק בריענון הבא, כנראה בלי שאף אחד ישים לב.

לכן הכיוון הוא חד‑סטרי: כותבים ב‑`drafts/`, מתקינים ידנית ב‑claude.ai, ומשם
הצילום הבא מרים את הסקיל לתוך `skills/` לבד. אחרי שזה קרה, אפשר למחוק את
הטיוטה.

## התקנה מהנייד

1. מורידים את ה‑zip של הסקיל (או בונים אותו, ראו למטה)
2. ‏claude.ai ← Settings ← Capabilities ← Skills ← Upload
3. אחרי ההתקנה, בסשן הבא: `bash scripts/snapshot-skills.sh` ואז
   `python3 scripts/build-index.py` ו‑`python3 scripts/build-viewer.py`

## בניית ה‑zip

מתוך `drafts/`:

```bash
zip -r incident-response.zip incident-response
```

הקובץ נשאר מחוץ ל‑git בכוונה: הוא נגזר מ‑`SKILL.md` ולא מוסיף עליו כלום,
וקובץ בינארי שנשמר בריפו מתיישן בשקט בכל פעם שהמקור משתנה.

## מה יש כאן עכשיו

| סקיל | מה הוא עושה |
| --- | --- |
| `incident-response` | תקלת ייצור אצל לקוח, לבד ומהטלפון: מה בודקים ובאיזה סדר, מה כותבים ללקוח, ואיך סוגרים בפסקה |
