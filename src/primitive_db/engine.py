# src/primitive_db/engine.py
import shlex
import sys

from src.primitive_db import core, parser, utils


def print_help():
    """Выводит справочную информацию."""
    print("\n*** Управление таблицами ***")
    print("create_table <имя> <столбец1:тип> ... - создать таблицу")
    print("list_tables - показать список таблиц")
    print("drop_table <имя> - удалить таблицу")
    print("\n*** Операции с данными ***")
    print("insert into <имя> values (...) - вставить запись")
    print("select from <имя> [where <условие>] - выбрать записи")
    print("update <имя> set <столбец=значение> where <условие> - обновить записи")
    print("delete from <имя> where <условие> - удалить записи")
    print("info <имя> - информация о таблице")
    print("\n*** Общие команды ***")
    print("help - эта справка")
    print("exit - выход\n")


def run():
    """Основной цикл обработки команд."""
    print("Добро пожаловать в базу данных!")
    print_help()

    while True:
        # Метаданные загружаются на каждой итерации, а данные таблиц - по требованию
        metadata = utils.load_metadata()
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
            
            # --- Команды управления таблицами ---
            elif command == 'create_table':
                if len(args) < 3:
                    raise ValueError("Нужно имя таблицы и хотя бы один столбец.")
                updated_meta = core.create_table(metadata, args[1], args[2:])
                utils.save_metadata(updated_meta)
            
            elif command == 'list_tables':
                core.list_tables(metadata)

            elif command == 'drop_table':
                if len(args) != 2:
                    raise ValueError("Нужно только имя таблицы.")
                table_name = args[1]
                updated_meta = core.drop_table(metadata, table_name)
                utils.save_metadata(updated_meta)
                # Также удаляем файл с данными, если он был
                utils.save_table_data(table_name, [])

            # --- CRUD-команды ---
            elif command == 'insert':
                if len(args) < 4 or args[1] != 'into':
                    raise ValueError("Синтаксис: insert into <имя> values (...)")
                table_name = args[2]
                values = parser.parse_insert_values(args[3:])
                table_data = utils.load_table_data(table_name)
                updated_data = core.insert(metadata, table_name, table_data, values)
                utils.save_table_data(table_name, updated_data)

            elif command == 'select':
                if len(args) < 3 or args[1] != 'from':
                    raise ValueError("Синтаксис: select from <имя> [where ...]")
                table_name = args[2]
                where_clause, _ = parser.parse_where_clause(args)
                table_data = utils.load_table_data(table_name)
                schema = metadata.get(table_name, {}).get('columns', [])
                core.select(table_data, schema, where_clause)

            elif command == 'update':
                table_name = args[1]
                where_clause, _ = parser.parse_where_clause(args)
                set_clause = parser.parse_set_clause(args)
                table_data = utils.load_table_data(table_name)
                updated_data = core.update(table_data, set_clause, where_clause)
                utils.save_table_data(table_name, updated_data)
            
            elif command == 'delete':
                if len(args) < 3 or args[1] != 'from':
                    raise ValueError("Синтаксис: delete from <имя> where ...")
                table_name = args[2]
                where_clause, _ = parser.parse_where_clause(args)
                table_data = utils.load_table_data(table_name)
                updated_data = core.delete(table_data, where_clause)
                utils.save_table_data(table_name, updated_data)

            elif command == 'info':
                if len(args) != 2:
                    raise ValueError("Нужно только имя таблицы.")
                table_name = args[1]
                table_data = utils.load_table_data(table_name)
                core.info(metadata, table_name, table_data)

            else:
                print(f"Неизвестная команда: '{command}'. Введите 'help' для справки.")

        except (ValueError, KeyError) as e:
            print(f"Ошибка: {e}")
        except (KeyboardInterrupt, EOFError):
            print("\nДо свидания!")
            sys.exit()
        except Exception as e:
            print(f"Произошла критическая ошибка: {e}")

