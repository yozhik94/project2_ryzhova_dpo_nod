from src.decorators import confirm_action, handle_db_errors

# ALLOWED_TYPES вынесен сюда, так как используется только в create_table
ALLOWED_TYPES = {'int', 'str', 'bool'}

@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает новую таблицу с проверками."""
    if table_name in metadata:
        # Используем raise для централизованной обработки ошибок
        raise ValueError(f'Таблица "{table_name}" уже существует.')

    formatted_columns = [('ID', 'int')]
    for col in columns:
        if ':' not in col:
            raise ValueError(
                f"Неверный формат столбца: {col}. Ожидается 'имя:тип'."
            )

        name, type_name = col.split(':', 1)
        if type_name not in ALLOWED_TYPES:
            raise ValueError(f"Неподдерживаемый тип данных: {type_name}.")
        formatted_columns.append((name, type_name))

    metadata[table_name] = {
        "columns": formatted_columns,
        "data": []
    }
    
    column_str = ', '.join([f'{n}:{t}' for n, t in formatted_columns])
    print(f'Таблица "{table_name}" успешно создана со столбцами: {column_str}')
    return metadata

@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata, table_name):
    """Удаляет таблицу после подтверждения."""
    if table_name not in metadata:
        # Используем raise для централизованной обработки ошибок
        raise KeyError(f'Таблица "{table_name}" не существует.')
    
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

# list_tables не работает с файлами и не вызывает стандартных ошибок,
# поэтому декораторы здесь не нужны.
def list_tables(metadata):
    """Выводит список всех таблиц."""
    if not metadata:
        print("База данных не содержит таблиц.")
        return
    
    print("Список таблиц:")
    for table_name in metadata:
        print(f"- {table_name}")




