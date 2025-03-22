import os

# Database settings
DATABASE = {
    'HOST': '192.168.29.221',
    'PORT': '2021',
    'USER': 'ray',
    'PASSWORD': 'advicr49--',
    'NAME': 'health',
    'DRIVER': 'ODBC Driver 17 for SQL Server',
}

# OpenAI settings
OPENAI = {
    'MODEL': 'gpt-4o',
    'TEMPERATURE': 0,
}

# Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(BASE_DIR, 'src')
OBJ_DIR = os.path.join(BASE_DIR, 'obj')
BIN_DIR = os.path.join(BASE_DIR, 'bin')

# Compiler settings
COMPILER = {
    'CC': 'gcc',
    'CFLAGS': '-Wall -Wextra -O2',
}
