# Y_lab FastAPI project


Четвертое ДЗ.

- Эндпоинт для древовидной структуры `menu` доступен по адресу<br>
`/api/v1/menus/all`
- Тесты для этого эндпоинта добавил в модуль `test/test_count.py`

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
- тесты `pytest` запускаются командой `make tests`, которая:
  + поднимает `docker-compose-tests.yaml`;
  + выводит в консоль результаты прогона тестов;
  + выполняет команду `docker compose -f docker-compose-tests.yaml down`
- тесты `postman` можно проходить, выполнив команду `make postman`, которая:
  + поднимает `docker-compose-postman.yaml` в detached-режиме;
  + после завершения тестов выполнить команду `make postman_down`, которая сворачивает `docker-compose-postman.yaml`
- команда `make up` запускает `docker-compose-dev.yaml` в detached-режиме;

### Примечания:
#### Синхронизация к excel:

- При изменении excel-файла нужно учитывать, что в нем записаны реальные `id` объектов базы данных, т.е. если даже мы удалим, скажем, меню `Алкогольное меню`, то при создании другого меню в `Menu.xlsx` все равно следует назначить ему `id` 3, первому подменю в нем - `id` 5, а первому блюду в нем - `id` 13 и т.д.
- Для синхронизации локального файла `Menu.xlsx` вместо тома `admin_folder` в контейнере `celery` в файле `docker-compose-dev.yaml` нужно подставить абсолютный путь до папки `app/admin` на вашей машине (например, у меня это `/home/onehandedpirate/Python/RestaurantFastAPI/app/admin`, т.е. раздел `volumes` в контейнере `celery` у меня должен выглядеть так: <br>`- /home/onehandedpirate/Python/RestaurantFastAPI/app/admin:code/app/admin`<br>).
#### Выполненные задания повышенной сложности:

- Реализовать тестовый сценарий «Проверка кол-ва блюд и подменю в меню» из Postman с помощью pytest:<br>
  реализовано в модуле `test/test_count`
- Описать ручки API в соответствий c OpenAPI:<br>
  Добавлено описание к каждому эндпоинту, так же эндпоинты сгруппированы по тэгам (к ним тоже добавлены описания).
- Достать все данные одним запросом:<br>
  `app/repositories/sqlalch.py | 98`
