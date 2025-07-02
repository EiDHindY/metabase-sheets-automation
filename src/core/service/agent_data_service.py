# src/core/services/agent_data_service.py

from typing import Dict, Any
from src.data.csv_reader.talk_time_reader import extract_talk_time
from src.data.csv_reader.dials_reader import extract_dials
from src.data.csv_reader.leads_reader import extract_leads

def process_agent_data(
        agent_name: str,
        talk_time_path: str,
        dials_made_path: str,
        leads_path: str) -> Dict[str,Any]:
    """
    Process all CSV data for a single agent and return the extracted metrics.
    Attendance status will be determined by user input, not automated logic.
    
    Args:
        agent_name: Name of the agent to process
        talk_time_path: Path to the talk-time CSV file
        dials_path: Path to the dials-made CSV file  
        leads_path: Path to the leads CSV file
    
    Returns:
        Dictionary containing all agent data (no attendance determination)
    """
    # Extract data from all three CSV files
    talk_time: float = extract_talk_time(talk_time_path, agent_name)
    dials: int = extract_dials(dials_made_path, agent_name)
    leads: int = extract_leads(leads_path, agent_name)

    return{
        "agnet_name":agent_name,
        "talk_time": talk_time,
        "dials":dials,
        "leads":leads
    }