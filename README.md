# Образовательные модули
## Технологии
Python 3.10, Django Rest Framework, Docker, PostgreSQL, Unittest, drf-spectacular

## Локальный запуск проекта  
Для запуска подойдёт Docker 20.10.21, Docker Compose 2.12.2.  
Клонируйте репозиторий:  
```
git clone git@github.com:ElenaChuvasheva/education.git
```
Перейдите в папку education/:
```
cd education
```
Создайте в этой папке файл .env, примеры значений:
```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
SECRET_KEY=django-insecure-eypuo#-7um8bs2y3_&x&493^7@i!7snp_c!#zncgn+6m3xnnlr
```
Запустите команду:
```
docker-compose up
```
Выполните команду сборки статики:
```
docker-compose exec web python manage.py collectstatic
```
Выполните команду применения миграций:
```
docker-compose exec web python manage.py migrate
```
При необходимости загрузите фикстуры:
```
docker-compose exec web python manage.py loaddata fixtures.json
```
Бэкенд запустится по адресу localhost.
Запуск тестов:
```
docker-compose exec web python manage.py test
```
Отчёт по покрытию тестами формируется командой
```
docker-compose exec web coverage run manage.py test
```
Посмотреть его можно, выполнив
```
docker-compose exec web coverage report
```

## Примеры запросов
schema/redoc/ - автоматически сгенерированная документация API  
for_staff_only/ - админка  
В тестовой базе данных суперпользователь admin, пароль admin.  
api/modules/ - получить список модулей
