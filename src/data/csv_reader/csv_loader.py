# src/data/csv_reader/csv_loader.py

import os, csv
from typing import List, Dict


def load_csv_dicts(path:str) -> List[Dict[str,str]]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"CSV file not found:{path}")
    with open(path, newline='', encoding='utf-8') as f:
        return list(csv.DictReader(f))
