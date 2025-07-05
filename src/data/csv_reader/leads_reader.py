# src/data/csv_reader/leads_reader.py

from typing import List, Dict, Optional
from .csv_loader import load_csv_dicts

def extract_leads(path: str, agent: str) -> Optional[int]:
    """
    Read the leads CSV at `path` and return the total count
    for the given agent. Returns 0 if the agent is not present.
    """
    # Load all rows as dicts
    rows: List[Dict[str,str]] = load_csv_dicts(path)

    # Schema validation
    REQUIRED_COLUMNS = ["Sales Rep", "Count"]
    missing = [c for c in REQUIRED_COLUMNS if not rows or c not in rows[0]]
    if missing:
        raise RuntimeError(f"Missing expected columns: {missing}")
    
    # Search for exact match on 'Sales Rep'
    for row in rows:
        if row.get("Sales Rep") == agent:
            # Convert the count string to int
            return int(row["Count"])
    
    # Agent not found → zero leads/sales
    return 0