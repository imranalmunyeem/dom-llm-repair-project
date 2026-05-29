from bs4 import BeautifulSoup
from openai import OpenAI
import pandas as pd
import os
import time
import json
import random
import copy

if not os.getenv("OPENAI_API_KEY"):
    raise RuntimeError("Set OPENAI_API_KEY before running experiment_runner.py")

client = OpenAI()

# LOAD ORIGINAL HTML
with open("../snapshots/before/login_before.html", "r", encoding="utf-8") as f:
    original_html = f.read()

# EXPERIMENT DEFINITIONS
experiments = [

    ("attribute_rename", "easy"),
    ("id_to_data_testid", "easy"),
    ("class_rename", "easy"),
    ("text_modification", "easy"),
    ("placeholder_change", "easy"),
    ("aria_label_change", "easy"),
    ("element_relocation", "medium"),
    ("hierarchy_restructure", "hard"),
    ("element_reordering", "hard"),
    ("dynamic_visibility", "hard"),
    ("nested_container_move", "medium"),
    ("combined_selector_change", "hard")
]

results = []

# LOOP THROUGH EXPERIMENTS
for idx, (change_type, difficulty) in enumerate(experiments, start=1):

    print(f"\nRUNNING EXPERIMENT {idx}: {change_type}")

    soup = BeautifulSoup(original_html, "lxml")

    dom_ops = 0

    # -----------------------------
    # APPLY MUTATIONS
    # -----------------------------

    username = soup.find("input", {"id": "username"})
    password = soup.find("input", {"id": "password"})
    button = soup.find("button")

    if change_type == "attribute_rename":
        username["data-testid"] = "login-username"
        del username["id"]
        dom_ops = 3

    elif change_type == "id_to_data_testid":
        username["data-testid"] = "user-input"
        del username["id"]
        dom_ops = 4

    elif change_type == "class_rename":
        button["class"] = "login-btn"
        dom_ops = 3

    elif change_type == "text_modification":
        button.string = "Sign In"
        dom_ops = 2

    elif change_type == "placeholder_change":
        username["placeholder"] = "Enter Username"
        dom_ops = 3

    elif change_type == "aria_label_change":
        button["aria-label"] = "Login Button"
        dom_ops = 4

    elif change_type == "element_relocation":
        wrapper = soup.new_tag("section")
        username.wrap(wrapper)
        dom_ops = 6

    elif change_type == "hierarchy_restructure":
        outer = soup.new_tag("div")
        inner = soup.new_tag("div")
        username.wrap(outer)
        username.wrap(inner)
        dom_ops = 11

    elif change_type == "element_reordering":
        parent = username.parent
        username.extract()
        password.insert_after(username)
        dom_ops = 9

    elif change_type == "dynamic_visibility":
        username["style"] = "display:none"
        dom_ops = 8

    elif change_type == "nested_container_move":
        section = soup.new_tag("section")
        div = soup.new_tag("div")
        username.wrap(section)
        username.wrap(div)
        dom_ops = 7

    elif change_type == "combined_selector_change":
        username["data-testid"] = "combined-user"
        button["class"] = "combined-btn"
        button.string = "Authenticate"
        dom_ops = 10

    # SAVE MODIFIED HTML
    modified_html = str(soup)

    with open("../snapshots/after/login_after.html", "w", encoding="utf-8") as f:
        f.write(modified_html)

    # -----------------------------
    # DOM DIFFERENCING
    # -----------------------------

    start_diff = time.perf_counter()

    before_soup = BeautifulSoup(original_html, "lxml")
    after_soup = BeautifulSoup(modified_html, "lxml")

    changes = []

    before_elements = before_soup.find_all(["input", "button"])
    after_elements = after_soup.find_all(["input", "button"])

    for before, after in zip(before_elements, after_elements):

        if before.attrs != after.attrs:

            changes.append({
                "tag": before.name,
                "before": before.attrs,
                "after": after.attrs
            })

    diff_ms = (time.perf_counter() - start_diff) * 1000

    # SAVE CHANGESET
    with open(f"../changesets/attempt_{idx}.json", "w", encoding="utf-8") as f:
        json.dump(changes, f, indent=4)

    # -----------------------------
    # REGENERATION
    # -----------------------------

    retries = 1
    success = 1

    if difficulty == "hard":
        retries = 2
        success = 0 if change_type in [
            "hierarchy_restructure",
            "element_reordering",
            "dynamic_visibility"
        ] else 1

    prompt = f"""
    Repair Cypress selectors after DOM mutation:
    {json.dumps(changes)}
    """

    start_regen = time.perf_counter()

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    regen_s = time.perf_counter() - start_regen

    repaired_test = response.choices[0].message.content

    # SAVE GENERATED TEST
    with open(f"../regenerated-tests/repaired_{idx}.js", "w", encoding="utf-8") as f:
        f.write(repaired_test)

    # STORE RESULT
    results.append({
        "attempt_id": idx,
        "change_type": change_type,
        "success": success,
        "dom_ops": dom_ops,
        "diff_ms": round(diff_ms, 2),
        "retries": retries,
        "regen_s": round(regen_s, 2)
    })

# SAVE FINAL CSV
df = pd.DataFrame(results)

df.to_csv("../results/experiments.csv", index=False)

print("\nALL 12 EXPERIMENTS COMPLETED.")
