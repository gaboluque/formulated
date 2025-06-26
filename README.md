# Formulated 🏎️

A modern, full-stack social Formula 1 application that brings together F1 teams, races, and fan engagement in one comprehensive platform.

## 🚀 Features

### Core Features
- **Team Management**: Browse and explore detailed F1 team profiles with complete member rosters
- **Race Tracking**: Follow current and historical F1 races with comprehensive circuit information
- **Member Profiles**: Detailed driver and team member information with roles and statistics
- **Circuit Database**: Comprehensive circuit information with race history

### Social Features
- **Reviews System**: Rate and review teams, races, and members with detailed feedback
- **Like System**: Express appreciation for your favorite teams, drivers, and races
- **User Authentication**: Secure user registration and login system
- **User Profiles**: Personalized user experiences with interaction history

### Data Integration
- **Live F1 Data**: Integration with APISports F1 API for real-time race data
- **Automated Data Sync**: Management commands to pull and sync race data
- **Admin Dashboard**: Django admin interface for content management

## 🛠️ Technologies

### Backend
- **Django 4.2**: Web framework with REST API capabilities
- **Django REST Framework**: RESTful API development
- **PostgreSQL**: Primary database with UUID primary keys
- **Python 3.x**: Core programming language

### Frontend
- **React 19**: Modern UI library with hooks
- **TypeScript**: Type-safe JavaScript development
- **Vite**: Fast development build tool
- **Tailwind CSS**: Utility-first CSS framework
- **React Router**: Client-side routing

### Infrastructure
- **Docker**: Containerization for consistent development
- **Docker Compose**: Multi-container orchestration
- **PostgreSQL**: Database containerization

### External APIs
- **APISports F1 API**: Real Formula 1 data integration

## 📋 Prerequisites

- Docker and Docker Compose
- Make (optional, for convenient commands)

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd formulated
```

### 2. Environment Setup
Create a `.env` file in the root directory:
```env
# Django Settings
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=1
ALLOWED_HOSTS=localhost,127.0.0.1,api

# Database
DATABASE_URL=postgresql://formulated_user:formulated_pass@db:5432/formulated

# API Keys (Optional)
APISPORTS_API_KEY=your-apisports-api-key

# Admin User
DJANGO_SUPERUSER_USERNAME=admin
DJANGO_SUPERUSER_EMAIL=admin@formulated.com
DJANGO_SUPERUSER_PASSWORD=qwerty123
```

### 3. Start the Application
```bash
# Build and start all services
make up
# or
docker-compose up -d

# The application will automatically:
# - Set up the PostgreSQL database
# - Run Django migrations
# - Create a superuser account
# - Seed initial data
```

### 4. Access the Application
- **Frontend**: http://localhost:5173
- **API**: http://localhost:8000/api/
- **Admin Panel**: http://localhost:8000/admin/

### 5. Default Credentials
- **Admin**: admin / qwerty123
- **Test User**: testuser / qwerty123

## 🔧 Development Commands

### Using Make (Recommended)
```bash
make help          # Show all available commands
make build         # Build all containers
make up            # Start all services
make down          # Stop all services
make logs          # View logs from all services
make shell         # Enter API container shell
make migrate       # Run Django migrations
make test          # Run Django tests
make seed          # Seed database with initial data
```

### Using Docker Compose Directly
```bash
# Container management
docker-compose build
docker-compose up -d
docker-compose down
docker-compose logs -f

# Django commands
docker-compose exec api python manage.py migrate
docker-compose exec api python manage.py createsuperuser
docker-compose exec api python manage.py test
docker-compose exec api python manage.py seed_data

# Data loading commands
docker-compose exec api python manage.py pull_races --season 2024

# Frontend commands
docker-compose exec client npm install
docker-compose exec client npm run build
```

## 📡 API Endpoints

### Teams
- `GET /api/teams/` - List all teams
- `GET /api/teams/{id}/` - Get team details
- `POST /api/teams/{id}/reviews/` - Create team review
- `POST /api/teams/{id}/like/` - Like/unlike team

### Races
- `GET /api/races/` - List all races
- `GET /api/races/{id}/` - Get race details
- `POST /api/races/{id}/reviews/` - Create race review
- `POST /api/races/{id}/like/` - Like/unlike race

### Members
- `GET /api/members/` - List all team members
- `GET /api/members/{id}/` - Get member details
- `POST /api/members/{id}/reviews/` - Create member review
- `POST /api/members/{id}/like/` - Like/unlike member

### Circuits
- `GET /api/circuits/` - List all circuits
- `GET /api/circuits/{id}/` - Get circuit details
- `POST /api/circuits/{id}/reviews/` - Create circuit review
- `POST /api/circuits/{id}/like/` - Like/unlike circuit

### Authentication
- `POST /api/auth/register/` - User registration
- `POST /api/auth/login/` - User login
- `POST /api/auth/logout/` - User logout

## 🗄️ Database Schema

### Core Models
- **Team**: F1 teams with detailed information and statistics
- **Member**: Team members (drivers, engineers, managers) with roles
- **Race**: F1 races with status tracking and results
- **Circuit**: Racing circuits with location information
- **Position**: Race results and driver positions

### Social Models
- **Review**: User reviews with ratings (1-5 stars) for teams, races, and members
- **Like**: User likes for teams, races, and members
- **User**: Django's built-in user model for authentication

## 🔄 Data Management

### Pulling Live Data
```bash
# Pull current season races
docker-compose exec api python manage.py pull_races

# Pull specific season
docker-compose exec api python manage.py pull_races --season 2024

# Dry run (preview changes)
docker-compose exec api python manage.py pull_races --dry-run
```

### Database Operations
```bash
# Create database backup
docker-compose exec db pg_dump -U postgres formulated > backup.sql

# Reset database (careful!)
docker-compose exec api python manage.py flush

# Check migration status
docker-compose exec api python manage.py showmigrations
```

## 🧪 Testing

### Backend Tests
```bash
# Run all tests
docker-compose exec api python manage.py test

# Run specific app tests
docker-compose exec api python manage.py test teams
docker-compose exec api python manage.py test races
docker-compose exec api python manage.py test interactions

# Run with coverage
docker-compose exec api coverage run --source='.' manage.py test
docker-compose exec api coverage report
```

### Frontend Development
```bash
# Type checking
docker-compose exec client npm run type-check

# Linting
docker-compose exec client npm run lint

# Build for production
docker-compose exec client npm run build
```

## 🏗️ Project Structure

```
formulated/
├── api/                    # Django REST Framework backend
│   ├── formulated/         # Main Django project
│   ├── teams/              # Teams and members app
│   ├── races/              # Races and circuits app
│   ├── interactions/       # Reviews and likes app
│   ├── data_loader/        # External API integration
│   └── requirements.txt
├── client/                 # React frontend
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── pages/          # Page components
│   │   ├── lib/            # API client and utilities
│   │   └── routing/        # Router configuration
│   └── package.json
├── docker-compose.yml      # Development orchestration
└── Makefile               # Development commands
```
