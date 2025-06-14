# Superheroes API
A Flask API for tracking superheroes and their respective superpowers.

## Description
The API enables the user perform **Create**, **Read**, and **Update** operations on the heroes and powers through endpoints, and provides relationships between them through the hero_powers entity.

## Features

- **Hero Management:** View all heroes or details of a specific hero.
- **Power Management:** View all powers, get specific power details, and update power descriptions.
- **Hero-Power Relationships:** Create associations between heroes and powers with strength levels
- **Data Validation:** Ensures the right data is submitted through validations

## Project Structure

```
python-p4-superheroes-cc/
├── Pipfile                 # Dependencies
├── Pipfile.lock            # Locked dependencies
├── README.md               # This file
└── server/
    ├── app.py              # Main Flask application and routes
    ├── debug.py            # Debug utilities
    ├── models.py           # Database models and relationships
    ├── migrations/         # Database migration files
    └── instance/
        └── superheroes.db  # SQLite database (Created after setup)
```

## Setup
### Prerequisites

Python 3.8 or higher

### Installation

1. Clone this repository:
```
git clone <repository-url>
cd python-p4-superheroes-cc
```

2. Create aand activate virtual environment (this also installs the required dependencies):

```
pipenv install; pipenv shell
```

3. Initialize the database:
```
cd server
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

4. Seed the database with sample data:

```
python seed.py
```


5. Run the application:
```
python app.py
```

The API will be available at http://localhost:5555/


## API Endpoints
### Heroes

- GET /heroes - Get all heroes
- GET /heroes/:id - Get a specific hero with their powers

### Powers

- GET /powers - Get all powers
- GET /powers/:id - Get a specific power
- PATCH /powers/:id - Update a power's description

### Hero Powers

- POST /hero_powers - Create a new hero-power relationship

## Data Models
### Hero

- `id`: Primary key
- `name`: Hero's real name
- `super_name`: Hero's superhero name

### Power

- `id`: Primary key
- `name`: Power name
- `description`: Power description (must be at least 20 characters)

### HeroPower

- `id`: Primary key
- `strength`: Power strength level ('Strong', 'Weak', or 'Average')
- `hero_id`: Foreign key to Hero
- `power_id`: Foreign key to Power

## Validations

- Power description: Must be present and at least 20 characters long
- HeroPower strength: Must be one of 'Strong', 'Weak', or 'Average'

## Responses
All successful responses return JSON data with appropriate HTTP Status Codes:

- 200: Success
- 201: Created
- 404: Not Found
- 400: Bad Request (validation errors)

Error responses include descriptive messages for easier debugging.

## Author
Enock Tangus
