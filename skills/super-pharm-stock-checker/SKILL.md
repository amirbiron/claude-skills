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

# Super-Pharm Stock Checker

Check **real-time inventory** at Super-Pharm branches across Israel without opening a browser.

> **Disclaimer**: Unofficial tool, not affiliated with or endorsed by Super-Pharm Israel. Stock data may
> not reflect actual availability. Always call the branch to confirm before visiting.

## Prerequisites

This skill uses **Claude in Chrome** — a browser extension that lets Claude control a Chrome tab and run
JavaScript in it. Without it, Step 1 below will fail.

**To install:**
1. Install the [Claude in Chrome extension](https://support.claude.com/en/articles/12012173-get-started-with-claude-in-chrome)
   — follow the setup guide on Anthropic's support page.
2. Open Chrome and make sure the extension is active (you should see the Claude icon in the toolbar).
3. In your Claude Code / Cowork session, the `mcp__Claude_in_Chrome__*` tools will now be available.

> If you prefer not to use the Chrome extension, see the **CLI Alternative** at the bottom of this file.

## Instructions

### Step 1: Open the Stock Check App in the Browser

Use `mcp__Claude_in_Chrome__tabs_context_mcp` (with `createIfEmpty: true`) to get a tab ID, then navigate:

```
mcp__Claude_in_Chrome__navigate → https://spinventoryapp.super-pharm.co.il/?v12
```

Wait until the page title reads **"STOCK CHECK"** before proceeding.

### Step 2: Search for the Product

Run the following JavaScript via `mcp__Claude_in_Chrome__javascript_tool`:

```javascript
fetch('/api/InventoryCheck/SearchProduct', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ SearchString: '<QUERY>', Page: 1, Department: '' })
})
.then(r => r.json())
.then(data => { window._spSearch = data; });
'done'
```

Then read the results:

```javascript
JSON.stringify(
  (window._spSearch?.productsSearch?.products || [])
    .map(p => ({ id: p.productId, name: p.productName, brand: p.productTitle, barcode: p.primaryBarcode, superposID: p.superposID }))
)
```

Pick the most relevant product and note its `productId` and `superposID`.

> **Product link**: The `superposID` maps directly to a short product URL on the Super-Pharm shop:
> `https://shop.super-pharm.co.il/p/<superposID>` — this redirects to the full product page.
> Keep this URL handy; you'll include it in the final report (Step 5).

| Search tip | Example |
|------------|---------|
| Use short terms | `"מי חמצן"` not `"מי חמצן 3 אחוז"` |
| Hebrew works | `"אקמול"`, `"נורופן"`, `"מי חמצן"` |
| English works | `"acamol"`, `"nurofen"`, `"ibuprofen"` |
| Multiple results? | Show list to user and ask them to choose |

### Step 3: Get Branch List for the Requested City

```javascript
fetch('/api/InventoryCheck/GetBranchesAndCitys')
  .then(r => r.json())
  .then(data => { window._spBranches = data; });
'done'
```

Filter by city:

```javascript
JSON.stringify(
  window._spBranches.filter(b =>
    b.branchCity.includes('<CITY>') || b.branchName.includes('<CITY>')
  ).map(b => ({
    code: b.branchCode, name: b.branchName,
    city: b.branchCity, address: b.branchAddress,
    closeTime: b.todayCloseTime
  }))
)
```

### Step 4: Check Inventory

**Option A — Specific branches** (when you have 1–5 branch codes):

```javascript
Promise.all([103, 243, 319].map(code =>   // replace with actual branch codes
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

**Option B — All branches in city** (faster, use this when the city has many branches):

```javascript
fetch('/api/InventoryCheck/NearbyBranches', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ BranchNumber: <ANY_BRANCH_CODE_IN_CITY>, ProductIds: ['<PRODUCT_ID>'] })
})
.then(r => r.json())
.then(data => { window._spNearby = data; });
'done'
```

Read NearbyBranches results:

```javascript
JSON.stringify(window._spNearby?.branches?.map(b => ({
  code: b.branchCode, address: b.branchAddress,
  city: b.branchCity, hours: b.branchOpeningTime,
  closeToday: b.todayCloseTime, isOpen: b.isOpen
})))
```

### Step 5: Report to the User

Use this **exact template** for every response — no improvising the structure:

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

**Rules:**
- Always include the product link on the first line, right after the product name — even when no branches have stock (the user can order online).
- List in-stock branches first, then out-of-stock. When using `NearbyBranches` (which only returns in-stock branches), just list those; write "לא נמצאו סניפים עם מלאי" if the list is empty.
- Always include the closing time for in-stock branches.
- When no branches have stock at all: show the product line with the link, then write "❌ אין מלאי בסניפים שנבדקו — ניתן להזמין דרך האתר."

Consult `references/api-reference.md` for full endpoint specifications and response field definitions.

## Examples

### Example 1: Product in a specific city

User says: "האם יש מי חמצן 3% בסניפי ראש העין?"

Actions:
1. Navigate to `https://spinventoryapp.super-pharm.co.il/?v12`
2. Search `"מי חמצן"` → find "מי חמצן 3%" by לייף, `productId: 4ed182e3-...`
3. Get branches filtered by `"ראש העין"` → 3 branches (codes 103, 243, 319)
4. Use Option B (`NearbyBranches`) with branch code 103
5. Report results with addresses and closing times

Result:
```
🛒 מי חמצן 3% (לייף) | [לצפייה באתר סופר-פארם](https://shop.super-pharm.co.il/p/236588)

📍 ראש העין:
✅ יש מלאי ב-3 סניפים:
  • גבעת טל — משה דיין 2 (סגירה: 22:00)
  • שבזי ראש העין — שבזי 10 (סגירה: 22:00)
  • שפיר סנטר — דרך השרון 5 (סגירה: 21:00)
```

### Example 2: Product search with multiple results

User says: "בדוק אם יש אקמול בתל אביב בסופר-פארם"

Actions:
1. Navigate to app
2. Search `"אקמול"` → multiple results (different dosages, formats)
3. Present list to user, ask which product
4. After user picks → get Tel Aviv branches → run NearbyBranches
5. Report: branches with stock, branches without

### Example 3: English product name

User says: "Is nurofen in stock at Super-Pharm in Haifa?"

Actions:
1. Navigate to app
2. Search `"nurofen"` → returns Hebrew product names with matching entries
3. Pick most relevant product
4. Get Haifa branches → check inventory → report

## CLI Alternative (No Chrome Extension Required)

If the user doesn't have Claude in Chrome installed, the skill ships a Node.js script that calls the
same API endpoints directly from the terminal:

```bash
# Search for a product
node scripts/stock-check.js search "מי חמצן"

# Check stock by city (paste the productId from the search result)
node scripts/stock-check.js stock 4ed182e3-f324-46e0-8e0a-65b54de38c6e "ראש העין"

# List all branches in a city
node scripts/stock-check.js branches "תל אביב"
```

Requirements: Node.js 14+ — no npm install needed (uses only Node.js built-ins).

Use the CLI route when: the user is running Claude Code in a terminal-only environment, or the Chrome
extension is not available.

## Bundled Resources

### References
- `references/api-reference.md` — Full API endpoint specs, request/response schemas, field definitions,
  and `availableInStock` value meanings. Consult when debugging unexpected API responses or building
  advanced queries.

## Gotchas

- **Short search terms only**: `"מי חמצן"` works; `"מי חמצן 3 אחוז"` may return unrelated products due to
  keyword splitting in the search API.
- **NearbyBranches returns only in-stock branches**: If you need out-of-stock information too, use
  CheckInventory per branch instead.
- **Content-Type is required**: All POST requests must include `Content-Type: application/json` or the
  API returns HTTP 415.
- **Page must be loaded first**: API calls made before the page finishes loading may fail. Always wait
  for the page title to read "STOCK CHECK" before running JavaScript.

## Troubleshooting

### No products returned for search

Cause: Search term is too long or contains words not indexed.
Solution: Shorten the query. Use the product's Hebrew brand name or active ingredient only.

### CheckInventory returns empty items array

Cause: The productId or BranchNumber may be incorrect.
Solution: Verify the `productId` came from a SearchProduct call in the same session. Verify branch code
from the GetBranchesAndCitys response.

### API returns HTTP 415

Cause: Missing or wrong `Content-Type` header.
Solution: Ensure every POST request includes `headers: { 'Content-Type': 'application/json' }`.

### Navigation fails or page doesn't load

Cause: The spinventoryapp.super-pharm.co.il domain may be temporarily unavailable.
Solution: Wait 10–15 seconds and retry. If still failing, the Super-Pharm stock check service may be
down. Direct the user to https://shop.super-pharm.co.il/stock-check instead.
