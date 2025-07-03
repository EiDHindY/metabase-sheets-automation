# src/data/file_manager/file_manager.py


import os, shutil
from datetime import datetime
from typing import Optional, List, Dict, Any
from src.core.services.team_data_service import process_team_data

def _get_single_file(dir_path: str) -> Optional[str]:
    """
    Return the first (and only) CSV filepath in dir_path,
    or None if the directory is empty.
    Raises an error if more than one file is present.
    """
    files: List[str] = [f for f in os.listdir(dir_path) if f.lower().endswith('csv')]
    if not files:
        return None
    if len(files) > 1:
        raise RuntimeError(f"Multible CSVs in{dir_path}: {files}")
    return os.path.join(dir_path, files[0])

def process_daily_files(
        leads_dir: str,
        talk_time_dir: str,
        dials_made_dir: str,
        team_members_dir: str
) -> List[Dict[str, Any]]:
    """
    Finds the single CSV in each input directory, processes
    all team members, archives the files, and returns the results.
    """
    # 1. Locate files
    leads_file: Optional[str] = _get_single_file(leads_dir)
    talk_time_file: Optional[str] = _get_single_file(talk_time_dir)
    dials_made_file: Optional[str] = _get_single_file(dials_made_dir)
    team_members_file: Optional[str] = _get_single_file(team_members_dir)

    # 2. Ensure all files are present
    missing:List[str] = []
    if not talk_time_file: missing.append("talk time")
    if not dials_made_file: missing.append("dials-made")
    if not team_members_file: missing.append("team members")
    if missing:
        raise FileNotFoundError(f"Missing required CSVs: {missing}")

    assert team_members_file and talk_time_file and dials_made_file and leads_file # just to silence pylance type checking
    # 3. Process team data
    result: List[Dict[str, Any]] = process_team_data(
        team_members_file,
        talk_time_file,
        dials_made_file,
        leads_file
    )

    # 4. Archive processed files
    today: str = datetime.now().strftime("%Y-%m-%d")
    archived_dir = os.path.join("raw-data", "processed", today)
    for path in (talk_time_file, leads_file, dials_made_file):
        shutil.move(path, archived_dir)
    
    return result