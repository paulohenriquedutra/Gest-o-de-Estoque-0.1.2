#Principais ideias de Funcionalidades: Login, Histórico de Movimentação,(entrada e saída de produtos com data e hora), Cadastro de Produtos, Controle de Estoque, Consulta e Pesquisa

#Bibliotecas

from Xclasses import Funcoes

#Conectando com o Banco de dados
host='localhost'
usuario='root'
senha='admin'
db ='pythonsql'

sistema = Funcoes(host, usuario, senha, db)

i = sistema.Inicio(1)
x = 0
while i[0] == 1 or x == 1:
    print('\033c', end='')
    print('\033[36m', end='=' * 40)
    print('\n=====\033[35m Sistema de Gestão de Estoque\033[36m =====')
    print('=' * 40)
    funcao = int(input('\nEscolha uma das opções abaixo:\n'
          '(1) - Consultar produtos \n'
          '(2) - Cadastrar produto novo\n'
          '(3) - Adicionar ou remover quantidade\n'
          '(4) - Historico de Movimentação\n'
          '(5) - Logoff\n: '))
    if funcao == 1:
        x = sistema.Consulta(1)
    elif funcao == 2:
        x = sistema.Cadastrar(1)
    elif funcao == 3:
        print('\033c', end='')
        escolha = input('\033[36m(1) - Adicionar produto\n'
              '(2) - Remover produto \n'
              'Escolha uma das opções acima:')
        if escolha == '1':
            x = sistema.Adicionar(1, i)
        else:
            x = sistema.Remover(1, i)
    elif funcao == 4:
        x = sistema.Historico(1)
    elif funcao == 5:
        print('Saindo......')
        i = 0, 0, 0
        x = sistema.Inicio(1)
    else:
        input('\033[31m\nOpção Invalida, pressione enter para voltar ')
        x = 1