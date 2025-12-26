# Development vs Production Setup

This project supports two distinct workflows optimized for different use cases.

## 🔧 Development Mode (Recommended for Development)

Run Django locally on your machine while using Docker only for services (PostgreSQL, Redis, MinIO).

### Why Development Mode?
- ✅ Fast code reloading without rebuilding Docker images
- ✅ Easy debugging with breakpoints
- ✅ Direct access to Django shell and management commands
- ✅ Lower resource usage

### Setup (Windows)

1. **First time setup:**
   ```bash
   dev.bat setup
   ```
   This will:
   - Copy `.env.development` to `.env`
   - Start Docker services (PostgreSQL, Redis, MinIO)
   - Run database migrations

2. **Run Django locally:**
   ```bash
   python manage.py runserver
   ```

### Setup (Linux/macOS)

1. **Make script executable:**
   ```bash
   chmod +x dev.sh
   ```

2. **First time setup:**
   ```bash
   ./dev.sh setup
   ```

3. **Run Django locally:**
   ```bash
   python manage.py runserver
   ```

### Manual Setup (All Platforms)

1. **Copy environment file:**
   ```bash
   # Windows
   copy .env.development .env
   
   # Linux/macOS
   cp .env.development .env
   ```

2. **Start Docker services only:**
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
- Django API: http://localhost:8000
- Django Admin: http://localhost:8000/admin
- PostgreSQL: localhost:5432
- Redis: localhost:6379
- MinIO Console: http://localhost:9001 (admin/secure_minio_password_123)
- MinIO API: http://localhost:9000

### Development Commands

**Windows:**
```bash
dev.bat setup      # First time setup
dev.bat start      # Start services
dev.bat stop       # Stop services
dev.bat restart    # Restart services
dev.bat logs       # View logs
dev.bat clean      # Remove all data and volumes
```

**Linux/macOS:**
```bash
./dev.sh setup     # First time setup
./dev.sh start     # Start services
./dev.sh stop      # Stop services
./dev.sh restart   # Restart services
./dev.sh logs      # View logs
./dev.sh clean     # Remove all data and volumes
```

---

## 🚀 Production Mode (Full Docker)

Run everything in Docker including Django with Gunicorn and Nginx.

### Why Production Mode?
- ✅ Production-like environment
- ✅ Test Nginx configuration
- ✅ Test Gunicorn settings
- ✅ Isolated and reproducible deployment

### Setup (Windows)

1. **Configure environment:**
   ```bash
   copy .env.production .env.production
   ```
   ⚠️ **Important:** Edit `.env.production` and change all passwords!

2. **Build and start:**
   ```bash
   prod.bat build
   ```

3. **Run migrations:**
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
   ```

4. **Create superuser:**
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
   ```

### Setup (Linux/macOS)

1. **Make script executable:**
   ```bash
   chmod +x prod.sh
   ```

2. **Configure environment:**
   ```bash
   cp .env.production .env.production
   ```
   ⚠️ **Important:** Edit `.env.production` and change all passwords!

3. **Build and start:**
   ```bash
   ./prod.sh build
   ```

4. **Run migrations:**
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py migrate
   ```

5. **Create superuser:**
   ```bash
   docker-compose -f docker-compose.prod.yml exec web python manage.py createsuperuser
   ```

### Access Points (Production)
- Django API (via Nginx): http://localhost
- Django Admin: http://localhost/admin
- MinIO Console: http://localhost:9001

### Production Commands

**Windows:**
```bash
prod.bat build     # Build and start all services
prod.bat start     # Start all services
prod.bat stop      # Stop all services
prod.bat restart   # Restart services
prod.bat logs      # View all logs
```

**Linux/macOS:**
```bash
./prod.sh build    # Build and start all services
./prod.sh start    # Start all services
./prod.sh stop     # Stop all services
./prod.sh restart  # Restart services
./prod.sh logs     # View all logs
```

---

## 📁 File Structure

```
.env.development           # Development environment variables
.env.production            # Production environment variables
.env.example               # Template for environment variables
docker-compose.dev.yml     # Services only (no web container)
docker-compose.prod.yml    # All services including web + nginx
dev.bat / dev.sh           # Development helper scripts
prod.bat / prod.sh         # Production helper scripts
```

## 🔄 Switching Between Modes

### Development → Production

**Windows:**
```bash
dev.bat stop
prod.bat build
```

**Linux/macOS:**
```bash
./dev.sh stop
./prod.sh build
```

### Production → Development

**Windows:**
```bash
prod.bat stop
copy .env.development .env
dev.bat start
python manage.py runserver
```

**Linux/macOS:**
```bash
./prod.sh stop
cp .env.development .env
./dev.sh start
python manage.py runserver
```

## 💡 Tips & Best Practices

### Development
- Use development mode for daily coding work
- Django auto-reloads on code changes
- Easy to use debuggers and breakpoints
- Direct access to all services on localhost
- Run tests with `pytest`

### Production
- Test production configuration before deployment
- Verify Nginx routing and static file serving
- Test Gunicorn worker configuration
- Check health checks and restart policies

### Security
- ⚠️ Never commit `.env*` files with real passwords
- ⚠️ Change all default passwords in production
- ⚠️ Use strong passwords for PostgreSQL, Redis, and MinIO
- ✅ Use `.env.example` as a template
- ✅ Keep `.env*` files in `.gitignore`

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Check what's using the port (Windows)
netstat -ano | findstr :5432

# Check what's using the port (Linux/macOS)
lsof -i :5432
```

### Database Connection Issues
```bash
# Wait for PostgreSQL to be ready
# Windows
timeout /t 5

# Linux/macOS
sleep 5
```

### Clean Start
```bash
# Windows
dev.bat clean
dev.bat setup

# Linux/macOS
./dev.sh clean
./dev.sh setup
```

## 📚 Additional Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Redis Documentation](https://redis.io/documentation)
- [MinIO Documentation](https://min.io/docs/)
