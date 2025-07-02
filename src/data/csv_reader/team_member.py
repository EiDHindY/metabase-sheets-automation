# src/data/csv_reader/team_reader.py

from typing import List
from .csv_loader import load_csv_dicts

def load_team_members(path: str) -> List[str]:
    """
    Read the team_members.csv at `path` and return a list of agent names.
    Expects a header "Agent Name".
    """
    rows = load_csv_dicts(path)
    if not rows or "Agent Name" not in rows[0]:
        raise RuntimeError(f'Missing expected column: Agent Name')
    
    # Extract the 'Agent Name' field from each row
    return [row["Agent Name"] for row in rows]