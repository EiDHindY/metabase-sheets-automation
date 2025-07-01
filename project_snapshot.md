<!-- set up -->
1- created a remote repo on github with the name (metabase-sheets-automation)
2- cloned the repo that comes with .gitignore for python and README.md
3- created a venv 
4- installed some dependencies (pip install python-dotenv requests gspread metabase-api) and froze it to the .txt file
5- pushed to the main branch on github as the initial commit


<!-- current file layout -->
  📁 metabase-sheets-automation
  ├── 📁config 
  │       └── __init__.py
  ├── 📁docs 
  │       └── 
  ├── 📁src 
  │       ├── 📁business
  │       │     ├── 📁models
  │       │     │      └── __init__.py
  │       │     ├── 📁services
  │       │     │      └── __init__.py
  │       │     └── __init__.py
  │       ├── 📁data
  │       │     ├── 📁clients
  │       │     │      └── __init__.py
  │       │     ├── 📁repositories
  │       │     │      └── __init__.py
  │       │     └── __init__.py
  │       ├── 📁presentation
  │       │     └── __init__.py
  │       ├── 📁utils
  │       │     └── __init__.py
  │       └── __init__.py
  ├── 📁tests 
  │       └── __init__.py
  ├── .env.example
  ├── README.md
  ├── .gitignore
  ├── requirements.txt
  └── main.py

