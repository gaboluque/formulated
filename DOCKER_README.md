# Docker Setup for Formulated

This project uses Docker Compose to run the client, API, and PostgreSQL database in containers.

## Prerequisites

- Docker
- Docker Compose

## Services

- **db**: PostgreSQL 15 database
- **api**: Django REST API backend
- **client**: React frontend with Vite

## Quick Start

1. Build and start all services:
   ```bash
   docker-compose up --build
   ```

2. The services will be available at:
   - Client (React): http://localhost:5173
   - API (Django): http://localhost:8000
   - Database: localhost:5432

## Environment Variables

You can customize the setup by creating a `.env` file in the root directory with these variables:

```env
# Django Settings
DEBUG=1
DJANGO_SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgresql://formulated_user:formulated_pass@db:5432/formulated

# CORS Settings
CORS_ALLOW_ALL_ORIGINS=1

# Vite/Client Settings
VITE_API_URL=http://localhost:8000
```

## Database

The PostgreSQL database is configured with:
- Database: `formulated`
- User: `formulated_user`
- Password: `formulated_pass`
- Port: `5432`

Data is persisted in a Docker volume named `postgres_data`.

## Development

- The API and client containers use volume mounts for live code reloading
- Changes to your code will be reflected immediately
- Database migrations are run automatically when the API starts

## Useful Commands

```bash
# Start services in background
docker-compose up -d

# Stop services
docker-compose down

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs api

# Rebuild containers
docker-compose up --build

# Run Django management commands
docker-compose exec api python manage.py <command>

# Access PostgreSQL shell
docker-compose exec db psql -U formulated_user -d formulated

# Remove everything including volumes
docker-compose down -v
```

## Notes

- The API waits for the database to be healthy before starting
- Database migrations are run automatically on startup
- The client is configured to proxy API requests to the backend container
- CORS is configured to allow requests from the frontend 