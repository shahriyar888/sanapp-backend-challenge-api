# Django Docker Project

A Django project with Redis, MinIO, Gunicorn, and Nginx using Docker Compose.

## Services

- **Django**: Web application with Gunicorn
- **PostgreSQL**: Database
- **Redis**: Caching
- **MinIO**: Object storage
- **Nginx**: Reverse proxy

## Quick Start

1. Build and start services:
```bash
docker-compose up --build
```

2. Run migrations:
```bash
docker-compose exec web python manage.py migrate
```

3. Create superuser:
```bash
docker-compose exec web python manage.py createsuperuser
```

## Access Points

- Django app: http://localhost
- MinIO console: http://localhost:9001 (admin/minioadmin)
- Redis: localhost:6379