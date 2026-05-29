from bs4 import BeautifulSoup
import json
import time

# START TIMER
start_time = time.perf_counter()

# LOAD BEFORE SNAPSHOT
with open("../snapshots/before/login_before.html", "r", encoding="utf-8") as f:
    before_html = f.read()

# LOAD AFTER SNAPSHOT
with open("../snapshots/after/login_after.html", "r", encoding="utf-8") as f:
    after_html = f.read()

# PARSE HTML
before_soup = BeautifulSoup(before_html, "lxml")
after_soup = BeautifulSoup(after_html, "lxml")

changes = []

# FIND INPUTS AND BUTTONS
before_elements = before_soup.find_all(["input", "button"])
after_elements = after_soup.find_all(["input", "button"])

# COMPARE ATTRIBUTES
for before, after in zip(before_elements, after_elements):

    before_attrs = before.attrs
    after_attrs = after.attrs

    if before_attrs != after_attrs:

        changes.append({
            "tag": before.name,
            "type": "attribute_modification",
            "before": before_attrs,
            "after": after_attrs
        })

# END TIMER
end_time = time.perf_counter()

# CALCULATE TIME
diff_ms = (end_time - start_time) * 1000

# PRINT RESULTS
print("\nDOM DIFFERENCING COMPLETE")
print(f"Total Changes: {len(changes)}")
print(f"Diff Time: {diff_ms:.2f} ms")

# SAVE CHANGESET JSON
with open("../changesets/attempt_1.json", "w", encoding="utf-8") as f:
    json.dump(changes, f, indent=4)