```javascript
describe('Login Test', () => {

  it('logs in successfully', () => {

    cy.visit('http://127.0.0.1:5500/app/login_modified.html')

    cy.get('[data-testid="login-username"]').type('user@test.com')

    cy.get('input[name="user-password"]').type('pass123')

    cy.get('button[aria-label="Sign in"]').click()

  })

})
```