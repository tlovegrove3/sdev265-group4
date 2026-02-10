# SDEV265 Event Management System - Developer Setup

## Prerequisites

**Choose Your Setup Path:**
- **Path A (Recommended): uv** - Modern, fast package manager
- **Path B (Traditional): venv + pip** - Standard Python workflow

---

## Path A: Setup with uv (Recommended)

### 1. Install uv
```bash
# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Mac/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone & Setup
```bash
git clone https://github.com/tlovegrove3/sdev265-group4.git
cd sdev265-group4

# Install dependencies (auto-creates venv)
uv sync

# Configure git
git config commit.template .gitmessage.txt
git config core.editor "code --wait"
```

### 3. Run Database Migrations
```bash
uv run manage.py migrate
uv run manage.py check
```

### 4. Start Development Server
```bash
# Use convenience script
run.bat

# Or manually
uv run manage.py runserver 8001
```

**Key uv Commands:**
```bash
# Run any Django command
uv run manage.py <command>

# Examples
uv run manage.py makemigrations
uv run manage.py createsuperuser
uv run manage.py shell

# Add a new package
uv add <package-name>

# Update dependencies
uv sync
```

---

## Path B: Traditional Setup (venv + pip)

### 1. Clone Repository
```bash
git clone https://github.com/YourTeam/sdev265-group4.git
cd sdev265-group4
```

### 2. Create Virtual Environment
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
# Install from pyproject.toml
pip install -e .

# Or if requirements.txt exists
pip install -r requirements.txt
```

### 4. Configure Git
```bash
git config commit.template .gitmessage.txt
git config core.editor "code --wait"
```

### 5. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py check
python manage.py runserver 8001
```

**Important:** Always activate your venv before working:
```bash
# Windows: .venv\Scripts\activate
# Mac/Linux: source .venv/bin/activate
```

---

## Daily Development Workflow

### Starting Work

**With uv:**
```bash
git pull origin main
git checkout -b feat/your-feature-name
# No venv activation needed!
uv run manage.py runserver 8001
```

**With venv:**
```bash
git pull origin main
git checkout -b feat/your-feature-name
.venv\Scripts\activate  # Windows
# or: source .venv/bin/activate  # Mac/Linux
python manage.py runserver 8001
```

### Making Commits

**Using VS Code UI (Recommended - Works with both):**
1. Stage changes in Source Control panel
2. Click icon Conventional Commits extension
3. Select type, add description, commit

**Using Terminal:**
```bash
git add .
git commit
# Template opens - fill in:
# <type>(<scope>): <description>
```

**Commit Types:**
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Formatting
- `refactor` - Code restructuring
- `test` - Tests
- `chore` - Build/dependencies

---

## Initial Project Structure
```
sdev265-group4/
├── accounts/              # User authentication app
│   ├── models.py         # User-related models
│   ├── views.py          # Auth views (login, register, logout)
│   └── urls.py           # Auth URL patterns
├── events/               # Event management app
│   ├── models.py        # Event, Category, RSVP models
│   ├── views.py         # Event CRUD views
│   └── urls.py          # Event URL patterns
├── config/              # Django project settings
│   ├── settings.py      # Main settings file
│   ├── urls.py          # Root URL configuration
│   └── wsgi.py
├── templates/           # HTML templates (shared)
├── static/             # CSS, JS, images
├── manage.py           # Django management script
├── run.bat            # Quick start script (Windows)
├── pyproject.toml     # Python dependencies
└── .gitmessage.txt    # Commit message template
```

---

## Useful Commands

### Database

**With uv:**
```bash
uv run manage.py makemigrations
uv run manage.py migrate
uv run manage.py createsuperuser
```

**With venv (after activation):**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
```

### Development

**With uv:**
```bash
uv run manage.py check
uv run manage.py shell
uv run manage.py test
```

**With venv (after activation):**
```bash
python manage.py check
python manage.py shell
python manage.py test
```

---

## Troubleshooting

### "Port 8001 already in use"
```bash
# Windows
netstat -ano | findstr :8001
taskkill /PID <process_id> /F

# Mac/Linux
lsof -ti:8001 | xargs kill -9
```

### uv: command not found
Restart your terminal after installation, or install manually:
- Windows: Check PATH includes `%USERPROFILE%\.cargo\bin`
- Mac/Linux: Source your shell profile

### Virtual environment issues (venv users)
```bash
# Deactivate and recreate
deactivate
rm -rf .venv  # or: rmdir /s .venv on Windows
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e .
```

### Database conflicts after pulling
```bash
# Safe reset (loses local data)
rm db.sqlite3  # or: del db.sqlite3 on Windows

# With uv
uv run manage.py migrate

# With venv
python manage.py migrate
```

---

## Setup Verification Checklist

After setup, verify you can:
- [ ] Run migrations without errors
- [ ] Access `http://localhost:8001` and see Django page
- [ ] Make a commit using Conventional Commits extension
- [ ] See template when running `git commit` in terminal

---

## VS Code Extensions (Recommended)

Install these for better developer experience:
- **Conventional Commits** - Commit message helper
- **Python** - Language support
- **Django** - Template syntax
- **Pylance** - Fast IntelliSense

---

## Team Collaboration

- **Discord:** Daily questions & updates
- **Trello:** Task tracking
- **GitHub:** Code & PRs
- **Google Drive:** Shared docs
- **Monday 6:30 PM:** Weekly team meeting

---

**Questions?** Ask in Discord!