# Y_lab FastAPI project


Первое ДЗ.

### Требования перед установкой:
- установленный poetry;
- установленный docker, docker-compose;

### Установка:
- стянуть репо и перейти в папку с ним:<br>
```
git clone https://github.com/OneHandedPirate/Y_labFastAPI.git
cd Y_labFastAPI
```
- выполнить команду `make init`. Она создает последовательно выполняет следующее:
  - создает файл `.env` со следующим набором переменных:
    ```
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    POSTGRES_HOST=localhost
    POSTGRES_PORT=5432
    ```
  - устанавливает зависимости проекта в новое окружение `poetry`;  
  - активирует это окружение;

### Запуск:
- выполнить команду `make up`, которая:

    - поднимает docker-compose с БД с настройками из файла `.env` и ждет ее инициализации 5 секунды;
    - накатывает на БД alembic-миграции;
    - запускает приложение;
    