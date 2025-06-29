# Detection Engineering

![GitHub Actions Flow](./assets/github_actions_flow.png)

> A modern, GitHub Actions–driven framework for managing and automating detection rules using TOML, with native integration into Elastic and automated validation pipelines.

---

## Overview

Detection Engineering is an automation-first approach to maintaining detection logic. It is designed for teams or individuals who want to:

- Build and validate detection rules in TOML
- Automatically push validated alerts to Elastic
- Generate metrics and ATT&CK Navigator layers
- Enforce consistent rule structure and CI/CD quality gates

This project uses **GitHub Actions** for continuous integration and deployment of detection content, built around the following core workflows:

---

## GitHub Actions Workflow

This repo uses GitHub Actions to automate:

- **Elastic Automation** – Push modified alerts directly into Elastic Security
- **TOML Validation** – Validate against required fields and MITRE ATT&CK accuracy
- **Metrics Automation** – Generate CSVs and MITRE Navigator JSONs from TOML

See the diagram above for full flow.

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
