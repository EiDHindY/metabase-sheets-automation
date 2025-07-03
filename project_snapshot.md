<!-- set up -->
1- created a remote repo on github with the name (metabase-sheets-automation)
2- cloned the repo that comes with .gitignore for python and README.md
3- created a venv 
4- pushed to the main branch on github as the initial commit
5- downloaded some dependencies will be found in the rquirements.txt

<!-- current file layout -->
📁 metabase-sheets-automation
  ├── 📁service_account
  │   └── service_account.json
  ├── 📁config 
  │   └── __init__.py
  ├── 📁src 
  │   ├── 📁ui/
  |   │   ├── 📁cli/
  |   │   │    ├── cli.py
  │   ├── 📁data/
  |   │   ├── 📁csv_reader/
  |   │   │    ├── csv_loader.py
  |   │   │    ├── talk_time_reader.py
  |   │   │    ├── dials_reader.py
  |   │   │    ├── leads_reader.py
  |   │   │    ├── team_member.py
  |   |   │    └── __init__.py
  |   │   ├── 📁file_manager/
  |   │   │    ├── file_manager.py
  |   |   │    └── __init__.py
  |   │   └── __init__.py
  │   ├── 📁core/
  |   │   ├── 📁services/
  |   │   │    ├── agent_data_service.py
  |   |   │    └── __init__.py
  │   └── __init__.py
  ├── 📁raw-data/
  │   ├── 📁input/
  │   │   ├── 📁leads/
  │   │   ├── 📁talk-time/
  │   │   └── 📁dials-made/
  │   ├── 📁processed/
  │   └── 📁team/
  ├── 📁tests 
  │   └── __init__.py
  ├── .env
  ├── .env.example
  ├── README.md
  ├── .gitignore
  ├── requirements.txt
  └── main.py

<!-- configuring .env -->
1- created project on the google cloud with the google sheet api and downloaded as a json file
2- put the .json file in a service_account/ in the root directory under the name service_account.json 
3- added that dir to the .git ignore
4- added both the .env and .env.example
5- created a new branch on github and pushed that to it

<!-- csv logic -->
1- merged the current branch to the main
2- started a new one to work on the csv logic
3- implemented the csv loader login in src/data/csv_reader/csv_loader.py
4- impleneted the csv talk_time_extractor in src/data/csv_reader/talk_time_reader.py
5- implemnted the csv dials_reader extractor in src/data/csv_reader/dials_reader.py
6- implemnted the csv leads_reader extractor in src/data/csv_reader/leads_reader.py

<!-- agent_data_processing -->
1- merged the current branch to the main
2- started a new one to work on the core logic
3- implemented the agent_data_service in src/core/services/agent_data_service.py
4- implemented the team_member service in src/data/csv_reader/team_member.py
5- implemented the file_manger.py file in src/data/file_manager/file_manager.py

<!-- agent_data_processing -->
1- refactored the file_manager.py and the agent_data_service.py to silently ignore if the leads file doesn't exist and leave it to the user to enter it
2- created a cli.py file in src/ui/cli/cli.py