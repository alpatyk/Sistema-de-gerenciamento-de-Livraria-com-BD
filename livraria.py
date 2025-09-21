import sqlite3
import os
import cvs
import shutil
from pathlib import Path
from datetime import datetime   

# 1 - Estrutura de arquivos e diretorios
BASE_DIR = Path("meu_sistema_livraria")
BACKUP_DIR = BASE_DIR / "backups"
DATA_DIR = BASE_DIR / "data"
EXPORT_DIR = BASE_DIR / "exports"

for directory in [BASE_DIR, BACKUP_DIR, DATA_DIR, EXPORT_DIR]:
    os.makedirs(directory, exist_ok=True)

DB_PATH = DATA_DIR / "livraria.db"

# 2 - Funcoes de gerenciamento do banco de dados


#4 - Funcoes de CRUD

# 5 - Funcoes de exportacao/Importacao CSV

# 6 - Menu Principal

# 7 - Execucao do sistema

