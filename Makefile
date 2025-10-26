# Установка зависимостей
install:
	poetry install

# Запуск проекта из виртуального окружения
project:
	poetry run project

# Сборка пакета
build:
	poetry build

# Тестовая публикация на PyPI
publish:
	poetry publish --dry-run

# Установка собранного пакета в систему
package-install:
	pipx install ./dist/*.whl

# Запуск линтера для проверки качества кода
lint:
	poetry run ruff check .
