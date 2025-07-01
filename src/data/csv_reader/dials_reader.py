# src/data/csv_reader/dials_reader.py

from typing import List, Dict
from .csv_loader import load_csv_dicts

def extract_dials(path: str, agent: str) -> int:
    """
    Read the dials-made CSV at `path` and return the total number
    of distinct 'Started At' values for `agent`. Returns 0 if none.
    """
    # Load all rows as dicts
    rows: List[Dict[str,str]] = load_csv_dicts(path)

    # Schema validation
    REQUIRED_COLUMNS = ["User Name", "Distinct values of Started At"]
    missing = [c for c in REQUIRED_COLUMNS if not rows or c not in rows[0]]
    if missing:
        raise RuntimeError(f"Missing expected columns: {missing}")

    # Search for exact match on 'User Name'
    for row in rows:
        if row.get("User Name") == agent:
            # Convert the distinct-count string to int
            return int(row["Distinct values of Started At"])

    # Agent not found → zero dials made
    return 0
