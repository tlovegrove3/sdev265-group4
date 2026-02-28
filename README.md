# G4 Event Optimizer

A web-based event management system built with Django. Users can create events, RSVP to events, and discover events through filtered search.

**Course:** SDEV265 - Ivy Tech Community College  
**Team:** Terry Lovegrove, Douglas Marshall, Amine Oubellil, Joshua Baker, Bryan Cajuste

## Features

- **User Authentication** - Register, log in, log out
- **Event Management** - Create, edit, and cancel events (creator-only permissions)
- **RSVP System** - RSVP/cancel RSVP with privacy-aware attendee visibility
- **Event Discovery** - Filter by category, date, price and sort by multiple fields
- **Predefined Categories** - 14 seeded event categories
- **Test Accounts and Events** - Test user funcitonality with different users and events created by them.

## Tech Stack

- Python 3.12+
- Django 6.0.1
- SQLite
- Bootstrap 5 (CDN)

## Getting Started

### Prerequisites

- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager (recommended) **or** pip

**Install uv**

```sh
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/tlovegrove3/sdev265-group4.git
   cd sdev265-group4
   ```

2. **Install dependencies**

   With uv (recommended):
   ```bash
   uv sync
   ```

   With pip:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Run migrations**
   ```bash
   uv run manage.py migrate
   ```
   Or with pip/venv: `python manage.py migrate`

4. **Seed test data** (optional - creates sample users and events)
   ```bash
   uv run manage.py seed_test_data
   ```

5. **Start the dev server**
   ```bash
   uv run manage.py runserver 8001
   ```
   Or use the included shortcut on Windows:
   ```bash
   .\run.bat #Includes the uv run manage.py runserver 8001 command
   ```

6. **Open your browser** to [http://localhost:8001](http://localhost:8001)

> **Note:** We use port 8001 because port 8000 is blocked on some devices. You can use any open port.

## Project Structure

```
sdev265-group4/
├── accounts/        # Authentication app (register, login, logout)
|---api/             # API configuration
├── config/          # Django settings and root URL config
├── events/          # Events, RSVPs, categories, discovery
|---static/          # CSS, Javascript, or Images go here
├── templates/       # HTML templates (base layout + app templates)
├── manage.py
├── pyproject.toml   # Project metadata and dependencies
└── run.bat          # Dev server shortcut (port 8001)
```

## Test Accounts

After running `seed_test_data`, these accounts are available (password for all: `testpass123`):

| Username | Purpose |
|----------|---------|
| `testuser1` | General testing |
| `testuser2` | General testing |
| `testuser3` | General testing |
| `testuser4` | General testing |
| `testuser5` | General testing |

## License

Academic project - not licensed for redistribution.
