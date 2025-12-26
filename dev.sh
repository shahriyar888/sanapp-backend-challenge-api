#!/bin/bash
# Development Helper Script for Linux/macOS

set -e

show_help() {
    echo "Usage: ./dev.sh [command]"
    echo ""
    echo "Commands:"
    echo "  setup    - First time setup (copy .env, start services, migrate)"
    echo "  start    - Start development services (db, redis, minio)"
    echo "  stop     - Stop development services"
    echo "  restart  - Restart development services"
    echo "  logs     - Show service logs"
    echo "  clean    - Stop services and remove volumes"
    echo ""
    echo "First time? Run: ./dev.sh setup"
    echo "After that, use: python manage.py runserver"
}

start_services() {
    echo "Starting development services (PostgreSQL, Redis, MinIO)..."
    docker-compose -f docker-compose.dev.yml --env-file .env.development up -d
    echo ""
    echo "Waiting for PostgreSQL to be ready..."
    sleep 3
    echo ""
    echo "Services started! Now run Django locally:"
    echo "  python manage.py migrate"
    echo "  python manage.py runserver"
}

stop_services() {
    echo "Stopping development services..."
    docker-compose -f docker-compose.dev.yml down
}

restart_services() {
    echo "Restarting development services..."
    docker-compose -f docker-compose.dev.yml --env-file .env.development restart
}

show_logs() {
    docker-compose -f docker-compose.dev.yml logs -f
}

clean_services() {
    echo "Stopping and removing all containers and volumes..."
    docker-compose -f docker-compose.dev.yml down -v
}

setup_environment() {
    echo "Setting up development environment..."
    echo ""
    echo "1. Copying environment file..."
    if [ ! -f .env ]; then
        cp .env.development .env
        echo ".env created from .env.development"
    else
        echo ".env already exists, skipping..."
    fi
    echo ""
    echo "2. Starting services..."
    docker-compose -f docker-compose.dev.yml --env-file .env.development up -d
    echo ""
    echo "3. Waiting for PostgreSQL to be ready..."
    sleep 5
    echo ""
    echo "4. Running migrations..."
    python manage.py migrate
    echo ""
    echo "Setup complete! Start Django with:"
    echo "  python manage.py runserver"
}

# Main script logic
case "$1" in
    start)
        start_services
        ;;
    stop)
        stop_services
        ;;
    restart)
        restart_services
        ;;
    logs)
        show_logs
        ;;
    clean)
        clean_services
        ;;
    setup)
        setup_environment
        ;;
    *)
        show_help
        ;;
esac
