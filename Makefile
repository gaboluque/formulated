.PHONY: help build up down restart logs shell shell-db migrate createsuperuser test clean

# Default target
help:
	@echo "Available commands:"
	@echo "  build         - Build all containers"
	@echo "  up            - Start all services"
	@echo "  down          - Stop all services"
	@echo "  logs          - View logs from all services"
	@echo "  shell         - Enter Python container shell"
	@echo "  make-migrations - Make Django migrations"
	@echo "  migrate       - Run Django migrations"
	@echo "  seed          - Seed database with initial data"
	@echo "  createsuperuser - Create Django superuser"
	@echo "  test          - Run all Django tests"

# Build containers
build:
	docker-compose build

# Start services
up:
	docker-compose up -d

# Stop services
down:
	docker-compose down

# View logs
logs:
	docker-compose logs -f

# Enter Python/Django container shell
shell:
	docker-compose exec api bash

make-migrations:
	docker-compose exec api python manage.py makemigrations

# Run Django migrations
migrate:
	docker-compose exec api python manage.py migrate

# Seed database with initial data
seed:
	docker-compose exec api python manage.py seed_data

# Create Django superuser
createsuperuser:
	docker-compose exec api python manage.py createsuperuser

# Run all Django tests
test:
	docker-compose exec api python manage.py test
