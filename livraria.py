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
def criar_tabela():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER,
            preco REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

#4 - Funcoes de Backup
def fazer_backup():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = BACKUP_DIR / f"backup_livraria_{timestamp}.db"
    
    if DB_PATH.exists():
        shutil.copy2(DB_PATH, backup_file)
        print(f"Backup criado: {backup_file}")
    
    limpar_backups_antigos()
    
    return backup_file

def limpar_backups_antigos():
    backups = list(BACKUP_DIR.glob("backup_livraria_*.db"))
    backups.sort(key=os.path.getmtime, reverse=True)
    
    for backup in backups[5:]:
        backup.unlink()
        print(f"Backup antigo removido: {backup}")
        
# 5 - Funções CRUD
def adicionar_livro():
    fazer_backup()
    titulo = input("Digite o título do livro: ")
    autor = input("Digite o autor do livro: ")
    while True:
        try:
            ano = int(input("Ano de publicação: "))
            if ano < 0 or ano > datetime.now().year:
                raise ValueError
            break
        except ValueError:
            print("Ano inválido! Digite um ano válido.")
    
    while True:
        try:
            preco = float(input("Preço do livro: "))
            if preco <= 0:
                raise ValueError
            break
        except ValueError:
            print("Preço inválido! Digite um valor numérico positivo.")
        
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO livros (titulo, autor, ano_publicacao, preco)
        VALUES (?, ?, ?, ?)
    ''', (titulo, autor, ano, preco))
    conn.commit()
    conn.close()
    print("Livro adicionado com sucesso!")

def exibir_livros():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM livros')
    livros = cursor.fetchall()

    if not livros:
        print("Nenhum livro cadastrado.")
    else:
        print("\n=== Livris Cadastrados ===")
        for livro in livros:
            print(f"ID: {livro[0]}")
            print(f"Título: {livro[1]}")
            print(f"Autor: {livro[2]}")
            print(f"Ano de Publicação: {livro[3]}")
            print(f"Preço: R$ {livro[4]:.2f}")
            print("-" * 30)
    conn.close()

def atualizar_preco():
    fazer_backup()  
    
    exibir_livros()
    livro_id = input("ID do livro para atualizar preço: ")
    
    while True:
        try:
            novo_preco = float(input("Novo preço: R$ "))
            if novo_preco <= 0:
                raise ValueError
            break
        except ValueError:
            print("Preço inválido! Digite um valor positivo.")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("UPDATE livros SET preco = ? WHERE id = ?", (novo_preco, livro_id))
    
    if cursor.rowcount > 0:
        print("Preço atualizado com sucesso!")
    else:
        print("Livro não encontrado!")
    
    conn.commit()
    conn.close()

def remover_livro():
    fazer_backup()
    
    exibir_livros()
    livro_id = input("ID do livro para remover: ")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM livros WHERE id = ?", (livro_id,))
    
    if cursor.rowcount > 0:
        print("Livro removido com sucesso!")
    else:
        print("Livro não encontrado!")
    
    conn.commit()
    conn.close()

def buscar_por_autor():
    autor = input("Digite o nome do autor: ")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM livros WHERE autor LIKE ?", (f"%{autor}%",))
    livros = cursor.fetchall()
    
    if not livros:
        print("Nenhum livro encontrado para este autor.")
    else:
        print(f"\n=== LIVROS DE {autor.upper()} ===")
        for livro in livros:
            print(f"Título: {livro[1]}")
            print(f"Ano: {livro[3]}")
            print(f"Preço: R$ {livro[4]:.2f}")
            print("-" * 30)
    
    conn.close() 
# 6- Funcoes de exportacao/Importacao CSV

# 7 - Menu Principal

# 8 - Execucao do sistema

