# Django Docker Project

A Django REST API project with PostgreSQL, Redis, MinIO, Gunicorn, and Nginx using Docker Compose.

## 📋 Overview

This project supports two distinct workflows:
- **Development Mode**: Run Django locally with Docker services only (PostgreSQL, Redis, MinIO)
- **Production Mode**: Run everything in Docker including Django with Gunicorn and Nginx

## 🚀 Quick Start

### Windowsm




**Development:**
```bash
dev.bat setup
python manage.py runserver
```

**Production:**
```bash
prod.bat build
```

### Linux/macOS

**Development:**
```bash
chmod +x dev.sh
./dev.sh setup
python manage.py runserver
```

**Production:**
```bash
chmod +x prod.sh
./prod.sh build
```

## 📚 Documentation

- **[GETTING_STARTED.md](GETTING_STARTED.md)** - Complete beginner's guide ⭐ START HERE
- [PLATFORM_SETUP.md](PLATFORM_SETUP.md) - Platform-specific setup (Windows/Linux/macOS)
- [DEVELOPMENT.md](DEVELOPMENT.md) - Detailed development and production setup
- [TEST_README.md](TEST_README.md) - Testing guide and test structure
- [QUICK_REFERENCE.md](QUICK_REFERENCE.md) - Command reference for Windows and Linux/macOS
- [DOCS_INDEX.md](DOCS_INDEX.md) - Documentation navigator

## 🔧 Services

- **Django**: REST API with Django REST Framework
- **PostgreSQL**: Primary database
- **Redis**: Caching and session storage
- **MinIO**: S3-compatible object storage
- **Nginx**: Reverse proxy (production only)
- **Gunicorn**: WSGI server (production only)

## 🌐 Access Points

**Development Mode:**
- Django API: http://localhost:8000
- MinIO Console: http://localhost:9001
- PostgreSQL: localhost:5432
- Redis: localhost:6379

**Production Mode:**
- Django API (via Nginx): http://localhost
- MinIO Console: http://localhost:9001

## 📦 Project Structure

```
├── account/              # User authentication and profiles
├── document/             # Document management with RBAC
├── sannap_project/       # Django settings and configuration
├── docker-compose.dev.yml   # Development services only
├── docker-compose.prod.yml  # Production full stack
├── dev.bat / dev.sh         # Development helper scripts
├── prod.bat / prod.sh       # Production helper scripts
├── .env.development         # Development environment variables
├── .env.production          # Production environment variables
└── requirements.txt         # Python dependencies
```

## 🔐 Security Notes

- Never commit `.env`, `.env.development`, or `.env.production` files
- Change all default passwords in production
- Use `.env.example` as a template for new environments