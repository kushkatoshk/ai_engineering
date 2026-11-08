"""Build the validated ticket dataset: download, map, validate, write.

Run from the repo root with: make data
"""

from pathlib import Path

import pandas as pd
from pydantic import ValidationError

from support_copilot.data.contract import SupportTicket
from support_copilot.data.taxonomy import GUIDELINE_VERSION

BITEXT_DATASET = "bitext/Bitext-customer-support-llm-chatbot-training-dataset"

RAW_PATH = Path("data/raw/bitext.parquet")
PROCESSED_PATH = Path("data/processed/tickets.parquet")
QUARANTINE_PATH = Path("data/quarantine/bitext_failures.csv")

MAX_FAILURE_RATE = 0.01  # above this, something upstream broke: stop


def download_bitext(path: Path = RAW_PATH) -> pd.DataFrame:
    """Download Bitext once and cache it in data/raw. Never edit that file."""
    if path.exists():
        print(f"Using cached raw data: {path}")
        return pd.read_parquet(path)

    from datasets import load_dataset  # slow import, so only when needed

    print(f"Downloading {BITEXT_DATASET} ...")
    raw = load_dataset(BITEXT_DATASET, split="train").to_pandas()
    path.parent.mkdir(parents=True, exist_ok=True)
    raw.to_parquet(path, index=False)
    return raw


def to_contract_rows(raw: pd.DataFrame) -> list[dict]:
    """Map Bitext's columns onto the contract's fields and add provenance."""
    return [
        {
            "ticket_id": f"bitext-{i:05d}",
            "text": row["instruction"],
            "intent": row["intent"],
            "source": "bitext",
            "label_source": "bitext",
            "guideline_version": GUIDELINE_VERSION,
        }
        for i, row in enumerate(raw.to_dict("records"))
    ]


def validate(rows: list[dict]) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Split rows into those that pass the contract and those that fail."""
    passed, failed = [], []
    for row in rows:
        try:
            passed.append(SupportTicket.model_validate(row).model_dump())
        except ValidationError as exc:
            reasons = "; ".join(f"{e['loc'][0]}: {e['msg']}" for e in exc.errors())
            failed.append({**row, "errors": reasons})
    return pd.DataFrame(passed), pd.DataFrame(failed)


def main() -> None:
    raw = download_bitext()
    rows = to_contract_rows(raw)
    passed, failed = validate(rows)

    failure_rate = len(failed) / len(rows)
    print(
        f"Rows in: {len(rows):,}   passed: {len(passed):,}   "
        f"quarantined: {len(failed):,} ({failure_rate:.2%})"
    )

    if len(failed):
        QUARANTINE_PATH.parent.mkdir(parents=True, exist_ok=True)
        failed.to_csv(QUARANTINE_PATH, index=False)
        print(f"Failures written to {QUARANTINE_PATH}")
    elif QUARANTINE_PATH.exists():
        QUARANTINE_PATH.unlink()  # don't leave stale failures from an old run

    if failure_rate > MAX_FAILURE_RATE:
        PROCESSED_PATH.unlink(missing_ok=True)  # fail closed: no stale data left behind
        raise SystemExit(
            f"Failure rate {failure_rate:.2%} is above {MAX_FAILURE_RATE:.0%}. "
            f"Processed data was not written. Check {QUARANTINE_PATH}."
        )

    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)
    passed.to_parquet(PROCESSED_PATH, index=False)
    print(f"Wrote {PROCESSED_PATH}\n")
    print("Rows per intent:")
    print(passed["intent"].value_counts().to_string())


if __name__ == "__main__":
    main()
