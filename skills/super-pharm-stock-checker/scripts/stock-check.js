#!/usr/bin/env node
/**
 * Super-Pharm Stock Checker
 * Checks real-time inventory at Super-Pharm branches in Israel.
 *
 * Usage:
 *   node stock-check.js search <query>
 *   node stock-check.js stock <productId> [city]
 *   node stock-check.js branches [city]
 *   node stock-check.js cities
 *   node stock-check.js test
 *
 * API base: https://spinventoryapp.super-pharm.co.il
 */

const https = require('https');

const BASE_URL = 'https://spinventoryapp.super-pharm.co.il';

// ─── HTTP helpers ────────────────────────────────────────────────────────────

function httpGet(path) {
  return new Promise((resolve, reject) => {
    https.get(`${BASE_URL}${path}`, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`Failed to parse response: ${data.substring(0, 200)}`)); }
      });
    }).on('error', reject);
  });
}

function httpPost(path, body) {
  const payload = JSON.stringify(body);
  return new Promise((resolve, reject) => {
    const options = {
      hostname: 'spinventoryapp.super-pharm.co.il',
      path,
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Content-Length': Buffer.byteLength(payload),
      },
    };
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try { resolve(JSON.parse(data)); }
        catch (e) { reject(new Error(`Failed to parse response (${res.statusCode}): ${data.substring(0, 200)}`)); }
      });
    });
    req.on('error', reject);
    req.write(payload);
    req.end();
  });
}

// ─── API calls ───────────────────────────────────────────────────────────────

async function getBranches() {
  return httpGet('/api/InventoryCheck/GetBranchesAndCitys');
}

async function searchProduct(query, page = 1, department = '') {
  const result = await httpPost('/api/InventoryCheck/SearchProduct', {
    SearchString: query,
    Page: page,
    Department: department,
  });
  return result.productsSearch?.products || [];
}

async function checkInventory(branchCode, productIds) {
  const result = await httpPost('/api/InventoryCheck/CheckInventory', {
    BranchNumber: branchCode,
    ProductIds: productIds,
  });
  return result.inventoryData?.items || [];
}

async function getNearbyBranches(branchCode, productIds) {
  const result = await httpPost('/api/InventoryCheck/NearbyBranches', {
    BranchNumber: branchCode,
    ProductIds: productIds,
  });
  return result.branches || [];
}

// ─── Commands ────────────────────────────────────────────────────────────────

async function cmdSearch(query) {
  if (!query) { console.error('Usage: stock-check.js search <query>'); process.exit(1); }
  console.log(`\nSearching for: "${query}"\n`);
  const products = await searchProduct(query);
  if (!products.length) {
    console.log('No products found.');
    return;
  }
  products.forEach(p => {
    console.log(`${p.productTitle ? p.productTitle + ' - ' : ''}${p.productName}`);
    console.log(`  Product ID: ${p.productId}`);
    console.log(`  Barcode:    ${p.primaryBarcode}`);
    console.log(`  SuperPos:   ${p.superposID}`);
    console.log();
  });
}

async function cmdStock(productId, cityFilter) {
  if (!productId) { console.error('Usage: stock-check.js stock <productId> [city]'); process.exit(1); }

  const allBranches = await getBranches();
  let branches = allBranches;

  if (cityFilter) {
    branches = allBranches.filter(b =>
      b.branchCity.includes(cityFilter) || b.branchName.includes(cityFilter)
    );
    if (!branches.length) {
      console.log(`\nNo branches found for city: "${cityFilter}"`);
      console.log('Run "cities" to see all available city names.');
      return;
    }
  }

  console.log(`\nChecking stock for product ${productId}${cityFilter ? ` in: ${cityFilter}` : ' (all branches)'}\n`);

  // Check all branches in parallel (batches of 10 to be polite)
  const results = [];
  const batchSize = 10;
  for (let i = 0; i < branches.length; i += batchSize) {
    const batch = branches.slice(i, i + batchSize);
    const checks = await Promise.all(
      batch.map(async branch => {
        try {
          const items = await checkInventory(branch.branchCode, [productId]);
          const item = items.find(it => it.productId === productId || String(it.branchNumber) === String(branch.branchCode));
          return {
            branch,
            availableInStock: item ? item.availableInStock : 0,
          };
        } catch {
          return { branch, availableInStock: -1 };
        }
      })
    );
    results.push(...checks);
  }

  const inStock   = results.filter(r => r.availableInStock === 1);
  const outStock  = results.filter(r => r.availableInStock === 0);
  const unknown   = results.filter(r => r.availableInStock === -1);

  console.log(`=== Stock Summary ===`);
  console.log(`  ✅ In Stock:     ${inStock.length} branches`);
  console.log(`  ❌ Out of Stock: ${outStock.length} branches`);
  if (unknown.length) console.log(`  ❓ Unknown:      ${unknown.length} branches`);
  console.log();

  if (inStock.length) {
    console.log(`=== Branches with Stock ===`);
    inStock.forEach(r => {
      const b = r.branch;
      console.log(`✅ ${b.branchName || b.branchCity}`);
      console.log(`   📍 ${b.branchAddress}, ${b.branchCity}`);
      if (b.todayCloseTime) console.log(`   🕐 סוגר היום: ${b.todayCloseTime}`);
      console.log();
    });
  }

  if (outStock.length && cityFilter) {
    console.log(`=== Branches Without Stock ===`);
    outStock.forEach(r => {
      const b = r.branch;
      console.log(`❌ ${b.branchName || b.branchCity} — ${b.branchAddress}`);
    });
    console.log();
  }
}

async function cmdBranches(cityFilter) {
  const allBranches = await getBranches();
  let branches = allBranches;
  if (cityFilter) {
    branches = allBranches.filter(b =>
      b.branchCity.includes(cityFilter) || b.branchName.includes(cityFilter)
    );
  }
  console.log(`\n=== Super-Pharm Branches${cityFilter ? ` in ${cityFilter}` : ''} (${branches.length}) ===\n`);
  branches.forEach(b => {
    console.log(`${b.branchName || b.branchCity} [${b.branchCode}]`);
    console.log(`  📍 ${b.branchAddress}, ${b.branchCity}`);
    if (b.todayCloseTime) console.log(`  🕐 סוגר היום: ${b.todayCloseTime}`);
    console.log();
  });
}

async function cmdCities() {
  const branches = await getBranches();
  const cities = [...new Set(branches.map(b => b.branchCity))].sort();
  console.log(`\n=== Available Cities (${cities.length}) ===\n`);
  cities.forEach(c => console.log(`  ${c}`));
}

async function cmdTest() {
  console.log('Running quick test...\n');
  try {
    const branches = await getBranches();
    console.log(`✅ GetBranchesAndCitys: ${branches.length} branches loaded`);

    const products = await searchProduct('אקמול');
    console.log(`✅ SearchProduct: found ${products.length} products for "אקמול"`);
    if (products.length > 0) {
      console.log(`   First result: ${products[0].productTitle} ${products[0].productName} (${products[0].productId})`);
    }

    if (products.length > 0) {
      const firstBranchCode = branches[0].branchCode;
      const items = await checkInventory(firstBranchCode, [products[0].productId]);
      const status = items[0]?.availableInStock === 1 ? '✅ IN STOCK' : '❌ OUT OF STOCK';
      console.log(`✅ CheckInventory: ${products[0].productName} at ${branches[0].branchName} → ${status}`);
    }

    console.log('\n✅ All tests passed!');
  } catch (e) {
    console.error('❌ Test failed:', e.message);
    process.exit(1);
  }
}

// ─── CLI entry ───────────────────────────────────────────────────────────────

const [,, command, ...args] = process.argv;

(async () => {
  switch (command) {
    case 'search':   await cmdSearch(args.join(' ')); break;
    case 'stock':    await cmdStock(args[0], args[1]); break;
    case 'branches': await cmdBranches(args[0]); break;
    case 'cities':   await cmdCities(); break;
    case 'test':     await cmdTest(); break;
    default:
      console.log(`
Super-Pharm Stock Checker
Usage:
  node stock-check.js search <query>           Search for a product
  node stock-check.js stock <productId> [city] Check stock at branches
  node stock-check.js branches [city]          List branches
  node stock-check.js cities                   List all cities
  node stock-check.js test                     Quick sanity check

Examples:
  node stock-check.js search "מי חמצן"
  node stock-check.js stock 4ed182e3-f324-46e0-8e0a-65b54de38c6e "ראש העין"
  node stock-check.js branches "תל אביב"
  node stock-check.js cities
`);
  }
})().catch(e => {
  console.error('Error:', e.message);
  process.exit(1);
});
