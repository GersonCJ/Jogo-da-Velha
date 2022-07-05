import os


class User:  # Criação da classe User responsável por criar e averiguar Usuários existentes.

    def __init__(self, nome: str):
        self.__name = nome

    @property
    def name(self):
        return self.__name

    def __str__(self):
        return self.name

    def get_history(self, name_id):
        pass

    def __create_user(self, nome):

        with open(f"{nome}.txt", 'w') as file:
            file.writelines(['0', '\n0'])

    def check_user(self, name):
        if os.path.isfile(f'{name}.txt'):
            print('Esse usuário já existe ! Favor criar um novo usuário.')
        else:
            return self.__create_user(name)
