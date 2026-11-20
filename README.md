# Lego DB

An inventory tracking system for bulk lego parts, built with Python, Flask, and PostgreSQL.

## Tech Stack

* **Backend:** Python 3.x, Flask
* **Database:** PostgreSQL
* **ORM & Migrations:** Flask-SQLAlchemy, Flask-Migrate (Alembic)
* **Database Driver:** `psycopg2-binary`

## Prerequisites

Ensure you have the following installed locally:
* [Python 3.10+](https:/python.org)
* [PostgreSQL 14+](https:/postgresql.org)
* `pip` and `venv`

## Getting Started

### 1. Clone the Repository
```bash
git clone https:/github.com/funkaspuckX/legodb.git
cd lego_db
```

### 2. Set Up a Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure DB
Update the __init__.py file
```bash
SQLALCHEMY_DATABASE_URI='postgresql:/postgres@pg:5432/lego_db',
```


### 5. Set Up the Database
Create the PostgreSQL database locally:
```bash
psql -U postgres -c "CREATE DATABASE lego_db;"
```

Run database migrations to create the tables:
```bash
flask db upgrade
```

### 6. Run the Application
```bash
flask run
```
The application will be available at `http:/127.0.0.1:3000`.

## Project Structure

```text
├── src/
c
│   ├── models.py                       # SQLAlchemy database models
│   └── api/                            # API specifications
│   │   ├── __init__.py                 # App factory & extensions initialization
│   │   ├── colors.py                   # API for colors table
│   │   ├── compartments.py             # API for compartments table
│   │   ├── containers.py               # API for containers table
│   │   ├── locations.py                # API for locations table
│   │   ├── part_types.py               # API for part_types table
│   │   ├── parts.py                    # API for parts table
│   │   ├── room_inventory_report.py    # API for room_inventory_report 
│   │   ├── shelves.py                  # API for shelves table
│   │   ├── shelving_units.py           # API for shelving_units table
│   │   └── size_categories.py          # API for size_categories table
├── migrations/                         # Alembic database migration files
├── tests/                              # Unit and integration tests
├── .gitignore
├── requirements.txt                    # Python dependencies
└── run.py                              # Entry point to start the server
```

## API Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/colors/` | Retrieve all items |
| `GET` | `/colors/<id>` | Retrieve a single item by ID |
| `POST` | `/colors/` | Create a new item |
| `PUT` | `/colors/<id>` | Update an existing item |
| `DELETE` | `/colors/<id>` | Delete an item |
| `GET` | `/compartments/` | Retrieve all items |
| `GET` | `/compartments/<id>` | Retrieve a single item by ID |
| `POST` | `/compartments/` | Create a new item |
| `PUT` | `/compartments/<id>` | Update an existing item |
| `DELETE` | `/compartments/<id>` | Delete an item |
| `GET` | `/containers/` | Retrieve all items |
| `GET` | `/containers/<id>` | Retrieve a single item by ID |
| `POST` | `/containers/` | Create a new item |
| `PUT` | `/containers/<id>` | Update an existing item |
| `DELETE` | `/containers/<id>` | Delete an item |
| `GET` | `/locations/` | Retrieve all items |
| `GET` | `/locations/<id>` | Retrieve a single item by ID |
| `POST` | `/locations/` | Create a new item |
| `PUT` | `/locations/<id>` | Update an existing item |
| `DELETE` | `/locations/<id>` | Delete an item |
| `GET` | `/part_types/` | Retrieve all items |
| `GET` | `/part_types/<id>` | Retrieve a single item by ID |
| `POST` | `/part_types/` | Create a new item |
| `PUT` | `/part_types/<id>` | Update an existing item |
| `DELETE` | `/part_types/<id>` | Delete an item |
| `GET` | `/parts/` | Retrieve all items |
| `GET` | `/parts/<id>` | Retrieve a single item by ID |
| `POST` | `/parts/` | Create a new item |
| `PUT` | `/parts/<id>` | Update an existing item |
| `DELETE` | `/parts/<id>` | Delete an item |
| `GET` | `/room_inventory_report/<id>` | Retrieve inventory remote for room ID |
| `GET` | `/shelves/` | Retrieve all items |
| `GET` | `/shelves/<id>` | Retrieve a single item by ID |
| `POST` | `/shelves/` | Create a new item |
| `PUT` | `/shelves/<id>` | Update an existing item |
| `DELETE` | `/shelves/<id>` | Delete an item |
| `GET` | `/shelving_units/` | Retrieve all items |
| `GET` | `/shelving_units/<id>` | Retrieve a single item by ID |
| `POST` | `/shelving_units/` | Create a new item |
| `PUT` | `/shelving_units/<id>` | Update an existing item |
| `DELETE` | `/shelving_units/<id>` | Delete an item |
| `GET` | `/size_categories/` | Retrieve all items |
| `GET` | `/size_categories/<id>` | Retrieve a single item by ID |
| `POST` | `/size_categories/` | Create a new item |
| `PUT` | `/size_categories/<id>` | Update an existing item |
| `DELETE` | `/size_categories/<id>` | Delete an item |

## Lessons Learned / Development Retrospective

The initial decision was made to utilize ORM, but the complex nature of joining so many 
tables to generate the inventory report resulted in raw SQL being most effective.

To do the sample data loading during development, simple direct API access scripts were
written for every table, but their use is tedious and unintuitive.  A future development
to implement a GUI or web portal seems the next priority.


## License

This project is licensed under the MIT License.