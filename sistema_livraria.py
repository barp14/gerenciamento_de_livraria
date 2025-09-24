from livraria_db import LivrariaDB
from csv_manager import CSVManager
import sqlite3

def validar_entrada(tipo, valor, campo):
    """Valida as entradas do usuário"""
    if tipo == 'texto':
        if not valor.strip():
            raise ValueError(f"O campo {campo} não pode estar vazio!")
        return valor.strip()
    elif tipo == 'ano':
        ano = int(valor)
        if ano < 1000 or ano > 9999:
            raise ValueError("Ano inválido! Digite um ano entre 1000 e 9999.")
        return ano
    elif tipo == 'preco':
        preco = float(valor)
        if preco < 0:
            raise ValueError("Preço não pode ser negativo!")
        return preco

class SistemaLivraria:
    def __init__(self):
        self.db = LivrariaDB()
        self.csv_manager = CSVManager()

    def adicionar_livro(self):
        """Adiciona um novo livro ao sistema"""
        try:
            titulo = validar_entrada('texto', input("Digite o título do livro: "), "título")
            autor = validar_entrada('texto', input("Digite o autor do livro: "), "autor")
            ano = validar_entrada('ano', input("Digite o ano de publicação: "), "ano")
            preco = validar_entrada('preco', input("Digite o preço do livro: "), "preço")

            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            self.db.criar_backup()  # Cria backup antes da inserção
            
            cursor.execute('''
            INSERT INTO livros (titulo, autor, ano_publicacao, preco)
            VALUES (?, ?, ?, ?)
            ''', (titulo, autor, ano, preco))
            
            conn.commit()
            conn.close()
            print("Livro adicionado com sucesso!")
            
        except ValueError as e:
            print(f"Erro de validação: {e}")
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")

    def exibir_livros(self):
        """Exibe todos os livros cadastrados"""
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM livros')
            livros = cursor.fetchall()
            
            if not livros:
                print("Nenhum livro cadastrado!")
                return
            
            print("\nLivros cadastrados:")
            print("ID | Título | Autor | Ano | Preço")
            print("-" * 50)
            for livro in livros:
                print(f"{livro[0]} | {livro[1]} | {livro[2]} | {livro[3]} | R${livro[4]:.2f}")
            
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Erro ao consultar banco de dados: {e}")

    def atualizar_preco(self):
        """Atualiza o preço de um livro"""
        try:
            self.exibir_livros()
            id_livro = int(input("\nDigite o ID do livro que deseja atualizar: "))
            novo_preco = validar_entrada('preco', input("Digite o novo preço: "), "preço")

            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            self.db.criar_backup()  # Cria backup antes da atualização
            
            cursor.execute('UPDATE livros SET preco = ? WHERE id = ?', (novo_preco, id_livro))
            
            if cursor.rowcount == 0:
                print("Livro não encontrado!")
            else:
                conn.commit()
                print("Preço atualizado com sucesso!")
            
            conn.close()
            
        except ValueError as e:
            print(f"Erro de validação: {e}")
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")

    def remover_livro(self):
        """Remove um livro do sistema"""
        try:
            self.exibir_livros()
            id_livro = int(input("\nDigite o ID do livro que deseja remover: "))

            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            self.db.criar_backup()  # Cria backup antes da remoção
            
            cursor.execute('DELETE FROM livros WHERE id = ?', (id_livro,))
            
            if cursor.rowcount == 0:
                print("Livro não encontrado!")
            else:
                conn.commit()
                print("Livro removido com sucesso!")
            
            conn.close()
            
        except ValueError:
            print("ID inválido!")
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")

    def buscar_por_autor(self):
        """Busca livros por autor"""
        try:
            autor = validar_entrada('texto', input("Digite o nome do autor: "), "autor")
            
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM livros WHERE autor LIKE ?', (f"%{autor}%",))
            livros = cursor.fetchall()
            
            if not livros:
                print("Nenhum livro encontrado para este autor!")
                return
            
            print("\nLivros encontrados:")
            print("ID | Título | Autor | Ano | Preço")
            print("-" * 50)
            for livro in livros:
                print(f"{livro[0]} | {livro[1]} | {livro[2]} | {livro[3]} | R${livro[4]:.2f}")
            
            conn.close()
            
        except ValueError as e:
            print(f"Erro de validação: {e}")
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")

    def exportar_dados(self):
        """Exporta os dados para CSV"""
        try:
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            cursor.execute('SELECT * FROM livros')
            dados = cursor.fetchall()
            
            if not dados:
                print("Não há dados para exportar!")
                return
            
            arquivo_csv = self.csv_manager.exportar_para_csv(dados)
            print(f"Dados exportados com sucesso para: {arquivo_csv}")
            
            conn.close()
            
        except sqlite3.Error as e:
            print(f"Erro ao exportar dados: {e}")

    def importar_dados(self):
        """Importa dados de um arquivo CSV"""
        try:
            arquivo = input("Digite o caminho do arquivo CSV: ")
            dados = self.csv_manager.importar_do_csv(arquivo)
            
            if not dados:
                print("Nenhum dado encontrado para importar!")
                return
            
            conn = sqlite3.connect(self.db.db_path)
            cursor = conn.cursor()
            
            self.db.criar_backup()  # Cria backup antes da importação
            
            for livro in dados:
                cursor.execute('''
                INSERT INTO livros (titulo, autor, ano_publicacao, preco)
                VALUES (?, ?, ?, ?)
                ''', livro)
            
            conn.commit()
            conn.close()
            print("Dados importados com sucesso!")
            
        except FileNotFoundError:
            print("Arquivo não encontrado!")
        except ValueError as e:
            print(f"Erro nos dados do arquivo: {e}")
        except sqlite3.Error as e:
            print(f"Erro no banco de dados: {e}")

    def fazer_backup(self):
        """Faz backup manual do banco de dados"""
        try:
            self.db.criar_backup()
            print("Backup realizado com sucesso!")
        except Exception as e:
            print(f"Erro ao realizar backup: {e}")

    def exibir_menu(self):
        """Exibe o menu principal do sistema"""
        while True:
            print("\n=== Sistema de Gerenciamento de Livraria ===")
            print("1. Adicionar novo livro")
            print("2. Exibir todos os livros")
            print("3. Atualizar preço de um livro")
            print("4. Remover um livro")
            print("5. Buscar livros por autor")
            print("6. Exportar dados para CSV")
            print("7. Importar dados de CSV")
            print("8. Fazer backup do banco de dados")
            print("9. Sair")
            
            try:
                opcao = int(input("\nEscolha uma opção: "))
                
                if opcao == 1:
                    self.adicionar_livro()
                elif opcao == 2:
                    self.exibir_livros()
                elif opcao == 3:
                    self.atualizar_preco()
                elif opcao == 4:
                    self.remover_livro()
                elif opcao == 5:
                    self.buscar_por_autor()
                elif opcao == 6:
                    self.exportar_dados()
                elif opcao == 7:
                    self.importar_dados()
                elif opcao == 8:
                    self.fazer_backup()
                elif opcao == 9:
                    print("Encerrando o sistema...")
                    break
                else:
                    print("Opção inválida!")
                    
            except ValueError:
                print("Por favor, digite um número válido!")