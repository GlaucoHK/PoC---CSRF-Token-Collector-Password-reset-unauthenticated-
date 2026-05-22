# Password Reset Timing Side-Channel Analysis PoC

This repository contains a simple Python Proof of Concept (PoC) script designed to identify and analyze timing side-channel vulnerabilities on user password reset endpoints.

The script targets applications that protect against traditional user enumeration by returning identical HTTP responses for both valid and invalid emails, but might still leak user existence through processing latency discrepancies (such as token generation or database lookups).

## Technical Overview

- **CSRF Token Harvesting:** Performs an initial `GET` request to establish a session and extract the `csrfmiddlewaretoken` from the form.
- **High-Precision Timing:** Uses `time.perf_counter()` to isolate and measure the exact duration of the `POST` request in milliseconds.
- **Metadata Logging:** Displays response status, round-trip time, and payload size to assist in comparative analysis.
- **Safe Iteration:** Implements a customizable delay (`time.sleep`) between requests to prevent overwhelming the target server.

## Getting Started

### Prerequisites

```bash
pip install requests


Configuration & Deployment
Open dospassword.py and configure your target staging endpoint and email list:
	url = "https://your-target-testing-environment/password_reset/"
	emails = ["valid-account@test.com", "invalid-account@test.com"]

Then execute:
	python dospassword.py