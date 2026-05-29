from openai import OpenAI
import json
import os
import time

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Set OPENAI_API_KEY before running repair_test.py")

client = OpenAI()

# LOAD CHANGESET
with open("../changesets/attempt_1.json", "r", encoding="utf-8") as f:
    changeset = json.load(f)

# ORIGINAL BROKEN TEST
original_test = """
describe('Login Test', () => {

  it('logs in successfully', () => {

    cy.visit('http://127.0.0.1:5500/app/login_modified.html')

    cy.get('#username').type('user@test.com')

    cy.get('#password').type('pass123')

    cy.get('.submit-btn').click()

  })

})
"""

# BUILD PROMPT
prompt = f"""
You are repairing a Cypress test.

Original Test:
{original_test}

DOM Changes:
{json.dumps(changeset, indent=2)}

Rules:
- preserve workflow
- preserve assertions
- use updated selectors
- avoid invalid selectors

Generate repaired Cypress test only.
"""

# START TIMER
start_time = time.perf_counter()

# CALL OPENAI
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[
        {"role": "user", "content": prompt}
    ],
    temperature=0.3
)

# END TIMER
end_time = time.perf_counter()

regen_time = end_time - start_time

# GET GENERATED TEST
generated_test = response.choices[0].message.content

# PRINT RESULT
print("\nREGENERATED TEST:\n")
print(generated_test)

print(f"\nRegeneration Time: {regen_time:.2f} seconds")

# SAVE GENERATED TEST
with open("../regenerated-tests/repaired_login.cy.js", "w", encoding="utf-8") as f:
    f.write(generated_test)
