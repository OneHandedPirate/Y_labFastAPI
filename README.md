# Y_lab FastAPI project


Третье ДЗ. Исправлено. Добавлены тайпхинты, инвалидация кэша не flushall.

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
