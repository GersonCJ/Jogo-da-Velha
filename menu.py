import os
from match import Match
from user import User


def menu():  # Menu do jogo. Inicialmente, exibir histórico e excluir jogador eram métodos da classe User, mas isso foi mudado e deixado direto na condição do menu, por simplificação.
    n = input('\nDigite o número correspondente ao que deseja fazer: \n'
              '1. Criar um novo jogador.\n'
              '2. Exibir histórico de um jogador.\n'
              '3. Excluir um jogador.\n'
              '4. Iniciar uma partida.\n')

    try:
        n = int(n)
    except ValueError:
        print('\nÉ preciso digitar um número inteiro de 1 a 4.')
        return menu()
    else:
        if n == 1:
            nome = input('\nInforme o nome do jogador que se deseja criar: ')
            p = User(nome)
            p.check_user(nome)

        elif n == 2:
            nome = input('\nInforme o nome do jogador, cujo histórico deseja verificar: ')
            try:
                with open(f"{nome}.txt") as file:
                    count = file.readlines()
                    print(f'\nVitórias = {count[0]}', f'\nDerrotas = {count[1]}')
            except IOError as e:
                print(e)
                print('\nJogador inexistente !')

        elif n == 3:
            nome = input('\nInforme o nome do jogador, que se deseja remover: ')
            if os.path.isfile(f'{nome}.txt'):
                os.remove(f'{nome}.txt')
            else:
                print('\nJogador informado não existe !')

        elif n == 4:
            player_1 = input('\nInforme o nome do jogador 1: ')
            player_2 = input('\nInforme o nome do jogador 2: ')

            if os.path.isfile(f'{player_1}.txt') and os.path.isfile(f'{player_2}.txt'):
                m = Match(player_1, player_2)
                m.rpg()

            else:
                print('\nAmbos jogadores precisam estar criados para que uma partida seja iniciada.')

        else:
            print('\nValor inválido ! Favor escolher um número inteiro de 1 a 4.')

        return menu()

