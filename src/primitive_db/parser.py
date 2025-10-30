import shlex


def _parse_value(value_str):
    """Преобразует строку в Python-объект (int, bool, str)."""
    value_str = value_str.strip()
    # Убираем кавычки для строк
    if value_str.startswith('"') and value_str.endswith('"'):
        return value_str[1:-1]
    if value_str.startswith("'") and value_str.endswith("'"):
        return value_str[1:-1]
    # Преобразуем булевы значения
    if value_str.lower() == 'true':
        return True
    if value_str.lower() == 'false':
        return False
    # Пытаемся преобразовать в число
    try:
        return int(value_str)
    except ValueError:
        try:
            return float(value_str)
        except ValueError:
            return value_str 

def parse_where_clause(tokens):
    """Парсит условие 'where'."""
    if not tokens or 'where' not in tokens:
        return None, tokens

    where_index = tokens.index('where')
    clause_tokens = tokens[where_index + 1:]
    if len(clause_tokens) != 3 or clause_tokens[1] != '=':
        raise ValueError("Неверный формат условия WHERE. "
                        "Ожидается 'столбец = значение'")

    column, _, value_str = clause_tokens
    return {column.strip(): _parse_value(value_str)}, tokens[:where_index]


def parse_insert_values(tokens):
    """Парсит значения для 'insert'."""
    if not tokens or tokens[0] != 'values':
        raise ValueError("Ожидалось ключевое слово 'values'")

    # shlex.split поможет обработать значения в кавычках
    values_str = ' '.join(tokens[1:])
    if not values_str.startswith('(') or not values_str.endswith(')'):
        raise ValueError("Значения для INSERT должны быть в круглых скобках")

    # Используем shlex для разделения с учетом кавычек
    splitter = shlex.shlex(values_str[1:-1], posix=True)
    splitter.whitespace = ','
    splitter.whitespace_split = True
    
    return [_parse_value(v) for v in splitter]


def parse_set_clause(tokens):
    """Парсит условие 'set' для 'update'."""
    if not tokens or 'set' not in tokens:
        raise ValueError("Ожидалось ключевое слово 'set'")

    set_index = tokens.index('set')
    where_index = tokens.index('where') if 'where' in tokens else len(tokens)

    # Все что между 'set' и 'where' (или концом строки)
    set_tokens = tokens[set_index + 1:where_index]
    if not set_tokens or len(set_tokens) % 3 != 0:
        raise ValueError("Неверный формат SET. Ожидается 'столбец = значение'")
    
    set_clause = {}
    for i in range(0, len(set_tokens), 3):
        column, equals, value_str = set_tokens[i:i+3]
        if equals != '=':
            raise ValueError("Ошибка в синтаксисе SET")
        set_clause[column.strip()] = _parse_value(value_str)

    return set_clause
