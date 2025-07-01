# src/data/csv_reader/talk_time_reader.py

from typing import List, Dict
from .csv_loader import load_csv_dicts

def extract_talk_time(path: str, agent: str) -> float:
    """
    Return total talk time in minutes for `agent`.
    Raises RuntimeError if required columns are missing.
    Returns None if the agent is not present in the CSV.
    """
    # Load all rows as dicts
    rows: List[Dict[str,str]] = load_csv_dicts(path)

    # Schema validation: ensure required columns exist
    REQUIRED_COLUMNS = ["User Name", "Sum of Duration in Minutes"]
    missing = [c for c in REQUIRED_COLUMNS if not rows or c not in rows[0]]
    if missing:
        raise RuntimeError(f"Missing expected columns: {missing}")
    
    # Search for exact match on 'User Name'
    for row in rows:
        if row.get("User Name") == agent:
            return float(row["Sum of Duration in Minutes"])
    
    # Agent not found → no talk time recorded
    return 0.0