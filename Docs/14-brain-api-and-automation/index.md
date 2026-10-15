# 14 — BRAIN API and Automation

## 1. Learning Objectives

By completing this module, you will be able to:

- Authenticate against `https://api.worldquantbrain.com/authentication` using Python `requests`, including handling `401` Persona biometric authentication redirects.
- Submit single and multi-alpha simulations programmatically to `/simulations`, poll `Retry-After` headers, and retrieve PnL and IS test breakdowns.
- Monitor daily simulation quota headers (`X-Ratelimit-Limit`, `X-Ratelimit-Remaining`, `X-Ratelimit-Reset`) and prevent duplicate simulations using a local SHA-256 hash cache (`simulation_cache.parquet`).
- Run the **Alpha Creation Engine (ACE)** library locally while keeping all credentials strictly outside the Git repository.

## 2. Prerequisites

- [03 — WorldQuant BRAIN Fundamentals & Simulation Settings](../03-worldquant-brain-fundamentals/index.md)
- Basic Python 3 proficiency (`requests`, `pandas`, `json`, `hashlib`).

## 3. Core Concepts

### Compliance Rule for Automation

WorldQuant BRAIN's consultant operating guidelines draw a strict line between permitted and prohibited automation (`[Platform]`):

- **Permitted:** Using the official BRAIN API (`https://api.worldquantbrain.com`) and the ACE library to automate repetitive mechanics (batching multi-simulations across a curated field list, checking rate limits, deduplicating via local hash caches, downloading Data Explorer field metadata, and formatting results tables) (`[Platform]`).
- **Prohibited:** Using automation to blindly generate random Alpha ideas without economic intuition, placing excessive load on platform servers, or screen-scraping/spidering outside documented API endpoints (`[Platform]`).

### Core BRAIN API Endpoints & Headers

| Endpoint / Header | Method / Location | Purpose (`[Platform]`) |
|---|---|---|
| `https://api.worldquantbrain.com/authentication` | `POST` (Basic Auth `(email, password)`) | Establishes authenticated session and returns JWT cookies; returns `401` with `WWW-Authenticate: persona` and `Location` header when biometrics sign-in is required |
| `https://api.worldquantbrain.com/simulations` | `POST` (JSON payload) | Submits a single Alpha dict or a Multi-Simulation list of up to 10 Alpha dicts sharing the same `region` and `delay`; returns `201` with `Location` URL for progress polling |
| `<simulation_location_url>` | `GET` | Polls simulation progress; while running, response headers include `Retry-After` (seconds to sleep before next poll); when complete, returns `alpha` ID |
| `https://api.worldquantbrain.com/alphas/<alpha_id>` | `GET` | Retrieves full simulation summary (`is` stats, `is.checks`, `os` start date, settings, expression) |
| `X-Ratelimit-Limit` | Response Header | Total daily simulation quota for your account |
| `X-Ratelimit-Remaining` | Response Header | Remaining simulations available today (platform UI warns below `1,000` remaining) |
| `X-Ratelimit-Reset` | Response Header | Seconds until the daily simulation quota resets (EST timezone) |

### Multi-Simulation Throughput Limits

- **Maximum Concurrent Multi-Simulations:** Up to **8 simultaneous Multi-Simulation batches** (`[Platform]`).
- **Maximum Alphas per Multi-Simulation Batch:** Up to **10 Alphas per batch** running sequentially (`[Platform]`).
- **Batch Constraint:** All 10 Alphas inside a single Multi-Simulation batch may vary expressions, fields, universes, decay, truncation, and neutralization, **but MUST share the exact same `region` and `delay`** (`[Platform]`).
- **Quota Counting Warning:** Every child simulation in a Multi-Simulation—and every re-simulation of a duplicate Alpha on a different day—counts against your daily simulation quota (`[Platform]`).

## 4. Step-by-Step Explanations

### Step 1: Safe Authentication and Persona Biometrics Handling

Store credentials in `~/.brain_credentials` or `~/secrets/platform-brain.json` (**outside** the repository, with `chmod 600` permissions) (`[Platform]`, `[Notes]`):

```python
import json
from os.path import expanduser
from urllib.parse import urljoin
import requests

session = requests.Session()
with open(expanduser("~/.brain_credentials"), "r", encoding="utf-8") as fh:
    session.auth = tuple(json.load(fh))

response = session.post("https://api.worldquantbrain.com/authentication")

if response.status_code == requests.status_codes.codes.unauthorized:
    if response.headers.get("WWW-Authenticate") == "persona":
        persona_url = urljoin(response.url, response.headers["Location"])
        input(f"Complete Persona biometrics in browser and press Enter: {persona_url}")
        session.post(persona_url)
    else:
        raise RuntimeError("Authentication failed: check ~/.brain_credentials")
```

### Step 2: Submitting and Polling a Simulation with Rate-Limit Inspection

```python
from time import sleep

simulation_data = {
    "type": "REGULAR",
    "settings": {
        "instrumentType": "EQUITY",
        "region": "USA",
        "universe": "TOP3000",
        "delay": 1,
        "decay": 4,
        "neutralization": "SUBINDUSTRY",
        "truncation": 0.08,
        "pasteurization": "ON",
        "unitHandling": "VERIFY",
        "nanHandling": "OFF",
        "language": "FASTEXPR",
        "visualization": False,
    },
    "regular": "rank(ebitda / enterprise_value) + rank(ts_mean(-returns, 5))",
}

sim_resp = session.post("https://api.worldquantbrain.com/simulations", json=simulation_data)
print("Remaining daily quota:", sim_resp.headers.get("X-Ratelimit-Remaining"))
progress_url = sim_resp.headers["Location"]

while True:
    poll = session.get(progress_url)
    retry_after = float(poll.headers.get("Retry-After", 0))
    if retry_after == 0:
        break
    sleep(retry_after)

alpha_id = poll.json()["alpha"]
alpha_details = session.get(f"https://api.worldquantbrain.com/alphas/{alpha_id}").json()
```

### Step 3: Preventing Duplicate Simulations via a Local SHA-256 Cache

Because re-simulating an identical Alpha wastes daily quota and hides the duplicate under its original creation date on the Alphas page (`[Platform]`), hash every `simulation_data` dictionary before sending it to `/simulations` (`[Platform]`):

```python
import hashlib
import json

def hash_alpha_config(alpha_dict: dict) -> str:
    canonical = json.dumps(alpha_dict, sort_keys=True)
    return hashlib.sha256(canonical.encode("utf-8")).hexdigest()
```
Store `(alpha_hashed, alpha_id, date_created)` in a local Parquet or SQLite table (`simulation_cache.parquet`) and skip any configuration whose SHA-256 hash is already recorded (`[Platform]`).

## 5. Working Examples: Running the Local ACE Library (`Tools/api-and-automation/ace-api/`)

The repository includes the official Gold-level **Alpha Creation Engine (ACE)** toolkit in [`Tools/README.md`](../../Tools/README.md):

- `ace_lib.py` — Thread-safe `SingleSession`, `start_session()`, `generate_alpha()`, `simulate_alpha_list_multi()`, `get_datasets()`, `get_datafields()`.
- `helpful_functions.py` — `prettify_result()`, `concat_pnl()`, `concat_is_tests()`, `save_simulation_result()`.
- `SETUP_JUPYTER_ANACONDA.md` — Instructions for launching Jupyter Lab with the verified `brain-ace` Conda kernel:
  ```bash
  /opt/anaconda3/envs/brain-ace/bin/jupyter lab --notebook-dir="Tools/api-and-automation/ace-api"
  ```

## 6. Common Mistakes and Troubleshooting

- **`ModuleNotFoundError: No module named ace_lib` in Jupyter:** Always launch Jupyter with `--notebook-dir="Tools/api-and-automation/ace-api"` or `cd` into that directory first so Python resolves `ace_lib.py` and `helpful_functions.py` (`[Notes]`).
- **Mixing regions or delays inside `simulate_alpha_list_multi`:** Group your candidate list by `(region, delay)` before passing batches to Multi-Simulation (`[Platform]`).

## 7. Practical Exercises

1. Review [`Tools/README.md`](../../Tools/README.md) to see how offline analysis tools (`brain_sweep_parser.py`, `verify_index.py`) complement the live API workflow.
2. Design a Python pre-check function that verifies an expression against both `simulation_cache.parquet` and [`master_experiments_catalog.csv`](../../Analysis%20and%20Simulation%20Reports/aggregate-analytics/master_experiments_catalog.csv) before calling `/simulations`.

## 8. Related Topics and Next Steps

- **Next Module:** [15 — Alpha Harness](../15-alpha-harness/index.md)
- **Tools Documentation:** [`Tools/README.md`](../../Tools/README.md)

## 9. Sources and Verification

- **Sources:** Official BRAIN Learn *BRAIN API* (`brain-api`), *Understanding Simulation Limits* (`understanding-simulation-limits`), *How Can You Avoid Duplicate Simulations?* (`how-can-you-avoid-duplicate-simulations`), *Consultant Simulation Features* (`multi-alpha-simulation`), and *Documentation for ACE API Library [Gold]* (`[Platform]`, captured 2026-10-06/09).
- **Verification Date:** 2026-10-15.
