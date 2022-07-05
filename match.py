import pandas as pd
import numpy as np


class Match:  # Classe que rege uma partida

    def __init__(self, player1, player2):
        first_rows = ["", "", "", "", ""]  # Criação do tabuleiro - Tabela do Pandas 5x5
        table = {'': ['R1', 'R2', 'R3', 'R4', 'R5'],
                 'C1': first_rows, 'C2': first_rows, 'C3': first_rows, 'C4': first_rows, 'C5': first_rows}

        self.__board = pd.DataFrame(data=table)
        self.__player1 = player1
        self.__player2 = player2
        self.__roles = self.__apply_roles()
        self.__rules = False

    @property
    def playing(self):
        return self.__playing

    @property
    def in_hold_player(self):
        return self.__in_hold_player

    @playing.setter
    def playing(self, set_player):
        self.__playing = set_player

    @in_hold_player.setter
    def in_hold_player(self, new_hold):
        self.__in_hold_player = new_hold

    @property
    def board(self):
        return self.__board

    @property
    def roles(self):
        return self.__roles

    @property
    def play1(self):
        return self.__player1

    @property
    def play2(self):
        return self.__player2

    @property
    def rules(self):
        return self.__rules

    def __str__(self):  # Apresentação do tabuleiro
        return self.board.to_string(index=False)

    def __apply_roles(self):  # Método privado apply_roles() determina peças, qual jogador jogará primeiro e qual ficará em espera. Jogador que escolher X começa a jogar.
        pieces = ['X', 'O']
        piece = input(f'Com qual peça {self.play1} deseja jogar? - X ou O ').upper()
        try:
            assert piece in pieces, 'oops'
        except AssertionError:
            print(f'Favor escolher {pieces[0]} ou {pieces[1]}')
            return self.__apply_roles()
        if piece == 'X':
            self.__playing = self.play1
            self.__in_hold_player = self.play2
            return {self.play1: ['X', False], self.play2: ['O', False]}  # Valor retornado é o atributo self.__roles
            # que contém as peças de cada jogador e um valor indicando se o jogador é ou não vitorioso,
            # ambos inciando por False.
        else:
            self.__playing = self.play2
            self.__in_hold_player = self.play1
            return {self.play2: ['X', False], self.play1: ['O', False]}

    def rpg(self):  # Inicio do jogo

        rows = {'R1': 0, 'R2': 1, 'R3': 2, 'R4': 3, 'R5': 4}
        cols = ['C1', 'C2', 'C3', 'C4', 'C5']

        if not self.rules:  # Rules - Começa com Falso, quando a classe Match é instanciada,
            # após a primeira jogada, self.rules recebe True, não aparecendo mais as instruções.
            print(
                "\nO tabuleiro abaixo contém 5 linhas (R1 a R5) e 5 Colunas (C1 a C5).\n"
                "Para garantir a vitória, o Player deverá preencher, com seu respectivo símbolo, 4"
                " espaços consecutivos, valendo vertical, horizontal e diagonal.\nÉ possível haver empate e, "
                "sendo assim, nenhum player receberá pontos."
            )
        else:
            pass

        print(f'\n{self}')

        print(f'\n{self.playing} escolha uma Coluna de C1 a C5 e uma linha de R1 a R5 para por sua peça')

        while True:
            while True:
                col = input("\nColuna: ").upper()  # Escolhe a coluna. Enquanto errada, repete.
                try:
                    assert col in cols, 'oops'
                    break
                except AssertionError:
                    print("\nEssa coluna não existe. Favor escolher uma coluna de C1 a C5.")

            while True:
                row = input("\nLinha: ").upper()
                try:
                    assert row in rows.keys(), 'oops'  # Escolhe a Linha. Enquanto errada, repete.
                    break
                except AssertionError:
                    print("\nEssa linha não existe. Favor escolher uma linha de R1 a R5.")

            if self.board[col][rows[row]] != '':  # Analisa se o espaço escolhido já está ocupado.
                print('\nJá tem uma peça nesse espaço.... Será preciso escolher outra vez.\n', self)
            else:
                self.board[col][rows[row]] = self.roles[self.playing][0]
                break

        self.__rules = True
        self.evaluate_board()

    def evaluate_board(self):  # A cada jogada o tabuleiro é avaliado e se não há vitória, ou empate, os jogador que está jogando é trocado com o jogador que está em espera, e o jogo retorna para rpg().
        piece = self.roles[self.playing][0]
        calculus = self.calculations(piece)  # Chama função calculations que realiza a verificação.
        if calculus[0] == 1:

            print(f'Parabéns !!! {self.playing} venceu !!!')  # Em caso de vitória, o self.__roles, recebe True, indicando vitória do jogador vencedor.
            self.__roles[self.playing][1] = True
            return self.distribute_points()

        elif calculus[0] == 2:  # Em caso de empate nada acontece.

            print('Empatou !!! :( Nenhum dos jogadores recebeu o ponto')

        else:  # Se não houver empate, nem vitória o jogo continua.

            if self.playing == self.play1:
                self.playing = self.play2
                self.in_hold_player = self.play1
            else:
                self.playing = self.play1
                self.in_hold_player = self.play2

            return self.rpg()

    def calculations(self, piece):

        table = self.board.copy()  # Cria uma cópia do tabuleuiro, para que a verificação não altere o tabuleiro em si.
        cols = list(self.board.columns)
        cols.pop(0)

        if piece == 'X':  # Analisa a peça que está sendo jogada, para que a verificação seja feita apenas em cima dessa peça.
            identifier_up = 'X'
            identifier_down = 'O'
        else:
            identifier_up = 'O'
            identifier_down = 'X'

        flag = (0, '')

        for i in cols:  # Substitui o identificador do jogador atual por 1 e os outros valores por zero.
            table.loc[table[i] == identifier_up, i] = 1
            table.loc[table[i] == identifier_down, i] = 0
            table.loc[table[i] == '', i] = 0

        # Vertical verification:
        for i in cols:
            if sum(table[i]) == 4:
                aux = 1
                c = 0

                for j in range(0, 5):
                    if table[i][j] == aux:
                        c += 1
                    else:
                        pass

                    if c == 4:
                        break
                if c == 4:
                    flag = (1, identifier_up)
                    break
                else:
                    pass
            else:
                pass

            if flag[0]:
                break

        if flag[0]:
            return flag
        else:
            pass

        # Horizontal Verification
        for i in range(0, 5):

            if sum(table.iloc[i][1:6]) == 4:
                aux = 1
                c = 0

                for j in range(1, 6):
                    if table.iloc[i, j] == aux:
                        c += 1
                    else:
                        pass

                    if c == 4:
                        break
                if c == 4:
                    flag = (1, identifier_up)
                    break
            else:
                pass

            if flag[0]:
                break

        if flag[0]:
            return flag
        else:
            pass

        # Diagonal Verification:
        d1 = table.iloc[0:4, 2:6]

        d2_up = table.iloc[0:4, 1:5]

        d2_down = table.iloc[1:5, 2:6]

        d3 = table.iloc[1:5, 1:5]

        diagonals = [d1, d2_up, d2_down, d3]

        for i in diagonals:
            if sum(np.diag(i)) == 4:
                flag = (1, identifier_up)
                break
            elif sum(np.diag(np.fliplr(i))) == 4:
                flag = (1, identifier_up)
                break
            else:
                pass

        if flag[0]:
            return flag
        else:
            pass

        # Draw verification
        empty_flag = 0
        empty = ''
        for i in cols:
            for j in range(0, 5):
                if self.board[i][j] == empty:
                    empty_flag = 1
                    break
                else:
                    pass

        if not flag[0] and not empty_flag:
            flag = (2, '')
        else:
            pass

        return flag

    def distribute_points(self):  # Pontos são gravados e atualizados.

        # winner:

        with open(f'{self.playing}.txt') as file:
            element = file.readlines()
            element = list(map(lambda x: x.rstrip('\n'), element))

        element[0] = str(int(element[0]) + 1)

        with open(f'{self.playing}.txt', 'w') as text:
            text.writelines([f'{element[0]}', f'\n{element[1]}'])

        # Loser:

        with open(f'{self.in_hold_player}.txt') as archive:
            element_2 = archive.readlines()
            element_2 = list(map(lambda x: x.rstrip('\n'), element_2))

        element_2[1] = str(int(element_2[1]) + 1)

        with open(f'{self.in_hold_player}.txt', 'w') as arch:
            arch.writelines([f'{element_2[0]}', f'\n{element_2[1]}'])

