To repair Cypress selectors after the DOM mutation where a `<button>` changes its class from `"submit-btn"` to `"login-btn"`, you need to update your Cypress test selectors accordingly.

### Before DOM change:
```js
cy.get('button.submit-btn').click();
```

### After DOM change:
```js
cy.get('button.login-btn').click();
```

---

### General approach to repair selectors:

If you have multiple selectors affected by this change, update all instances where the old class `.submit-btn` is used to `.login-btn`.

---

### Example:

**Old test code:**
```js
cy.get('button.submit-btn').should('be.visible').click();
```

**Updated test code:**
```js
cy.get('button.login-btn').should('be.visible').click();
```

---

### Optional: Use data attributes for more stable selectors

To avoid frequent selector breakage due to class changes, consider adding a `data-cy` or similar attribute to your elements:

```html
<button class="login-btn" data-cy="login-button">Login</button>
```

Then in Cypress:

```js
cy.get('[data-cy=login-button]').click();
```

This approach makes your tests more resilient to CSS class changes.

---

If you want me to help update your full test code, please share it!