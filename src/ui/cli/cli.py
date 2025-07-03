# src/ui/cli/cli.py

import os 
from dotenv import load_dotenv
from datetime import datetime
from src.core.services.team_data_service import process_team_data
from typing import Dict, Any


def prompt_user(record: Dict[str, Any]):
    agent = record["agent_name"]
    print(f"\n Agent: {agent}")
    print(f" • Talk Time: {record["talk_time"]} mins")
    print(f" • Dials Made: {record['dials']}")

    # 1) Date is always today
    date_str: str = datetime.now().strftime("%d/%m/%Y")
    print(f"Date: {date_str}")

    # 2) Attendance choice
    attendance: str = ""
    while attendance not in ("1", "2", "3"):
        attendance = input(f"Attendance for {agent} (1=Office, 2=Home, 3=UPL)").strip()
    attendance_map: Dict[str,str] = {"1":"Office", "2":"Home", "3":"UPL"}

    # 3) Leads: if extracted >0, show and allow override; if CSV missing, prompt fresh
    default_leads: int = record.get('leads', 0)
    if default_leads:
        entry: str = input(f"Leads (found {default_leads}; press Enter to keep or type new number): ").strip()
        leads: int = int(entry) if entry else default_leads
    else:
        leads: int = int(input(f"Leads for {agent}, (enter number): ").strip())
    
        # 4) Notes
    notes: str = input(f"any notes for {agent}? Press enter to skip").strip()
    if not notes: notes = ''

    # Merge all fields
    merged: Dict[str, Any] = {
        **record,
        "date": date_str,
        "attendance":attendance_map[attendance],
        "leads": leads,
        "notes": notes
    }
    return merged

def main():
    load_dotenv()
    leads_dir = os.getenv("LEADS_DIR")
    talk_dir  = os.getenv('TALK_TIME_DIR')
    dials_dir = os.getenv('DIALS_DIR')
    team_dir  = os.getenv('TEAM_DIR')

    assert leads_dir and talk_dir and dials_dir and team_dir
    team_data = process_team_data(team_dir, talk_dir, dials_dir, leads_dir)

    for rec in team_data:
        filled = prompt_user(rec)
    
    print(f"\nall agents are processed")
