# Super-Pharm Inventory API Reference

Base URL: `https://spinventoryapp.super-pharm.co.il`

All API calls must be made from within the browser page context (via `mcp__Claude_in_Chrome__javascript_tool`
after navigating to the app). The browser's session handles authentication automatically.

---

## GET /api/InventoryCheck/GetBranchesAndCitys

Returns all Super-Pharm branches with their codes, cities, addresses, and today's closing time.

**Request:** No body required.

**Response:** JSON array of branch objects.

| Field | Type | Description |
|-------|------|-------------|
| `branchCode` | number | Unique branch identifier (used in other API calls) |
| `branchCity` | string | City name in Hebrew (e.g., `"ראש העין"`, `"תל אביב - יפו"`) |
| `branchName` | string | Branch display name (e.g., `"גבעת טל"`, `"שבזי ראש העין"`) |
| `branchAddress` | string | Street address |
| `todayCloseTime` | string | Today's closing time in `HH:MM` format (e.g., `"22:00"`) |

**Example response item:**
```json
{
  "branchCode": 103,
  "branchCity": "ראש העין",
  "branchName": "גבעת טל",
  "branchAddress": "משה דיין 2 גבעת טל",
  "todayCloseTime": "16:00"
}
```

---

## POST /api/InventoryCheck/SearchProduct

Searches for products by name or keyword.

**Request body (JSON):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `SearchString` | string | Yes | Product name or keyword (Hebrew or English) |
| `Page` | number | Yes | Page number, start with `1` |
| `Department` | string | No | Department filter, pass `""` to search all |

**Response:** Object containing `productsSearch.products` array.

| Field | Type | Description |
|-------|------|-------------|
| `productId` | string (UUID) | Unique product identifier — use this for inventory checks |
| `productName` | string | Product name in Hebrew |
| `productTitle` | string | Brand/manufacturer name |
| `primaryBarcode` | string | Product barcode |
| `superposID` | number | Internal Super-Pharm POS system ID |

**Example response:**
```json
{
  "productsSearch": {
    "products": [
      {
        "productId": "4ed182e3-f324-46e0-8e0a-65b54de38c6e",
        "productName": "מי חמצן 3%",
        "productTitle": "לייף",
        "primaryBarcode": "7290001307717",
        "superposID": 236588
      }
    ]
  }
}
```

**Search behavior notes:**
- The API uses keyword matching — long queries with multiple words may split and match unrelated products
- Best results with 1–2 word queries: `"מי חמצן"` not `"מי חמצן 3 אחוז"`
- Returns up to ~20 results per page; use `Page: 2` to paginate

---

## POST /api/InventoryCheck/CheckInventory

Checks whether a specific product is in stock at a specific branch.

**Request body (JSON):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `BranchNumber` | number | Yes | Branch code from GetBranchesAndCitys |
| `ProductIds` | string[] | Yes | Array of product UUIDs from SearchProduct |

**Response:** Object containing `inventoryData.items` array.

| Field | Type | Description |
|-------|------|-------------|
| `productId` | string | The product UUID |
| `branchNumber` | number | The branch code |
| `availableInStock` | number | Stock status (see table below) |
| `productSuperPosId` | number | Internal POS ID |

**`availableInStock` values:**

| Value | Meaning |
|-------|---------|
| `1` | In stock ✅ |
| `0` | Out of stock ❌ |
| `-1` | Error / unknown ❓ |

**Example response:**
```json
{
  "inventoryData": {
    "items": [
      {
        "productId": "4ed182e3-f324-46e0-8e0a-65b54de38c6e",
        "branchNumber": 103,
        "availableInStock": 1,
        "productSuperPosId": 236588
      }
    ],
    "errMessage": null,
    "isSuccess": true
  }
}
```

---

## POST /api/InventoryCheck/NearbyBranches

Returns all branches in the area of a given branch that have the product in stock. Faster than calling
CheckInventory for each branch individually when you want "all branches in a city".

**Request body (JSON):**

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `BranchNumber` | number | Yes | Any branch code in the target city/area |
| `ProductIds` | string[] | Yes | Array of product UUIDs |

**Response:** Object containing `branches` array — only branches **with stock** are returned.

| Field | Type | Description |
|-------|------|-------------|
| `branchCode` | string | Branch code (note: string, not number here) |
| `branchAddress` | string | Street address |
| `branchCity` | string | City name |
| `branchOpeningTime` | string | Full weekly hours (multiline, includes Shabbat) |
| `todayCloseTime` | string | Today's closing time `HH:MM` |
| `isOpen` | boolean | Whether the branch is currently open |
| `longitude` | number | GPS longitude |
| `latitude` | number | GPS latitude |

**Example response:**
```json
{
  "branches": [
    {
      "branchCode": "103",
      "branchAddress": "משה דיין 2 גבעת טל",
      "branchCity": "ראש העין",
      "branchOpeningTime": "א'-ה': 08:00-22:00\r\nשישי: 08:00-16:00\r\nשבת: 20:30-22:00",
      "todayCloseTime": "16:00",
      "isOpen": true,
      "longitude": 32.09247,
      "latitude": 34.9657
    }
  ]
}
```

**Important:** If the product is out of stock in all branches near the given branch code, `branches` will
be an empty array — not an error.

---

## Known City Name Formats

Hebrew city names in the API use official municipality names, which may differ from colloquial usage:

| Common name | API value |
|-------------|-----------|
| תל אביב | `"תל אביב - יפו"` |
| ראש העין | `"ראש העין"` |
| ירושלים | `"ירושלים"` |
| חיפה | `"חיפה"` |
| באר שבע | `"באר שבע"` |

Use `.includes()` for fuzzy matching rather than strict equality.
