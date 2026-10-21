# Cirqllabs Pipeline Quality

A dependency-free Python utility for the Cirqllabs Python Developer Intern application. It validates API and data-pipeline event batches before they are loaded into downstream storage.

The checker catches missing schema fields, duplicate event IDs, out-of-order timestamps, and empty payloads. It prints a JSON summary by source and exits non-zero when a batch is unsafe to load, so it can run inside a small CI or ingestion job.

## Run

```bash
python3 pipeline_check.py events.json
python3 -m unittest -v
```
