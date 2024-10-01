# ToDoBot List
ToDoBot - телеграм бот, в котором вы можете хранить свои дела и задачи.

## Описание функций
* Создание задач
* Просмотр списка задач
* Просмотр описания задачи, ее категории и дедлайны
* Возможность закрыть задачу, если она выполнена

## Запуск бота

Установить зависимости
```
pip install -r requirements.txt
```

Применить миграции БД
```
python manage.py migrate
```

Запустить бекенд
```
python manage.py runserver
```

Создать пользователя, через которого бот будет получать токен (данные пользователя необходимо ввести в .env)
```
python manage.py createsuperuser
```

Запустить телеграм бота
```
python run.py
```

После команды /start в телеграм боте, когда пользователи будут добавлены на сервер, вы можете добавить тестовые данные с [jsonplaceholder](jsonplaceholder.typicode.com/) командой
```
python manage.py generate_random_tasks
```

Документация по api доступна по [ссылке](http://127.0.0.1:8000/api/schema/redoc/) или в [файле](redoc.yaml) проекта.

Или запустить Docker
```
docker compose -f docker-compose.yaml up -d
```
И создать там пользователя для бота
```
docker exec -it backend python manage.py createsuperuser
```

## Описание архитектуры
<dl>
<dt>1. Telegram Bot (aiogram + aiogram dialog)</dt>
<dd>Обработка команд и сообщений от пользователей, взаимодействие с бекендом для получения и отправки данных через API.</dd>
</dl>
<dl>
<dt>2. Backend (django + drf)</dt>
<dd>* Обработка запросов от бота, управление данными в базе данных, предоставление API для взаимодействия с ботом.</dd>
<dd>* Определение моделей данных для хранения информации о пользователях, задачах и категориях.</dd>
<dd>* Предоставление RESTful API для выполнения CRUD операций над данными.</dd>
</dl>
<dl>
<dt>3. БД (postgresql)</dt>
<dd> В проекте используется современная, производительная и распространенная СУБД</dd>
</dl>


## Описание трудностей

<dl>
<dt>aiogram-dialog</dt>
<dd>Я работал с aiogram, но с aiogram-dialog и его системой окон сталкиваться не приходилось, пришлось учиться работать с виджетами Aiogram Dialog. </dd>
<dd>I18NFormat не форматирует так же, как Format. Поэтому пришлось форматировать текст обходными путями.</dd>
</dl>


## ToDo
* Настроить уведомления для пользователей об их задачах

## Технологии
* Python 3.12
* Django
* DRF
* PostgeSQL
* Aiogram
* Aiogram-dialog
* Docker
