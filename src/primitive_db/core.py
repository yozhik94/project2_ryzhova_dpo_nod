# src/primitive_db/core.py
from prettytable import PrettyTable

from src.decorators import confirm_action, handle_db_errors, log_time

ALLOWED_TYPES = {'int', 'str', 'bool'}


@handle_db_errors
def create_table(metadata, table_name, columns):
    """Создает новую таблицу с проверками."""
    if table_name in metadata:
        raise ValueError(f'Таблица "{table_name}" уже существует.')
    
    formatted_columns = [('ID', 'int')]
    for col in columns:
        if ':' not in col:
            raise ValueError(f"Неверный формат столбца: {col}. Ожидается 'имя:тип'.")

        name, type_name = col.split(':', 1)
        if type_name not in ALLOWED_TYPES:
            raise ValueError(f"Неподдерживаемый тип данных: {type_name}.")
        formatted_columns.append((name, type_name))

    metadata[table_name] = {"columns": formatted_columns}
    column_str = ', '.join([f'{n}:{t}' for n, t in formatted_columns])
    print(f'Таблица "{table_name}" успешно создана со столбцами: {column_str}')
    return metadata

@confirm_action("удаление таблицы")
@handle_db_errors
def drop_table(metadata, table_name):
    """Удаляет таблицу после подтверждения."""
    if table_name not in metadata:
        raise KeyError(f'Таблица "{table_name}" не существует.')
    
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

# --- Новые CRUD-функции ---

def _validate_type(value, expected_type):
    """Проверяет соответствие типа значения ожидаемому типу."""
    type_map = {'str': str, 'int': int, 'bool': bool}
    if expected_type not in type_map:
        return False 
    if expected_type == 'bool' and isinstance(value, int):
        return True 
    return isinstance(value, type_map[expected_type])

@log_time
def insert(metadata, table_name, table_data, values):
    """Добавляет новую запись в таблицу."""
    if table_name not in metadata:
        raise KeyError(f"Таблица '{table_name}' не найдена.")

    schema = metadata[table_name]['columns'][1:] # Пропускаем ID
    if len(values) != len(schema):
        raise ValueError(
            f"Ожидалось {len(schema)} значений, но было передано {len(values)}"
        )

    new_row = {}
    for i, (col_name, col_type) in enumerate(schema):
        value = values[i]
        if not _validate_type(value, col_type):
            raise ValueError(
                f"Неверный тип для столбца '{col_name}'. "
                f"Ожидался {col_type}, получен {type(value).__name__}"
            )
        new_row[col_name] = value

    # Генерация ID
    max_id = max([row['ID'] for row in table_data], default=0)
    new_row['ID'] = max_id + 1
    
    table_data.append(new_row)
    print(f"Запись с ID={new_row['ID']} успешно добавлена в таблицу '{table_name}'.")
    return table_data


def select(table_data, schema, where_clause=None):
    """Выбирает и выводит данные из таблицы."""
    if where_clause:
        key, value = list(where_clause.items())[0]
        result_data = [row for row in table_data if row.get(key) == value]
    else:
        result_data = table_data

    # Вывод в красивом формате
    if not result_data:
        print("Не найдено записей, удовлетворяющих условию.")
        return

    table = PrettyTable()
    table.field_names = [col[0] for col in schema]
    for row in result_data:
        table.add_row([row.get(col_name) for col_name in table.field_names])
    
    print(table)


@log_time
@confirm_action("обновление записей")
def update(table_data, set_clause, where_clause):
    """Обновляет записи в таблице."""
    if not where_clause:
        raise ValueError("Операция UPDATE требует условие WHERE.")

    key, value = list(where_clause.items())[0]
    updated_count = 0
    for row in table_data:
        if row.get(key) == value:
            row.update(set_clause)
            updated_count += 1
    
    if updated_count > 0:
        print(f"Успешно обновлено {updated_count} записей.")
    else:
        print("Не найдено записей для обновления.")
    return table_data

@log_time
@confirm_action("удаление записей")
def delete(table_data, where_clause):
    """Удаляет записи из таблицы."""
    if not where_clause:
        raise ValueError("Операция DELETE требует условие WHERE.")

    key, value = list(where_clause.items())[0]
    
    initial_len = len(table_data)
    # Создаем новый список без удаленных элементов
    new_table_data = [row for row in table_data if row.get(key) != value]
    
    deleted_count = initial_len - len(new_table_data)
    if deleted_count > 0:
        print(f"Успешно удалено {deleted_count} записей.")
    else:
        print("Не найдено записей для удаления.")
    return new_table_data

def info(metadata, table_name, table_data):
    """Выводит информацию о таблице."""
    if table_name not in metadata:
        raise KeyError(f"Таблица '{table_name}' не найдена.")

    schema_str = ', '.join(
        [f'{col[0]}:{col[1]}' for col in metadata[table_name]['columns']]
    )
    print(f"Таблица: {table_name}")
    print(f"Столбцы: {schema_str}")
    print(f"Количество записей: {len(table_data)}")





