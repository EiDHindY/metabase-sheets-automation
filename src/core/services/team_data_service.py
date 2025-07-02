# src/core/services/team_data_service.py

from typing import List, Dict, Any
from src.data.csv_reader.team_member import load_team_members
from .agent_data_service import process_agent_data

def process_team_data(
        team_path: str,
        talk_time_path: str,
        dials_made_path: str,
        leads_path: str
) -> List[Dict[str,Any]]:
    """
    Load all team members and process each one’s CSV data.
    Returns a list of dicts with keys: agent_name, talk_time, dials, leads.
    """
    team_members = load_team_members(team_path)
    result: List[Dict[str,Any]] = []

    for agent in team_members:
        data = process_agent_data(agent, talk_time_path, dials_made_path, leads_path)
        result.append(data)
    
    return result