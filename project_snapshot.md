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
  │   └── __init__.py
  ├── 📁 data/
  │   ├── input/
  │   │   ├── leads/
  │   │   ├── talk-time/
  │   │   └── dials-made/
  │   ├── processed/
  │   └── team/
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


