import shlex
import sys

from src.primitive_db import core, utils

METADATA_FILE = "db_meta.json"

def print_help():
    """Выводит справочную информацию."""
    print("\n*** Процесс работы с таблицей ***")
    print("Функции:")
    print("<command> create_table <имя_таблицы> <столбец1:тип> ... - создать таблицу")
    print("<command> list_tables - показать список всех таблиц")
    print("<command> drop_table <имя_таблицы> - удалить таблицу")
    print("\nОбщие команды:")
    print("<command> exit - выход из программы")
    print("<command> help - справочная информация\n")

def run():
    """Основной цикл обработки команд."""
    print("Добро пожаловать в Базу Данных!")
    print_help()

    while True:
        metadata = utils.load_metadata(METADATA_FILE)
        try:
            user_input = input(">>> Введите команду: ").strip()
            if not user_input:
                continue
            
            args = shlex.split(user_input)
            command = args[0].lower()

            if command == 'exit':
                print("До свидания!")
                break
            elif command == 'help':
                print_help()
            elif command == 'create_table':
                if len(args) < 3:
                    print("Ошибка: Недостаточно аргументов для create_table.")
                    continue
                metadata = core.create_table(metadata, args[1], args[2:])
                utils.save_metadata(METADATA_FILE, metadata)
            elif command == 'list_tables':
                core.list_tables(metadata)
            elif command == 'drop_table':
                if len(args) != 2:
                    print(
                        "Ошибка: Команда drop_table требует ровно один аргумент "
                        "(имя таблицы)."
                    )
                metadata = core.drop_table(metadata, args[1])
                utils.save_metadata(METADATA_FILE, metadata)
            else:
                print(f"Функции <{command}> нет. Попробуйте снова.")

        except (KeyboardInterrupt, EOFError):
            print("\nДо свидания!")
            sys.exit()
        except Exception as e:
            print(f"Произошла непредвиденная ошибка: {e}")

