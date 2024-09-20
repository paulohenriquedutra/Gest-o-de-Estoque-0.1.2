import pymysql
from datetime import datetime
import pytz
import pandas as pd
from sqlalchemy import create_engine


class Funcoes:

    def __init__(self, host, usuario, senha, db):
        # Inicializando a conexão com o banco de dados
        self.conexao = pymysql.connect(
            host=host,
            user=usuario,
            passwd=senha,
            database=db
        )
        self.engine = create_engine(f'mysql+pymysql://{usuario}:{senha}@{host}/{db}')
        self.cursor = self.conexao.cursor()
    def Cadastrar(self, repeticao):
        while repeticao == 1:
            print('\033c', end='')
            print('\033[36m')
            print('=' * 20)
            print('\033[35mCADASTRO DE PRODUTO\033[36m')
            print('=' * 20)
            # Geração do código de um produto novo

            comando = 'SELECT MAX(codigo) FROM estoque'
            self.cursor.execute(comando)
            codigo = self.cursor.fetchone()[0] + 1
            codigo = int(codigo)
            self.cursor.execute(comando)
            comando = 'SELECT * FROM estoque'
            self.cursor.execute(comando)

            # Cadastrando item
            nome = input('\n\033[36mDigite o nome do produto: ').capitalize().split()
            nome = '-'.join(nome)
            preco_unitario = float(input('Digite o valor do produto: '))
            quantidade = int(input('Digite a quantidade de produtos: '))
            fornecedor = input('Digite o nome do fornecedor: ').upper()
            comando = f'INSERT INTO estoque(codigo, nome, preco_unitario, quantidade, fornecedor) VALUES(%s,%s, %s, %s, %s)'
            valores = {codigo}, {nome}, {preco_unitario}, {quantidade}, {fornecedor}
            self.cursor.execute(comando, valores)
            self.conexao.commit()
            print('Produto cadastrado com sucesso!')
            loop = input('Pressione a tecla "s" para continuar e "n" para voltar ao menu principal: ').upper()
            if loop == 'N':
                return 1
            else:
                repeticao = 1
    def Consulta(self, repeticao):
        while repeticao == 1:
            print('\033c', end='')
            print('\033[36m')
            print('=' * 20)
            print('\033[35m CONSULTA DE ITEM\033[36m')
            print('=' * 20)
            pesquisa = input('\033[36mDigite o codigo ou o nome do produto: ').capitalize()
            if pesquisa.isnumeric():
                codigo = pesquisa
                comando = f'SELECT * FROM estoque where codigo = {codigo}'
                self.cursor.execute(comando)
                resultado = self.cursor.fetchone()
                if resultado:
                    print(f'Código: {resultado[0]}\nNome: {resultado[1]}\nPreço Unitário: {resultado[2]}\nQuantidade: {resultado[3]}\nFornecedor: {resultado[4]}')
                    pesquisa = 'a'
                else:
                    print('\n\033[31mNenhum produto encontrado')
            else:
                nome = pesquisa.capitalize().split()
                nome = '-'.join(nome)
                comando = f'SELECT * FROM estoque where nome LIKE "%{nome}%"'
                self.cursor.execute(comando)
                saida = self.cursor.fetchall()
                vetor = len(saida)
                i = 0
                if saida:
                    print('\033c', end='')
                    print('\033[36m')
                    print('=' * 20)
                    print('\033[35mRESULTADOS\033[36m')
                    print('=' * 20)
                    while i < vetor:
                        resultado = saida[i]
                        print(f'\nCódigo: {resultado[0]}\nNome: {resultado[1]}\nPreço Unitário: {resultado[2]}\nQuantidade: {resultado[3]}\nFornecedor: {resultado[4]}')
                        i = i + 1
                else:
                    print('\n\033[31mNenhum produto encontrado')
            loop = input('\033[36m\nPressione a tecla "s" para continuar e "n" para voltar ao menu principal:  ').upper()
            if loop == 'N':
                return 1
            else:
                repeticao = 1
    def Adicionar(self, repeticao, user):
        while repeticao == 1:
            cpf = user[1]
            usuario = user[2]
            repeticao = 0
            print('\033c', end='')
            print('\033[36m')
            print('=' * 20)
            print('\033[35mADIÇÃO DE PRODUTOS\033[36m')
            print('=' * 20)
            codigo = int(input('\033[36mDigite o codigo do produto que deseja adicionar: '))
            comando = f'SELECT nome FROM estoque where codigo = {codigo}'
            self.cursor.execute(comando)
            nome = self.cursor.fetchone()[0]
            comando = f'SELECT quantidade FROM estoque where codigo = {codigo}'
            self.cursor.execute(comando)
            quantidade_anterior = self.cursor.fetchone()[0]
            quantidade_adicao = int(
            input(f'Atualmente possuimos em estoque {quantidade_anterior} {nome}s quantos(as) deseja adicionar?: '))
            quantidade_atual = quantidade_anterior + quantidade_adicao
            comando = f'UPDATE estoque SET quantidade = "{quantidade_atual}" WHERE nome = "{nome}"'
            self.cursor.execute(comando)
            self.conexao.commit()
            print(f'\nProduto adicionado com sucesso!\n\nquantidade atual de {nome}s em estoque é {quantidade_atual}')
            save = input('\nPressione "s" para salvar sua movimentação ou "n" para voltar ao menu principal: ' ).upper()
            if save == 'S':
                data = self.Data()
                hora = self.Hora()
                self.Add_historico(cpf, usuario, data, hora, codigo, nome, 'Adição', quantidade_adicao)
                loop = input('\nPressione a tecla "s" para continuar e "n" para voltar ao menu principal: ').upper()
            return 1
    def Remover(self, repeticao, user):
        while repeticao == 1:
            cpf = user[1]
            usuario = user[2]
            repeticao = 0
            print('\033c', end='')
            print('\033[36m')
            print('=' * 20)
            print('\033[35mREMOVER QUANTIDADE\033[36m')
            print('=' * 20)
            codigo = int(input('\033[36mDigite o codigo do produto que deseja remover: '))
            comando = f'SELECT nome FROM estoque where codigo = {codigo}'
            self.cursor.execute(comando)
            nome = self.cursor.fetchone()[0]
            comando = f'SELECT quantidade FROM estoque where codigo = {codigo}'
            self.cursor.execute(comando)
            quantidade_anterior = self.cursor.fetchone()[0]
            quantidade_remocao = int(input(f'Atualmente possuimos em estoque {quantidade_anterior} {nome}s quantos(as) deseja remover?: '))
            if quantidade_remocao > quantidade_anterior:
                print('\033[31m\nQuantidade insuficiente de produtos no estoque')
                loop = input('\033[36m\nPressione a tecla "s" para tentar novamente e "n" para voltar ao menu principal:')
                if loop == 'N':
                    return 1
                else:
                    repeticao = 1
            else:
                quantidade_atual = quantidade_anterior - quantidade_remocao
                comando = f'UPDATE estoque SET quantidade = "{quantidade_atual}" WHERE nome = "{nome}"'
                self.cursor.execute(comando)
                self.conexao.commit()
                print(f'\nProduto removido com sucesso!\n\nquantidade atual de {nome}s em estoque é {quantidade_atual} ')
                save = input('\nPressione "s" para salvar sua movimentação ou "n" para voltar ao menu principal: ').upper()
                if save == 'S':
                    data = self.Data()
                    hora = self.Hora()
                    self.Add_historico(cpf, usuario, data, hora, codigo, nome, 'Remoção', quantidade_remocao)
                    loop = input('\nPressione a tecla "s" para continuar e "n" para voltar ao menu principal: ').upper()
                elif save == 'N' or loop == 'N':
                    return 1
                else:
                    repeticao = 1
    def Historico(self, repeticao):
        while repeticao == 1:
            print('\033c', end='')
            print('\033[36m')
            print('=' * 25)
            print('\033[35mHISTORICO DE MOVIMENTAÇÃO\033[36m')
            print('=' * 25)
            comando = f'SELECT * FROM historico_movimentacao'
            df = pd.read_sql('SELECT * FROM historico_movimentacao', self.engine)
            print(df)
            loop = input('\033[36m\nPressione a tecla "s" para atualizar o historico e "n" para voltar ao menu principal:').upper()
            if loop == 'N':
                return 1
            else:
                repeticao = 1
    def Data(self):
        agora = datetime.now(pytz.utc)
        data = agora.strftime('%d/%m/%Y')
        return data
    def Hora(self):
        tz = pytz.timezone('America/Sao_Paulo')
        agora = datetime.now(tz)
        atual = agora.strftime('%H:%M:%S')
        return atual
    def Add_historico(self, cpf_usuario, nome_usuario, data, hora, codigo_produto, nome_produto, tipo_movimentacao, quantidade):
        comando = f"INSERT INTO historico_movimentacao(cpf_usuario, nome_usuario, data, hora, codigo_produto, nome_produto, tipo_movimentacao, quantidade) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        valores = (cpf_usuario, nome_usuario, data, hora, codigo_produto, nome_produto, tipo_movimentacao, quantidade)
        self.cursor.execute(comando, valores)
        self.conexao.commit()
        print('\nSalvo com sucesso.')
    def criar_usuario(self, repeticao):
        while repeticao == 1:
            print('\033c', end='')
            print('\033[36m')
            print('=' * 25)
            print('\033[35mCADASTRO DE USUARIO\033[36m')
            print('=' * 25)
            username = input("\nDigite um nome de usuário: ").capitalize()
            cpf = input("Digite seu cpf: ")
            tamanho = len(cpf)
            if tamanho == 11:
                cpf_formatado = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
                comando = f'SELECT * FROM users WHERE cpf = "{cpf_formatado}"'
                self.cursor.execute(comando)
                consulta = self.cursor.fetchone()
                if consulta is None:
                    senha = input("Digite uma senha: ")
                    comando = f'INSERT INTO users(cpf, nome, senha) VALUES(%s,%s,%s)'
                    valores = cpf, username, senha
                    self.cursor.execute(comando, valores)
                    self.conexao.commit()
                    print('\nUsuário cadastrado com sucesso!\n')
                else:
                    print("Usuário já existe. pressione'")
                    repeticao = 1
            else:
                print('\nerro\n\nverifique se seu cpf está correto')
                repeticao = 1
            loop = input('\033[36m\nPressione a tecla "s" para tentar novamente ou "n" para voltar ao inicio:  ').upper()
            if loop == 'N':
                return 1
            else:
                repeticao = 1
    def fazer_login(self, repeticao):
        while repeticao == 1:
            print('\033c', end='')
            print('\033[36m')
            print('=' * 10)
            print('\033[35m LOGIN\033[36m')
            print('=' * 10)
            cpf = input("\nDigite seu login (CPF): ")
            senha_login = input("Digite sua senha: ")
            cpf_formatado = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'
            comando = f'SELECT senha, nome FROM users WHERE cpf = "{cpf_formatado}"'
            self.cursor.execute(comando)
            resultado = self.cursor.fetchone()
            if resultado:
                if senha_login == resultado[0]:
                    return 1, cpf_formatado, resultado[1]
                else:
                    print('Credenciais inválidas')
                    loop = input('\033[36m\nPressione a tecla "s" para tentar novamente ou "n" para voltar ao inicio:  ').upper()
                    if loop == 'N':
                        return 0
                    else:
                        repeticao = 1
            else:
                print('Credenciais inválidas.')
                loop = input('\033[36m\nPressione a tecla "s" para tentar novamente ou "n" para voltar ao inicio:  ').upper()
                if loop == 'N':
                    return 0
                else:
                    repeticao = 1
    def Inicio(self, repeticao):
        while repeticao == 1:
            print('\033c', end='')
            print('\033[36m')
            print('=' * 15)
            print('\033[35m TELA INICIAL\033[36m')
            print('=' * 15)
            print("\n1. Criar usuário")
            print("2. Fazer login")
            print("3. Sair")
            escolha = input("\nEscolha uma opção: ")
            if escolha == '1':
                repeticao = self.criar_usuario(1)
            elif escolha == '2':
                autenticacao =  self.fazer_login(1)
                if autenticacao == 0:
                    repeticao = 1
                else:
                    return autenticacao
            elif escolha == '3':
                print("\nSaindo do sistema...")
                return 0, 0
            else:
                print("Opção inválida. Tente novamente.")