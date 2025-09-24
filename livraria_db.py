import sqlite3
from pathlib import Path
from datetime import datetime
import os
import shutil

class LivrariaDB:
    def __init__(self):
        self.data_dir = Path("data")
        self.backup_dir = Path("backups")
        self.db_path = self.data_dir / "livraria.db"
        self.setup_database()

    def setup_database(self):
        """Configura o banco de dados e cria a tabela se não existir"""
        self.data_dir.mkdir(exist_ok=True)
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS livros (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            autor TEXT NOT NULL,
            ano_publicacao INTEGER NOT NULL,
            preco REAL NOT NULL
        )
        ''')
        
        conn.commit()
        conn.close()

    def criar_backup(self):
        """Cria um backup do banco de dados"""
        self.backup_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        backup_path = self.backup_dir / f"backup_livraria_{timestamp}.db"
        
        if self.db_path.exists():
            shutil.copy2(self.db_path, backup_path)
            self.limpar_backups_antigos()

    def limpar_backups_antigos(self):
        """Mantém apenas os 5 backups mais recentes"""
        backups = sorted(self.backup_dir.glob("backup_*.db"))
        while len(backups) > 5:
            backups[0].unlink()  # Remove o backup mais antigo
            backups = backups[1:]  # Atualiza a lista