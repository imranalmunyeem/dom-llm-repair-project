# DOM LLM Repair Project

This repository contains a small experimental pipeline for repairing Cypress end-to-end tests after DOM changes. The example application is a static login page. The experiment mutates the DOM, detects selector-relevant changes, asks an LLM to regenerate Cypress selectors, records timing and success metrics, and generates charts for reporting.

## Tools Used

The project uses the following tools and libraries:

- Node.js and npm for the JavaScript/Cypress toolchain.
- Cypress 15.15.0 for browser-based end-to-end testing.
- Python 3 for the DOM-differencing, repair, experiment, statistics, and chart scripts.
- Beautiful Soup 4 and lxml for HTML parsing and DOM comparison.
- OpenAI Python SDK with `gpt-4.1-mini` for Cypress test repair generation.
- pandas for experiment result tables.
- matplotlib for chart generation.
- Git and GitHub for version control and publishing.
- A local static web server, such as `python -m http.server`, to serve the HTML files at `http://127.0.0.1:5500`.

## Project Structure

```text
app/
  login.html                 Original login page.
  login_modified.html        Modified login page that breaks the original selectors.

cypress/e2e/
  login.cy.js                Original Cypress test that targets the modified page.

snapshots/
  before/login_before.html   Baseline DOM snapshot.
  after/login_after.html     Mutated DOM snapshot used by the experiment.

scripts/
  dom_diff.py                Compares before/after DOM snapshots and writes a changeset.
  repair_test.py             Sends one changeset to the LLM and writes a repaired Cypress test.
  experiment_runner.py       Runs the 12 DOM mutation experiments.
  final_stats.py             Prints summary statistics from the experiment CSV.
  chart_generator.py         Generates PNG charts from the experiment CSV.

changesets/
  attempt_*.json             DOM change records for each experiment attempt.

regenerated-tests/
  repaired_*.js              LLM-generated repaired tests for each attempt.

results/
  experiments.csv            Main experiment result table.
  timing_results.csv         Timing data from the single repair example.
  retry_logs.txt             Retry notes for the single repair example.

charts/
  *.png                      Generated charts for success rate, change distribution, and repair time.

paper-results/
  *.png                      Evidence and presentation images for paper/report usage.
```

## Stored Result Summary

The committed `results/experiments.csv` contains 12 DOM mutation experiments:

- Total experiments: 12
- Successful repairs: 9
- Failed repairs: 3
- Success rate: 75.0%
- Mean DOM diff time: 1.94 ms
- Mean regeneration time: 4.62 s
- Failed hard cases: `hierarchy_restructure`, `element_reordering`, and `dynamic_visibility`

The chart outputs are available in `charts/`:

- `charts/success_rate.png`
- `charts/change_distribution.png`
- `charts/maintenance_effort.png`

## Prerequisites

Install these before reproducing the project:

- Node.js 22 or newer
- npm
- Python 3.10 or newer
- Git
- An OpenAI API key for the LLM regeneration steps

Set the API key as an environment variable. On PowerShell:

```powershell
$env:OPENAI_API_KEY="your_api_key_here"
```

On macOS or Linux:

```bash
export OPENAI_API_KEY="your_api_key_here"
```

Do not commit API keys to the repository.

## Setup

Clone the repository and install dependencies:

```bash
git clone https://github.com/imranalmunyeem/dom-llm-repair-project.git
cd dom-llm-repair-project
npm install
python -m venv venv
```

Activate the Python virtual environment.

PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

macOS or Linux:

```bash
source venv/bin/activate
```

Install Python packages:

```bash
pip install -r requirements.txt
```

## Run the Cypress Baseline

The Cypress spec visits `http://127.0.0.1:5500/app/login_modified.html`, so start a static server from the repository root:

```bash
python -m http.server 5500
```

In a second terminal, run Cypress:

```bash
npx cypress run --spec cypress/e2e/login.cy.js
```

The original test uses selectors from the old DOM (`#username`, `#password`, and `.submit-btn`) while `app/login_modified.html` uses changed attributes. That mismatch is the repair problem this project studies.

## Reproduce the Single DOM-Diff and Repair Example

Run scripts from the `scripts/` directory because the scripts use paths relative to that folder.

```bash
cd scripts
python dom_diff.py
python repair_test.py
cd ..
```

Expected outputs:

- `changesets/attempt_1.json`
- `regenerated-tests/repaired_login.cy.js`
- Console output showing DOM-diff timing and LLM regeneration time

## Reproduce the 12-Experiment Result

Run the full experiment:

```bash
cd scripts
python experiment_runner.py
cd ..
```

This regenerates:

- `changesets/attempt_1.json` through `changesets/attempt_12.json`
- `regenerated-tests/repaired_1.js` through `regenerated-tests/repaired_12.js`
- `results/experiments.csv`
- `snapshots/after/login_after.html`

The experiment covers these DOM mutation types:

1. `attribute_rename`
2. `id_to_data_testid`
3. `class_rename`
4. `text_modification`
5. `placeholder_change`
6. `aria_label_change`
7. `element_relocation`
8. `hierarchy_restructure`
9. `element_reordering`
10. `dynamic_visibility`
11. `nested_container_move`
12. `combined_selector_change`

Because LLM calls are nondeterministic and depend on API latency, regenerated test content and `regen_s` values may vary slightly between runs.

## Generate Statistics and Charts

After `results/experiments.csv` exists, print the final statistics:

```bash
cd scripts
python final_stats.py
cd ..
```

Generate charts:

```bash
cd scripts
python chart_generator.py
cd ..
```

Expected chart outputs:

- `charts/success_rate.png`
- `charts/change_distribution.png`
- `charts/maintenance_effort.png`

## Method Overview

The repair pipeline follows this sequence:

1. Capture or provide the original DOM snapshot in `snapshots/before/login_before.html`.
2. Apply a DOM mutation and save the changed snapshot in `snapshots/after/login_after.html`.
3. Parse both snapshots with Beautiful Soup and lxml.
4. Compare key interactive elements, currently `input` and `button` elements.
5. Save selector-relevant attribute changes as JSON changesets.
6. Prompt `gpt-4.1-mini` with the original Cypress test and DOM changes.
7. Save the regenerated Cypress test.
8. Record success, DOM operation count, DOM-diff timing, retry count, and LLM regeneration time.
9. Summarize the results with pandas and visualize them with matplotlib.

## Notes for Reproduction

- The scripts intentionally use simple relative paths, so run them from `scripts/`.
- `experiment_runner.py` overwrites files in `changesets/`, `regenerated-tests/`, `results/experiments.csv`, and `snapshots/after/`.
- `repair_test.py` and `experiment_runner.py` require `OPENAI_API_KEY`.
- The committed `node_modules/` directory exists in this repository, but `npm install` is still the preferred reproducible setup step.
- If a generated Cypress file contains Markdown code fences from the LLM response, remove the fences before using it directly as a Cypress spec.
