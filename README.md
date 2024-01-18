# Тестовое задание ООО Простые Решения
### Задача
· 	Реализовать Django + Stripe API бэкенд со следующим функционалом и условиями:
· 	Django Модель Item с полями (name, description, price)
· 	API с двумя методами:
· 	GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос stripe.checkout.Session.create(...) и полученный session.id выдаваться в результате запроса
· 	GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, на которой будет информация о выбранном Item и кнопка Buy. По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, получение session_id и далее с помощью JS библиотеки Stripe происходить редирект на Checkout форму stripe.redirectToCheckout(sessionId=session_id)
· 	Запуск используя Docker
· 	Использование environment variables
· 	Просмотр Django Моделей в Django Admin панели
· 	Запуск приложения на удаленном сервере, доступном для тестирования
· 	Модель Order, в которой можно объединить несколько Item и сделать платёж в Stripe на содержимое Order c общей стоимостью всех Items
· 	Модели Discount, Tax, которые можно прикрепить к модели Order и связать с соответствующими атрибутами при создании платежа в Stripe - в таком случае они корректно отображаются в Stripe Checkout форме.
· 	Добавить поле Item.currency, создать 2 Stripe Keypair на две разные валюты и в зависимости от валюты выбранного товара предлагать оплату в соответствующей валюте
· 	Реализовать не Stripe Session, а Stripe Payment Intent.

### Запуск проекта
Клонировать репозиторий и перейти в него в командной строке:
```
git clone git@github.com:pestovaarina/fintech.git
```

```
cd stripe_api
```
Создать .env файл, с параметрами:
``` 
    STRIPE_PUBLIC_KEY=<your_stripe_public_key>
    STRIPE_SECRET_KEY=<your_stripe_secret_key>
    POSTGRES_DB=<stripe>
    DB_NAME=postgres
    POSTGRES_USER=<your postgres_username>
    POSTGRES_PASSWORD=<your postgres_password>
    DB_HOST=db
    DB_PORT=5432
    SECRET_KEY=<secret_key>
```

Запустить docker-compose:

```
docker-compose up -d
```

Выполнить миграции:

```
docker-compose exec backend python manage.py migrate
```

Собрать и переместить в volume статику::

```
docker-compose exec backend python manage.py collectstatic --no-input
```
```
docker-compose exec backend cp -r /app/static/. /static/
```
Создать пользователя с правами администратора:

```
docker-compose exec backend python manage.py createsuperuser
```
Перейдите на страницу http://127.0.0.1:8000/admin/ для доступа к админ-зоне проекта,
создайте несколько объектов товаров и заказов, а также Discounts и один Tax.
Пожалуйста, не добавляйте в один заказ товары с ценой в разной валюте (я еще думаю, как это решить).

```4242 4242 4242 4242``` - тестовые данные номера карты для успешного платежа

```4000 0025 0000 3155``` - тестовые данные номера карты, для которой необходима аутентификация

```4000 0000 0000 0002``` - этот платеж будет отклонен