# database.py
import sqlite3
import json
from datetime import datetime

DB_NAME = 'plataforma_hidraulica.db'

def setup_database():
    """Cria as tabelas necessárias no banco de dados se elas não existirem."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    # Tabela de projetos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projects (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            project_name TEXT NOT NULL,
            project_data TEXT NOT NULL, -- Armazenará os dados do projeto como um JSON
            last_modified TIMESTAMP NOT NULL,
            UNIQUE(username, project_name) -- Garante que um usuário não tenha projetos com o mesmo nome
        )
    ''')
    conn.commit()
    conn.close()

def save_project(username, project_name, project_data):
    """Salva ou atualiza um projeto para um determinado usuário."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Converte o dicionário de dados do projeto para uma string JSON
    project_data_json = json.dumps(project_data)
    timestamp = datetime.now()

    # Usa INSERT OR REPLACE para inserir se não existir, ou substituir se já existir
    cursor.execute('''
        INSERT OR REPLACE INTO projects (username, project_name, project_data, last_modified)
        VALUES (?, ?, ?, ?)
    ''', (username, project_name, project_data_json, timestamp))

    conn.commit()
    conn.close()
    return True

def load_project(username, project_name):
    """Carrega os dados de um projeto específico de um usuário."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT project_data FROM projects WHERE username = ? AND project_name = ?", (username, project_name))
    result = cursor.fetchone()
    conn.close()

    if result:
        # Converte a string JSON de volta para um dicionário Python
        return json.loads(result[0])
    return None

def get_user_projects(username):
    """Retorna uma lista com os nomes de todos os projetos de um usuário."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT project_name FROM projects WHERE username = ? ORDER BY last_modified DESC", (username,))
    projects = [row[0] for row in cursor.fetchall()]
    conn.close()
    return projects
