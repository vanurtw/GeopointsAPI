# 🌍 Geopoints API - Геосервис с JWT аутентификацией

<div align="center">

![Django](https://img.shields.io/badge/Django-4.2-092E20?logo=django&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-4169E1?logo=postgresql&logoColor=white)
![JWT](https://img.shields.io/badge/JWT-Authentication-000000?logo=jsonwebtokens&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/Nginx-1.24-009639?logo=nginx&logoColor=white)

**REST API для работы с географическими точками на карте с JWT аутентификацией**

</div>


## 🌟 Особенности

| Функция | Статус | Описание |
|---------|--------|----------|
| 🔐 **JWT аутентификация** | ✅ Готово | Собственная реализация без сторонних библиотек |
| 🗺️ **Географический поиск** | ✅ Готово | Радиусный поиск точек на карте |
| 💬 **Сообщения к точкам** | ✅ Готово | Сообщения к точкам|
| 🐳 **Docker контейнеризация** | ✅ Готово | Полная изоляция всех сервисов |
| 🚀 **Производственный стек** | ✅ Готово | Nginx, PostgreSQL, Adminer |
| 📊 **RESTful API** | ✅ Готово | Полное соответствие REST принципам |
| 🧪 **Тестирование** | ✅ Готово| Покрытие unit-тестами |
| 📚 **Документация** | ✅ Готово | Полная документация SwaggerAPI |


## 🏗️ Архитектура

### Компоненты системы:

- **Django** - основной бэкенд фреймворк
- **PostgreSQL** - база данных
- **Nginx** - обратный прокси и статика
- **Adminer** - веб-интерфейс управления БД
- **Docker** - контейнеризация всех сервисов
- **JWT** - собственная реализация токенов

## 🚀 Запуск проекта

### 1. Клонируйте репозиторий
```git clone https://github.com/vanurtw/GeopointsAPI.git```


``` cd GeopointsAPI```
### 2. Настройте переменные окружения 
Создайте файл ***.env*** на одном уровне с фаулом **compose.yml** 

Добавте в него переменные среды:

*DB_NAME=DB_NAME*
*DB_USER=DB_USER*
*DB_PASSWORD=DB_PASSWROD*
*DB_HOST=dbps* ***# Закоментировать для запуска вне докера***
*DB_PORT=5432*
*SECRET_KEY=SEKRET_KEY*

### 3. Запустите проект через Dcoker

Запуск всех контейнеров: ```dcocker compose up --build```

Примените миграции: ```docker-compose exec geopoints python manage.py migrate```

Создайте суперпользователя: ```docker-compose exec geopoints python manage.py createsuperuser```

Можно загрузить начальные данные для БД (опционально): ```docker-compose exec geopoints python manage.py loaddata db.json```

Запуск всех тестов ```docker compose exex geopoints python manage.py test```

### Доступ к сервисам

|Сервис|URL|Описание|
|------|---|--------|
|🚀 API	|http://localhost:80|REST API
👨‍💼 Adminer|http://localhost:8080|Управление БД
👑 Админка Django|http://localhost:8000/admin|Администрирование
📚 API Документация|http://127.0.0.1:8000/swagger/|Swagger/Redoc


### Основные Endpoint

|Метод|Endpoint|Описание|Аутентификация|
|-----|--------|--------|--------------|
|POST|/auth/registration/|Регистрация пользователя|❌|
|POST|/auth/token/|Получение JWT токенов|❌|
|POST|/auth/token/refresh/|Обновление токенов|✅|
|||
GET|/points/|Список точек пользователя|✅|
POST|/points/|Создание точки|✅|
GET|/points/search/|Поиск точек в радиусе|✅|
|||
GET|/points/messages/|Получение сообщений пользователя|✅|
POST|/points/messages/|Создание сообщения|✅|
GET|/points/messages/search/|Поиск сообщений в радиусе|✅|


## 🔐 Аутентификация

Реализована собственная система аутентификации на основе JWT (JSON Web Tokens) без использования сторонних библиотек (SimpleJWT, PyJWT). Система обеспечивает безопасную аутентификацию и авторизацию пользователей с механизмом обновления токенов.

***Использование токенов: Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...***

*В setting.py можно настроить время жизни каждого токена, а так же имя загооловка передаваемого в Authorization*

[Файл конфигурации](geopoints-docker/geopoints/api_auth/services.py)

#### Свой бэкэнд аутентификации django
```python
class AuthenticationJWT(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_header = settings.JWT['AUTH_HEADER']
        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            return None, None
        parts = token.split()
        if len(parts) != 2 or parts[0] != auth_header:
            raise AuthenticationFailed(
                'Invalid Authorization header format. Expected: Bearer <token>',
                code='invalid_header'
            )
        head_token, token = parts
        try:
            header_bs64, payload_bs64, signature = token.split('.')
        except ValueError:
            raise AuthenticationFailed('Incorrect token form', code='invalid_token')
        if not TokenJWT.validate_signature(header_bs64, payload_bs64, signature):
            raise AuthenticationFailed('Signature verification failed', code='invalid_token')
        try:
            decode_payload = TokenJWT.decode_bs64(payload_bs64)
        except:
            raise AuthenticationFailed('Cannot decode token', code='decode_error')
        if not TokenJWT.validate_token(decode_payload, 'access'):
            raise AuthenticationFailed('Invalid token', code='invalid_token')
        user = get_object_or_404(get_user_model(), id=decode_payload['id'])
        return user, token
```

#### Сервис по созданию пары токенов access и refresh





#### Регистрация пользователя

##### Запрос с пустым телом запроса
![Запрос с пустым телом](./screenshots/а1.PNG)
##### Запрос на регистрацию с невалидными данными
![Запрос на регистрацию](./screenshots/а2.PNG)
##### Успешная регистрация пользователя
![Успешная регистрация](./screenshots/a3.PNG)


#### Получение и обновление токенов

##### Успешное получение токенов
![Токен](./screenshots/a4.PNG)

##### Получение токенов с невалидными данными
![Токен](./screenshots/а5.PNG)

##### Успешное обновление пары токенов
![Токен](./screenshots/a6.PNG)

##### Обновление токенов с невалидным refresh токеном
![Токен](./screenshots/a7.PNG)

## 🗺️ Работа с точками

#### 🎯 Выбор алгоритма вычисления расстояний

Для вычисления расстояния между географическими точками была выбрана формула гаверсинусов, обеспечивающая высокую точность расчетов на сферической поверхности Земли.

[Файл конфигурации](geopoints-docker/geopoints/api_geopoints/services.py)

```python
    def calculate_distance(lat1, lon1, lat2, lon2):
        '''Нахождение расстояния между двумя точками'''
        R = 6371

        lat1_rad = math.radians(float(lat1))
        lon1_rad = math.radians(float(lon1))
        lat2_rad = math.radians(float(lat2))
        lon2_rad = math.radians(float(lon2))

        delta_lat_rad = lat2_rad - lat1_rad
        delta_lon_rad = lon2_rad - lon1_rad

        cos_lat = math.cos(lat1_rad) * math.cos(lat2_rad)
        sin_lat = math.sin(delta_lat_rad / 2)
        sin_lon = math.sin(delta_lon_rad / 2)

        a = sin_lat ** 2 + cos_lat * sin_lon ** 2
        distance = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        return distance * R
```
#### ⚡ Оптимизация производительности

Для ускорения поиска ближайших точек используется двухэтапный алгоритм:

1. нахождение точек в пределах ограничивающего прямоугольника
2. Точный расчет для каждой точки

```python
    @staticmethod
    def get_bounding_box(latitude, longitude, radius) -> tuple:
        '''Возвращение ограничивающего прямоугольника для предварительной фильотрации'''
        KM_PER_DEGREE_LAT = 111.0

        delta_lat = float(radius) / KM_PER_DEGREE_LAT

        rad_lat = math.radians(latitude)
        delta_lon = float(radius) / (KM_PER_DEGREE_LAT * math.cos(rad_lat))

        max_lat = float(latitude) + delta_lat
        min_lat = float(latitude) - delta_lat
        max_lon = float(longitude) + delta_lon
        min_lon = float(longitude) - delta_lon
        return min_lat, max_lat, min_lon, max_lon
```
```python
def is_point_in_radius(lat1, lon1, lat2, lon2, radius):
        '''Возвращает находится ли точка в радиусе и дистанцию'''
        distance = Location.calculate_distance(lat1, lon1, lat2, lon2)
        return distance <= radius, distance
```
#### 🌍	 Геопространственный поиск

	Все точки в БД -> Быстрая Фильтрация -> Точный расчет -> Результат


#### 🔍 Сравнение подходов
##### 🆚 Почему не использован DjangoGeo + PostGIS?
|Критерий|Наш алгоритм|DjangoGeo + PostGIS|
|--------|------------|-------------------|
Зависимости|🟢Только Python|🔴 PostGIS, GDAL, GEOS
Производительность|🟢 Оптимизирована|🟡 Зависит от БД|
Точность|🟢 ~0.5% погрешность|🟢 Высокая|
Гибкость|🟢 Полный контроль|🟡 Ограничена ORM|


##### Получение всех точек пользователя
![Получение всех точек пользователя](./screenshots/p1.PNG)

##### Ошибка получения точек пользователя, т.к. он не авторизован

![Получениет точки  ошибки  пользователя](./screenshots/p2.PNG)

##### Создание точки пользователя

![ПСоздание точки](./screenshots/p3.PNG)

##### Создание точки с невалидными данными

![ПСоздание точки](./screenshots/p4.PNG)

##### Поиск точек с указанными параметрами

![Поиск точки](./screenshots/p5.PNG)
![Поиск точки](./screenshots/p6.PNG)

## 💬 Работа с сообщениями

##### Список всех сообщений пользователя

![Сообщение](screenshots/с1.PNG)

##### Создания сообщения к точке

![Сообщение](./screenshots/c2.PNG)

##### Создание сообщения к точке с невалидными данными

![Сообщение](screenshots/с3.PNG)

##### Поиск сообщения по указанным параметрам

![Сообщение](screenshots/с4.PNG)







## 🔧 Инструменты разработки и оптимизация


• 🧩 unittest - основной фреймворк
• 🏭 Factory Boy - генерация данных
• 🐍 Faker - реалистичные тест-данные
• 🔧 Django Test Client - HTTP запросы
• 🧹 in-memory SQLite - изоляция тестов



#### 📊 Покрытие тестами
|Модуль	|Количество тестов|Статус|
|-------|-----------------|------|
|🔐 Аутентификация (JWT)|7 тестов|✅ Полное|
🗺️ Модели|3теста|✅ Полное|
📊 Сериализаторы|6 тестов|✅ Полное
🚀 API Endpoints|17 тестов|✅ Полное|



#### 🏭 Factory Boy для генерации данных

```python
class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    username = factory.LazyFunction(lambda: fake.user_name())
    email = factory.LazyFunction(lambda: fake.email())
    password = factory.PostGenerationMethodCall('set_password', f'{username}12345')


class PointFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Point

    user = factory.SubFactory(UserFactory)
    name = factory.LazyFunction(lambda: fake.name())
    description = factory.LazyFunction(lambda: fake.text())
    latitude = factory.LazyFunction(lambda: fake.latitude())
    longitude = factory.LazyFunction(lambda: fake.longitude())


class MessageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Message

    point = factory.SubFactory(PointFactory)
    user = factory.SubFactory(UserFactory)
    content = factory.LazyFunction(lambda: fake.text())

```

### 🛠 Оптимизация запросов с Django Debug Toolbar


До оптимизации система выполняла N+1 запросов для получения связанных данных. Например, при загрузке списка сообщений.

Это приводило к:
- 📉 Высокой нагрузке на базу данных
- ⏱ Медленному отклику API
- 🔄 Ненужным дублирующимся запросам

**Была внедрена стратегия SELECT_RELATED, которая преобразует N+1 запросов в единый JOIN запрос**
Для анализа и подтверждения оптимизации использовался *Django Debug Toolbar*

![запросы](./screenshots/d1.PNG)







