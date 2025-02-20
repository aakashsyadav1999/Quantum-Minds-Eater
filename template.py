import os

# Project name
project_name = 'Agents_Pipeline'

# Create project directory
list_of_files = [
    'settings.py',
    'setup.toml',
    'README.md',
    'requirements.txt',
    'main.py',
    'LICENSE',
    'Dockerfile',
    '.gitignore',
    'Makefile',
    'tests/test_main.py',
    'tests/__init__.py',
    'src/__init__.py',
    'MANIFEST.in',
    '.dockerignore',
    '.gitattributes',
    '.editorconfig',
    '.bumpversion.cfg',
    'research/research.ipynb',
    'docker-compose.yml',
    'app.py',
    'src/__init__.py',
    'src/constant/__init__.py',
    'src/utils.py/__init__.py',
    'src/utils.py/common.py',
    'src/models.py',
    'src/prompts/__init__.py',
    'src/prompts/prompts.py',
    'models/config.yml',
    'database/config.yml',
    'src/exception/__init__.py',
    'src/logger/__init__.py',
    'src/pipeline/__init__.py',
    'src/pipeline/flow_pipeline.py',
    'src/components/__init__.py',
    'src/agents/__init__.py',
    'src/agents/csv_agent.py',
    'src/agents/jira_agent.py',
    'src/agents/dataframe_agent.py',
    'src/agents/sql_agent.py',
    'src/agents/email_agent.py',
    'src/agents/website_research_agent.py',
    'src/agents/duck_duck_go_agent.py',
    'src/agents/cassandra_database_agent.py',
    'src/entity/__init__.py',
    'src/entity/entity.py',
]

# Create project directory
def create_files():
    for file in list_of_files:
        directory = os.path.dirname(file)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(file):
            with open(file, 'w') as f:
                f.write('')
            print(f'Created {file}')
        else:
            print(f'{file} already exists')
        
create_files()