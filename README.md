# Y_lab FastAPI project


Третье ДЗ.

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


#### Примечания:

- **Инвалидация** кэша реализована довольно топорно: кэш полностью обнуляется при создании/обновлении/удалении любой сущности. Не самое лучшее решение (мягко говоря), что позволяет избежать множества проблем с хранением устаревших данных в кэше. К тому же, в реальном приложении ресторана изменяться наши сущности будут гораздо реже, чем время хранения данных в кэше (3600 секунд, можно изменить в `app/core/settings.py`, переменная `CACHE_EXPIRE_TIME`).
