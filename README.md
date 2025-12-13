# QuizFlow ⚡

A modern, high-performance quiz application built with Flask. Supports 100+ concurrent students with responsive timer, clean UI, and multiple question formats.

## Features

- 🎯 **Multiple Question Formats**: Support for YAML and GIFT formats
- ⏱️ **Stateful Timer**: Timer persists across page navigation
- 📊 **Real-time Progress**: Visual progress bar and question counter
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- 🔐 **Admin Panel**: Easy quiz management and results viewing
- ⚡ **High Performance**: Optimized for 100+ concurrent users
- 💾 **Persistent State**: Answers and timer state saved automatically

## Tech Stack

- **Backend**: Flask 3.0
- **Database**: SQLite with WAL mode
- **Production Server**: Gunicorn (Linux/Mac) or Waitress (Windows)
- **Frontend**: Vanilla JavaScript, CSS3

## Installation

### 1. Clone or extract the project

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the application

#### Development Mode (Testing)
```bash
python app.py
```

#### Production Mode (Linux/Mac with Gunicorn)
```bash
chmod +x run_production.sh
./run_production.sh
```

#### Production Mode (Windows with Waitress)
```bash
run_windows.bat
```

#### Cross-platform Production (Recommended)
```bash
python run_waitress.py
```

## Configuration

Edit `config.py` to customize:

```python
SECRET_KEY = 'your-secret-key-here'  # Change in production!
ADMIN_PASSWORD = 'admin123'  # Change immediately!
DEFAULT_QUIZ_TIMER = 30  # minutes
PASSING_SCORE = 70  # percentage
```

## Production Deployment

### For 70-100 concurrent students:

**Option 1: Waitress (Recommended for Windows)**
```bash
python run_waitress.py
```
- 8 threads
- Handles ~100 concurrent users
- Works on all platforms

**Option 2: Gunicorn (Linux/Mac)**
```bash
./run_production.sh
```
- 4 workers × 2 threads = 8 concurrent handlers
- For 100+ students, increase to 8 workers

### Performance Tuning

For heavy load (100+ students), edit production config:

**Gunicorn** (`run_production.sh`):
```bash
--workers 8 --threads 4  # 32 concurrent handlers
```

**Waitress** (`run_waitress.py`):
```python
threads=12  # Increase to 12-16 for higher load
```

## Usage

### Admin Panel

1. Navigate to `/admin/login`
2. Default password: `admin123` (change this!)
3. Upload quizzes in YAML or GIFT format
4. View results and manage quizzes

### Creating Quizzes

**YAML Format:**
```yaml
- question: "What is 2 + 2?"
  options:
    - "3"
    - "4"
    - "5"
  correct: 1

- question: "Select the capital of France"
  options:
    - "London"
    - "Paris"
    - "Berlin"
  correct: 1
```

**GIFT Format:**
```
::Q1:: What is 2 + 2?{
=4
~3
~5
}

::Q2:: Select the capital of France{
=Paris
~London
~Berlin
}
```

### Timer Features

- ⏱️ **Persistent**: Timer continues even if you navigate away
- 🔔 **Warnings**: Alerts at 5 minutes and 1 minute remaining
- 🎯 **Accurate**: Uses system time, not intervals
- 🔄 **Stateful**: Survives page refreshes

## Database

SQLite with optimizations:
- WAL (Write-Ahead Logging) for concurrent reads/writes
- Indexed queries for fast lookups
- Thread-safe connection pooling
- 64MB cache for better performance

## Security Notes

### Before Production:

1. **Change SECRET_KEY**:
```python
SECRET_KEY = 'generate-a-secure-random-key'
```

2. **Change ADMIN_PASSWORD**:
```python
ADMIN_PASSWORD = 'strong-password-here'
```

3. **Use environment variables**:
```bash
export SECRET_KEY="your-secret-key"
export ADMIN_PASSWORD="your-admin-password"
```

## API Endpoints

- `GET /` - Home page with quiz list
- `GET /admin/login` - Admin login
- `GET /admin` - Admin dashboard
- `POST /admin/upload` - Upload new quiz
- `GET /quiz/<id>/start` - Start a quiz
- `GET /quiz/<id>/question/<n>` - View question
- `POST /quiz/<id>/submit` - Submit answer
- `GET /quiz/<id>/complete` - View results
- `GET /quiz/<id>/review` - Review answers

## File Structure

```
quiz-app/
├── app.py              # Application factory
├── wsgi.py             # Production entry point
├── config.py           # Configuration
├── requirements.txt    # Dependencies
├── run_production.sh   # Linux/Mac production script
├── run_windows.bat     # Windows production script
├── run_waitress.py     # Cross-platform production
├── models/
│   ├── __init__.py
│   └── database.py     # Database layer with connection pooling
├── routes/
│   ├── __init__.py
│   ├── main.py         # Home routes
│   ├── admin.py        # Admin routes
│   └── quiz.py         # Quiz routes
├── utils/
│   ├── __init__.py
│   ├── helpers.py      # Helper functions
│   └── parsers.py      # Quiz format parsers
├── static/
│   ├── css/
│   │   └── style.css   # Minimalist styles
│   └── js/
│       └── timer.js    # Stateful timer
└── templates/
    ├── base.html       # Base template with navbar & footer
    ├── home.html       # Home page
    ├── admin/
    │   ├── login.html
    │   └── dashboard.html
    └── quiz/
        ├── take.html
        ├── result.html
        └── review.html
```

## Troubleshooting

### Timer not persisting
- Check browser localStorage is enabled
- Clear localStorage: `localStorage.clear()`

### Database locked errors
- WAL mode should handle this
- If persists, reduce concurrent connections

### Performance issues with 100+ students
- Increase workers/threads in production config
- Consider upgrading to PostgreSQL for heavy load
- Enable caching layer (Redis)

## License

MIT License - feel free to use and modify!

## Credits

Made with ❤ by Nikhil

---

For questions or issues, please check the troubleshooting section or review the code comments.