# Detection Engineering Home Lab

> A personal detection engineering lab and validation framework built with GitHub Actions, designed to help develop and test detection logic in a realistic environment.

---

## Overview

This project is a home lab I built to sharpen my detection engineering skills. It focuses on building, validating, and managing detection rules in a structured way, while integrating automation through GitHub Actions. While it's not intended as a plug-and-play solution for production environments, it does demonstrate how automation, consistency, and threat-informed development practices can be applied to detection engineering workflows.

With this setup, I can:

- Create and manage detection rules in TOML format
- Validate rules for required fields and MITRE ATT&CK accuracy
- Push updates directly into my Elastic Security instance
- Generate metrics, detection timelines, and ATT&CK Navigator heatmaps
- Experiment with CI/CD techniques in a security content context

This project uses **GitHub Actions** to simulate a full detection engineering pipeline, modeled after what a small team or solo practitioner might use in a real-world environment.

---

## GitHub Actions Workflow

GitHub Actions power the automation for:

- **Elastic Automation** – Push updated or new alerts to an Elastic Security instance
- **TOML Validation** – Enforce rule consistency and verify MITRE mappings
- **Metrics Generation** – Export CSVs, Markdown summaries, and ATT&CK Navigator layers from detection content

See the diagram below for a visual walkthrough of the full pipeline.

![GitHub Actions Flow](./assets/github_actions_flow.png)

---

## Script Descriptions

### `mitre.py`

> **Purpose:** Validates detection rules against the MITRE ATT&CK framework  
> Checks:

- MITRE tactic names
- Technique and subtechnique IDs and names
- Deprecation status

### `update_alert.py`

> **Purpose:** Pushes updated TOML alerts to Elastic  
> Uses:

- Environment variable `CHANGED_FILES`
- Converts TOML → JSON and uses PUT or POST depending on rule ID presence

### `toml_to_json.py`

> **Purpose:** Full sync of all TOML detection rules into Elastic  
> Uploads all TOML alerts in the `/detections` directory to the Elastic Detection Engine.

### `validation.py`

> **Purpose:** Field validation for TOML alerts  
> Checks:

- Presence of required fields based on `required_fields.toml`
- Ensures `metadata.creation_date` is defined

---

## Workflows

| Workflow File                   | Trigger               | Description                                  |
| ------------------------------- | --------------------- | -------------------------------------------- |
| `all_detections_to_elastic.yml` | Manual / On push      | Push all TOML alerts to Elastic              |
| `elastic_sync.yml`              | On file change (TOML) | Sync only changed TOML files to Elastic      |
| `toml_mitre_validation.yml`     | On PR / push          | Validate MITRE tactics, techniques, subtechs |

---

## Tracking Metrics

![Tracking Metrics](/assets/tracking_metrics.png)

This repository includes automated tooling to extract and visualize detection rule coverage and metadata from TOML-based alert definitions.

Three core outputs are generated from the `detections/` directory:

### CSV Export

**Script:** `toml_to_csv.py`  
Generates a CSV table of all detection alerts with the following fields:

- Name
- Date Created
- Author(s)
- Risk Score
- Severity
- MITRE Tactic, Technique, and Subtechnique(s)

**Output:** `metrics/detectiondata.csv`

Useful for audits, tracking changes over time, or importing into BI dashboards.

---

### Markdown Report

**Script:** `toml_to_md.py`  
Builds a rolling detection engineering changelog/report for the last 3 months.

**Output:** `metrics/recentdetections.md`

The report includes:

- Month-over-month summary of new alerts
- Tabular view of each alert's metadata

This can be used directly in GitHub Wikis or emailed to detection engineering stakeholders.

---

### MITRE Navigator JSON

**Script:** `toml_to_navigator.py`  
Creates a **MITRE ATT&CK Navigator layer** file that visualizes alert coverage across techniques.

**Output:** `metrics/navigator.json`

Upload to: [https://mitre-attack.github.io/attack-navigator/](https://mitre-attack.github.io/attack-navigator/)

> Each detection increases the "score" of a technique/subtechnique to reflect alert density.

---

---

## Elastic API Key Configuration

To store your Elastic API key securely:

1. Create a `.env` or `config.py` file and store your secrets (e.g., `API_KEY`)
2. Add that file to `.gitignore`:

   ```
   .env
   config.py
   ```

3. Load secrets using `os.environ` or similar at runtime

---

## Future Improvements

- Add enrichment with CTI context (e.g., threat actors, campaigns)
- Introduce coverage mapping vs. Sigma / ATT&CK matrix
- Continuous deployment into Elastic via CI/CD

---
