from menu import menu


if __name__ == '__main__':
    try:
        menu()
    except KeyboardInterrupt:
        print('\nEncerrado abruptamente...')

