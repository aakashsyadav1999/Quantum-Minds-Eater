# Quantum Minds Eater

## Problem Statement

In today's data-driven world, organizations face the challenge of extracting meaningful insights from vast amounts of data stored in various databases. Traditional methods of querying and analyzing data can be time-consuming and require specialized knowledge of SQL and database management. This project aims to simplify the process of data extraction and analysis by leveraging the power of AI agents.

## Solution

Quantum Minds Eater is a project designed to streamline data querying and analysis using AI agents. By integrating with SQL databases and utilizing advanced language models, this project allows users to interact with their data in a more intuitive and efficient manner. Users can ask natural language questions, and the AI agents will translate these queries into SQL commands, execute them, and return the results.

## Features

- **Natural Language Querying**: Users can ask questions in plain English, and the AI agents will handle the translation to SQL.
- **Integration with SQL Databases**: Supports various SQL databases, making it versatile for different use cases.
- **Advanced Language Models**: Utilizes state-of-the-art language models like GPT-4o for accurate and context-aware responses.
- **Streamlined Data Analysis**: Simplifies the process of data extraction and analysis, saving time and effort.

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/Quantum-Minds-Eater.git
    cd Quantum-Minds-Eater
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

## Configuration

1. Update the `settings.py` file with your database and OpenAI settings:
    ```python
    # filepath: d:\vscode\sstech\quantum-mind-eaters\Quantum-Minds-Eater\settings.py

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
    ```

## Usage

1. Run the main script:
    ```sh
    python src/agents/sql_agent.py
    ```

2. Enter your question when prompted:
    ```sh
    Enter your question: List the total sales per country. Which country's customers spent the most?
    ```

## Dependencies

The project requires the following dependencies, which are listed in the `requirements.txt` file:
- pandas
- langchain
- numpy
- langchain_experimental
- langchain_openai
- tabulate
- pydantic
- logfire
- requests
- ipykernel
- python-dotenv
- openai
- streamlit
- pyodbc
- google-auth-httplib2
- google-auth-oauthlib
- google-api-python-client
- beautifulsoup4
- duckduckgo-search
- phidata

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Authors

- Your Name - [your.email@example.com](mailto:your.email@example.com)

## Acknowledgments

- Special thanks to the developers of the libraries and tools used in this project.
- Inspired by the need to simplify data querying and analysis in modern organizations.
