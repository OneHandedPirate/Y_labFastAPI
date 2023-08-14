# Y_lab FastAPI project


Четвертое ДЗ.

- Эндпоинт для древовидной структуры `menu` доступен по адресу<br>
`/api/v1/menus/all`
- Тесты для этого эндпоинта добавил в модуль `test/test_count.py`
- Для прохождения тестов postman обязательно закомментировать задачу celery:<br>
`app/celery/tasks.py | 5`, (иначе они сломают синхронизацию с excel).

### Требования перед установкой:
- установленный docker, docker-compose;

### Установка:
- стянуть репо и перейти в папку с ним:<br>
```
git clone https://github.com/OneHandedPirate/Y_labFastAPI.git
cd Y_labFastAPI
```
- выполнить команду `make create_env`, которая создает файл `.env` с необходимым набором переменных;

### Запуск:
- тесты запускаются командой `make tests`, которая:
  + поднимает `docker-compose-tests.yaml`;
  + выводит в консоль результаты прогона тестов;
  + выполняет команду `docker compose -f docker-compose-tests.yaml down`
- команда `make up` запускает `docker-compose-dev.yaml` в detached-режиме;

### Примечания:
#### Выполненные задания повышенной сложности:

- Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest:<br>
  реализовано в модуле `test/test_count`
- Описать ручки API в соответствий c OpenAPI:<br>
  Добавлено описание к каждому эндпоинту, так же эндпоинты сгруппированы по тэгам (к ним тоже добавлены описания).
- Достать все данные одним запросом:<br>
  `app/repositories/sqlalch.py | 98`
