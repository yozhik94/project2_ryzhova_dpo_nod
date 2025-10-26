import prompt


def welcome():
    """
    Основной цикл программы.
    Приветствует пользователя и обрабатывает команды.
    """
    print("***")
    print("<command> exit - выйти из программы")
    print("<command> help - справочная информация")

    while True:
        command = prompt.string("Введите команду: ")
        if command == 'exit':
            print("До свидания!")
            break
        elif command == 'help':
            print("<command> exit - выйти из программы")
            print("<command> help - справочная информация")
        else:
            print(f"Неизвестная команда: {command}")
