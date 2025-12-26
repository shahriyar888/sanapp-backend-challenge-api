#!/bin/bash
# Production Helper Script for Linux/macOS

set -e

show_help() {
    echo "Usage: ./prod.sh [command]"
    echo ""
    echo "Commands:"
    echo "  start    - Start all production services"
    echo "  stop     - Stop all production services"
    echo "  restart  - Restart production services"
    echo "  logs     - Show service logs (add service name for specific logs)"
    echo "  build    - Build and start services"
}

start_services() {
    echo "Starting production services (all in Docker)..."
    docker-compose -f docker-compose.prod.yml --env-file .env.production up -d
    echo ""
    echo "Production services started!"
    echo "Access at: http://localhost"
}

stop_services() {
    echo "Stopping production services..."
    docker-compose -f docker-compose.prod.yml down
}

restart_services() {
    echo "Restarting production services..."
    docker-compose -f docker-compose.prod.yml --env-file .env.production restart
}

show_logs() {
    if [ -n "$2" ]; then
        docker-compose -f docker-compose.prod.yml logs -f "$2"
    else
        docker-compose -f docker-compose.prod.yml logs -f
    fi
}

build_services() {
    echo "Building and starting production services..."
    docker-compose -f docker-compose.prod.yml --env-file .env.production up --build -d
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
        show_logs "$@"
        ;;
    build)
        build_services
        ;;
    *)
        show_help
        ;;
esac
