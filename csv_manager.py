import csv
from pathlib import Path
from datetime import datetime

class CSVManager:
    def __init__(self):
        self.exports_dir = Path("exports")
        self.exports_dir.mkdir(exist_ok=True)

    def exportar_para_csv(self, dados):
        """Exporta os dados do banco de dados para um arquivo CSV"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        arquivo_csv = self.exports_dir / f"livros_exportados_{timestamp}.csv"
        
        with open(arquivo_csv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ID', 'Título', 'Autor', 'Ano de Publicação', 'Preço'])
            writer.writerows(dados)
        
        return arquivo_csv

    def importar_do_csv(self, caminho_arquivo):
        """Importa dados de um arquivo CSV"""
        dados = []
        with open(caminho_arquivo, 'r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Pula o cabeçalho
            for row in reader:
                if len(row) == 5:  # Verifica se a linha tem todos os campos
                    dados.append((row[1], row[2], int(row[3]), float(row[4])))
        return dados