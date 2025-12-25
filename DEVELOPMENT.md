# Development vs Production Setup

This project supports two distinct workflows:

## 🔧 Development Mode (Recommended for Development)

Run Django locally on your machine while using Docker only for services (PostgreSQL, Redis, MinIO).

### Setup

1. **Copy environment file:**
   ```bash
   copy .env.development .env
   ```

2. **Start Docker services only:**
   ```bash
   dev.bat start
   ```
   Or manually:
   ```bash
   docker-compose -f docker-compose.dev.yml --env-file .env.development up -d
   ```

3. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations:**
   ```bash
   python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Django locally:**
   ```bash
   python manage.py runserver
   ```

### Access Points (Development)
- Django: http://localhost:8000
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- MinIO Console: http://localhost:9001 (admin/secure_minio_password_123)
- MinIO API: http://localhost:9000

### Development Commands
```bash
dev.bat start      # Start services
dev.bat stop       # Stop services
dev.bat restart    # Restart services
dev.bat logs       # View logs
dev.bat clean      # Remove all data
```

---

## 🚀 Production Mode (Full Docker)

Run everything in Docker including Django web server.

### Setup

1. **Copy environment file:**
   ```bash
   copy .env.production .env.production
   ```
   Edit `.env.production` and change all passwords!

2. **Build and start all services:**
   ```bash
   prod.bat build
   ```
   Or manually:
   ```bash
   docker-compose -f docker-compose.prod.yml --env-file .env.production up --build -d
   ```

3. **Run migrations:**
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
   ```

4. **Create superuser:**
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
   ```

### Access Points (Production)
- Django (via Nginx): http://localhost
- MinIO Console: http://localhost:9001

### Production Commands
```bash
prod.bat start     # Start all services
prod.bat stop      # Stop all services
prod.bat restart   # Restart services
prod.bat logs      # View all logs
prod.bat build     # Rebuild and start
```

---

## 📁 File Structure

```
.env.development      # Local Django + Docker services
.env.production       # Full Docker production
docker-compose.dev.yml   # Services only (no web)
docker-compose.prod.yml  # All services including web
dev.bat              # Development helper script
prod.bat             # Production helper script
```

## 🔄 Switching Between Modes

**To Development:**
```bash
prod.bat stop
copy .env.development .env
dev.bat start
python manage.py runserver
```

**To Production:**
```bash
dev.bat stop
prod.bat build
```

## 💡 Tips

- **Development**: Fast iteration, easy debugging, direct access to all services
- **Production**: Test full deployment, Nginx integration, production-like environment
- Never commit `.env`, `.env.development`, or `.env.production` with real passwords
- Use `.env.example` as a template for new environments
