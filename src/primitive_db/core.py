ALLOWED_TYPES = {'int', 'str', 'bool'}

def create_table(metadata, table_name, columns):
    """Создает новую таблицу с проверками."""
    if table_name in metadata:
        print(f'Ошибка: Таблица "{table_name}" уже существует.')
        return metadata

    formatted_columns = [('ID', 'int')]  # Автоматически добавляем ID
    for col in columns:
        if ':' not in col:
            print(f"Некорректное значение: {col}. Попробуйте снова.")
            return metadata

        name, type_name = col.split(':', 1)
        if type_name not in ALLOWED_TYPES:
            print(f"Некорректное значение: {type_name}. Попробуйте снова.")
            return metadata
        formatted_columns.append((name, type_name))

    metadata[table_name] = {
        "columns": formatted_columns,
        "data": [] # Место для будущих данных
    }
    
    column_str = ', '.join([f'{n}:{t}' for n, t in formatted_columns])
    print(f'Таблица "{table_name}" успешно создана со столбцами: {column_str}')
    return metadata

def drop_table(metadata, table_name):
    """Удаляет таблицу."""
    if table_name not in metadata:
        print(f'Ошибка: Таблица "{table_name}" не существует.')
        return metadata
    
    del metadata[table_name]
    print(f'Таблица "{table_name}" успешно удалена.')
    return metadata

def list_tables(metadata):
    """Выводит список всех таблиц."""
    if not metadata:
        print("База данных не содержит таблиц.")
        return
    
    print("Список таблиц:")
    for table_name in metadata:
        print(f"- {table_name}")

