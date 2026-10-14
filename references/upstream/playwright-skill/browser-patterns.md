> Curated from [playwright-skill](https://github.com/lackeyjb/playwright-skill/blob/dd47a6a023e249eb1b36e9e943eab89d0900865d/skills/playwright-skill/API_REFERENCE.md), revision `dd47a6a023e2`. MIT; notice in [LICENSE](LICENSE).
> Reference material only: the presentation-builder workflow and user brief take precedence. Upstream tools, CDN examples, optional links, and website-specific rules are not prerequisites.
> Presentation adaptation: Examples use JavaScript Playwright; the bundled Python runner needs no Node dependency. Author assertions for the actual widgets.

## Selectors & Locators

### Best Practices for Selectors

```javascript
// PREFERRED: Data attributes (most stable)
await page.locator('[data-testid="submit-button"]').click();
await page.locator('[data-cy="user-input"]').fill('text');

// GOOD: Role-based selectors (accessible)
await page.getByRole('button', { name: 'Submit' }).click();
await page.getByRole('textbox', { name: 'Email' }).fill('user@example.com');
await page.getByRole('heading', { level: 1 }).click();

// GOOD: Text content (for unique text)
await page.getByText('Sign in').click();
await page.getByText(/welcome back/i).click();

// OK: Semantic HTML
await page.locator('button[type="submit"]').click();
await page.locator('input[name="email"]').fill('test@test.com');

// AVOID: Classes and IDs (can change frequently)
await page.locator('.btn-primary').click();  // Avoid
await page.locator('#submit').click();       // Avoid

// LAST RESORT: Complex CSS/XPath
await page.locator('div.container > form > button').click();  // Fragile
```

### Advanced Locator Patterns

```javascript
// Filter and chain locators
const row = page.locator('tr').filter({ hasText: 'John Doe' });
await row.locator('button').click();

// Nth element
await page.locator('button').nth(2).click();

// Combining conditions
await page.locator('button').and(page.locator('[disabled]')).count();

// Parent/child navigation
const cell = page.locator('td').filter({ hasText: 'Active' });
const row = cell.locator('..');
await row.locator('button.edit').click();
```

## Common Actions

### Form Interactions

```javascript
// Text input
await page.getByLabel('Email').fill('user@example.com');
await page.getByPlaceholder('Enter your name').fill('John Doe');

// Clear and type
await page.locator('#username').clear();
await page.locator('#username').type('newuser', { delay: 100 });

// Checkbox
await page.getByLabel('I agree').check();
await page.getByLabel('Subscribe').uncheck();

// Radio button
await page.getByLabel('Option 2').check();

// Select dropdown
await page.selectOption('select#country', 'usa');
await page.selectOption('select#country', { label: 'United States' });
await page.selectOption('select#country', { index: 2 });

// Multi-select
await page.selectOption('select#colors', ['red', 'blue', 'green']);

// File upload
await page.setInputFiles('input[type="file"]', 'path/to/file.pdf');
await page.setInputFiles('input[type="file"]', [
  'file1.pdf',
  'file2.pdf'
]);
```

### Mouse Actions

```javascript
// Click variations
await page.click('button');                          // Left click
await page.click('button', { button: 'right' });    // Right click
await page.dblclick('button');                       // Double click
await page.click('button', { position: { x: 10, y: 10 } });  // Click at position

// Hover
await page.hover('.menu-item');

// Drag and drop
await page.dragAndDrop('#source', '#target');

// Manual drag
await page.locator('#source').hover();
await page.mouse.down();
await page.locator('#target').hover();
await page.mouse.up();
```

### Keyboard Actions

```javascript
// Type with delay
await page.keyboard.type('Hello World', { delay: 100 });

// Key combinations
await page.keyboard.press('Control+A');
await page.keyboard.press('Control+C');
await page.keyboard.press('Control+V');

// Special keys
await page.keyboard.press('Enter');
await page.keyboard.press('Tab');
await page.keyboard.press('Escape');
await page.keyboard.press('ArrowDown');
```

## Waiting Strategies

### Smart Waiting

```javascript
// Wait for element states
await page.locator('button').waitFor({ state: 'visible' });
await page.locator('.spinner').waitFor({ state: 'hidden' });
await page.locator('button').waitFor({ state: 'attached' });
await page.locator('button').waitFor({ state: 'detached' });

// Wait for specific conditions
await page.waitForURL('**/success');
await page.waitForURL(url => url.pathname === '/dashboard');

// Prefer a user-visible assertion over network-idle heuristics.
await page.getByRole('heading', { name: 'Dashboard' }).waitFor();
await page.waitForLoadState('domcontentloaded');

// Wait for function
await page.waitForFunction(() => document.querySelector('.loaded'));
await page.waitForFunction(
  text => document.body.innerText.includes(text),
  'Content loaded'
);

// Wait for response
const responsePromise = page.waitForResponse('**/api/users');
await page.click('button#load-users');
const response = await responsePromise;

// Wait for request
await page.waitForRequest(request =>
  request.url().includes('/api/') && request.method() === 'POST'
);

// Custom timeout
await page.locator('.slow-element').waitFor({
  state: 'visible',
  timeout: 10000  // 10 seconds
});
```

## Visual Testing

### Screenshots

```javascript
// Full page screenshot
await page.screenshot({
  path: 'screenshot.png',
  fullPage: true
});

// Element screenshot
await page.locator('.chart').screenshot({
  path: 'chart.png'
});

// Visual comparison
await expect(page).toHaveScreenshot('homepage.png');
```

## Mobile Testing

```javascript
// Device emulation
const { devices } = require('playwright');
const iPhone = devices['iPhone 12'];

const context = await browser.newContext({
  ...iPhone,
  locale: 'en-US',
  permissions: ['geolocation'],
  geolocation: { latitude: 37.7749, longitude: -122.4194 }
});
```

## Best Practices

1. **Test Organization** - Use descriptive test names, group related tests
2. **Selector Strategy** - Prefer data-testid attributes, use role-based selectors
3. **Waiting** - Use Playwright's auto-waiting, avoid hard-coded delays
4. **Error Handling** - Add proper error messages, take screenshots on failure
5. **Performance** - Run tests in parallel, reuse authentication state
