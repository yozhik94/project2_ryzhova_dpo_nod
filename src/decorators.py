import copy
import time
from functools import wraps
from typing import Any, Callable


def handle_db_errors(func: Callable) -> Callable:
    """
    Декоратор для безопасной, транзакционной обработки ошибок.
    Работает с копией данных и возвращает оригинал в случае ошибки.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not args:
            print("Системная ошибка: Не удалось получить данные для операции.")
            return None

        metadata_copy = copy.deepcopy(args[0])
        new_args = (metadata_copy,) + args[1:]

        try:
            return func(*new_args, **kwargs)
        except (KeyError, ValueError) as e:
            print(f"Ошибка: {e}")
            return args[0]
        except Exception:
            # Убрана длинная строка
            print("Ошибка: Не удалось выполнить команду. Проверьте синтаксис.")
            return args[0]
    return wrapper


def confirm_action(action_name: str) -> Callable:
    """
    Безопасный декоратор для подтверждения действий.
    Возвращает оригинал данных при отмене.
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not args:
                print("Системная ошибка: Не удалось получить данные для операции.")
                return None

            try:
                # Убрана длинная строка
                prompt_text = f'Вы уверены, что хотите {action_name}? [y/n]: '
                answer = input(prompt_text).lower().strip()

                if answer == 'y':
                    return func(*args, **kwargs)
                else:
                    print("Операция отменена пользователем.")
                    return args[0]
            except (KeyboardInterrupt, EOFError):
                print("\nОперация отменена пользователем.")
                return args[0]
        return wrapper
    return decorator


def log_time(func: Callable) -> Callable:
    """Декоратор для замера и вывода времени выполнения функции."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.monotonic()
        result = func(*args, **kwargs)
        end_time = time.monotonic()
        execution_time = end_time - start_time
        # Убрана длинная строка
        print(f"Функция '{func.__name__}' выполнена за {execution_time:.3f} с.")
        return result
    return wrapper


def create_cacher() -> Callable:
    """Создает и возвращает функцию кэширования с замыканием."""
    _cache: dict[str, Any] = {}

    def cache_result(key: str, value_func: Callable[[], Any]) -> Any:
        if key in _cache:
            print("(результат из кэша)")
            return _cache[key]
        result = value_func()
        _cache[key] = result
        return result
    return cache_result

