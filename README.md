# Online Shop Backend

A production-ready e-commerce backend built with Django, Django REST Framework, PostgreSQL, Redis, Celery, RabbitMQ, Elasticsearch, and Django Channels.

---

# Features

* User Authentication (OTP)
* JWT Authentication
* Product Management
* Category Management
* Shopping Cart
* Order Management
* Wallet
* Payment Gateway (Zarinpal)
* Product Likes
* Product Comments
* Notifications
* Redis Cache
* Celery Background Tasks
* RabbitMQ Message Broker
* WebSocket Support (Channels)
* Elasticsearch Product Search
* Docker Support
* Swagger / ReDoc Documentation

---

# Requirements

* Python 3.14+
* PostgreSQL
* Redis
* RabbitMQ
* Elasticsearch
* Docker (Recommended)

---

# Clone Project

```bash
git clone <repository-url>
cd online_shop
```

---

# Create Virtual Environment

Windows

```bash
python -m venv venv
venv\Scripts\activate
```

Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create a `.env` file in the project root.

Example:

```env
DEBUG=True

SECRET_KEY=your-secret-key

DATABASE_URL=postgres://username:password@localhost:5432/online_shop

REDIS_URL=redis://127.0.0.1:6379/0

CELERY_BROKER_URL=amqp://guest:guest@localhost:5672//

CELERY_RESULT_BACKEND=rpc://

MERCHANT=your-zarinpal-merchant-id

KAVENEGAR_API_KEY=your-kavenegar-api-key

ELASTICSEARCH_HOST=http://localhost:9200
```

---

# Apply Migrations

```bash
python manage.py migrate
```

---

# Create Superuser

```bash
python manage.py createsuperuser
```

---

# Run Development Server

```bash
python manage.py runserver
```

---

# Celery

Start Celery Worker

```bash
celery -A online_shop worker -l info
```

Start Celery Beat (if used)

```bash
celery -A online_shop beat -l info
```

---

# RabbitMQ

If RabbitMQ is installed locally:

```
Broker URL

amqp://guest:guest@localhost:5672//
```

Management Panel

```
http://localhost:15672
```

Default Username

```
guest
```

Default Password

```
guest
```

---

# Redis

Default Address

```
redis://127.0.0.1:6379
```

Test Connection

```bash
python manage.py shell
```

```python
from django.core.cache import cache

cache.set("test", "hello", 60)

cache.get("test")
```

---

# Elasticsearch

Create Index

```bash
python manage.py search_index --create
```

Rebuild Index

```bash
python manage.py search_index --rebuild
```

---

# WebSocket

WebSocket URL

```
ws://127.0.0.1:8000/ws/wallet/
```

---

# API Documentation

Swagger

```
/api/schema/swagger-ui/
```

ReDoc

```
/api/schema/redoc/
```

OpenAPI Schema

```
/api/schema/
```

---

# Running Tests

```bash
pytest
```

With Coverage

```bash
coverage run -m pytest

coverage report

coverage html
```

---

# Docker

Build

```bash
docker compose build
```

Start Services

```bash
docker compose up -d
```

Stop Services

```bash
docker compose down
```

---

# Project Structure

```
online_shop/

├── users/
├── products/
├── orders/
├── payment_gateway/
├── wallet/
├── notifications/
├── transactions/
├── search/
├── config/
├── requirements.txt
├── docker-compose.yml
└── README.md
```

---

# Technologies

* Python
* Django
* Django REST Framework
* PostgreSQL
* Redis
* Celery
* RabbitMQ
* Elasticsearch
* Django Channels
* JWT
* Docker
* Swagger

---

# License

This project is intended for educational and personal development purposes.
