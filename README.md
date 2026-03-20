# Database Connection Pool

> A production-grade database connection management system built in pure Python, modelling the same architecture used by SQLAlchemy, psycopg2, and every professional ORM in the industry.

---

## Overview

**Database Connection Pool** is the third project in my OOP Python Data Engineering series. It implements a full database abstraction layer with a concrete SQLite connector and a connection pool that manages multiple reusable connections efficiently.

In production data engineering, opening a new database connection for every query is expensive. This project solves that by keeping a fixed number of connections alive and lending them out to callers — returning them to the pool when done instead of closing them.

---

## Architecture

```
database_connector/
├── __init__.py
├── base.py                 # Abstract DatabaseConnector base class
├── sqlite_connector.py     # Concrete SQLite implementation
└── connection_pool.py      # ConnectionPool manager
test.py                     # Integration tests
student_db                  # SQLite database file (auto-generated)
```

---

## Classes

### `DatabaseConnector` (Abstract Base Class)
The abstract parent for all database connectors. Enforces that every connector implements `connect()`, `disconnect()`, and `execute()`. Also implements the context manager protocol via `__enter__` and `__exit__`.

```python
from abc import ABC, abstractmethod

class DatabaseConnector(ABC):
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self._connection = None

    @abstractmethod
    def connect(self): ...

    @abstractmethod
    def disconnect(self): ...

    @abstractmethod
    def execute(self, query, params=()): ...

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return False
```

### `SQLiteConnector`
Concrete implementation for SQLite databases. Uses Python's built-in `sqlite3` module. Returns query results as a list of dictionaries using `cursor.description` for column names.

```python
with SQLiteConnector('student.db') as conn:
    conn.execute('''CREATE TABLE IF NOT EXISTS Students (
        std_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        email TEXT NOT NULL,
        course TEXT NOT NULL
    )''')

    conn.execute(
        "INSERT INTO Students (name, age, email, course) VALUES (?,?,?,?)",
        ('Thiyane Xavier', 21, 'thiyane@gmail.com', 'Information Technology')
    )

    results = conn.execute("SELECT * FROM Students")
    print(results)
    # [{'std_id': 1, 'name': 'Thiyane Xavier', 'age': 21, ...}]
```

### `ConnectionPool`
Manages a fixed-size pool of database connections. Creates all connections at initialisation time, tracks which are available and which are active, and enforces the pool size limit.

```python
pool = ConnectionPool(SQLiteConnector, size=3, db_path='student.db')

conn1 = pool.get_connection()
conn2 = pool.get_connection()
conn3 = pool.get_connection()

try:
    conn4 = pool.get_connection()  # Pool exhausted
except RuntimeError as e:
    print(e)  # No connection available

pool.release_connection(conn3)
conn4 = pool.get_connection()  # Works now

pool.close_all()
```

---

## Key Features

**Context Manager Support**
`SQLiteConnector` works as a context manager. The connection opens automatically on entry and closes cleanly on exit — even if an exception occurs inside the block.

**Parameterised Queries**
All queries support parameterised inputs to prevent SQL injection:
```python
conn.execute("SELECT * FROM Students WHERE age = ?", (21,))
```

**Results as Dictionaries**
`execute()` returns results as a list of dictionaries with column names as keys — not raw tuples. This makes results immediately usable without index guessing.

**Pool Exhaustion Handling**
`get_connection()` raises a `RuntimeError` with a clear message when no connections are available — preventing silent failures.

**Clean Pool Shutdown**
`close_all()` disconnects every connection in the pool cleanly, whether active or available.

---

## OOP Concepts Practised

| Concept | Where Used |
|---|---|
| Abstract Classes | `DatabaseConnector` uses `ABC` and `@abstractmethod` |
| Context Managers | `__enter__` and `__exit__` on `DatabaseConnector` |
| Encapsulation | `_connection`, `_available`, `_active` are private attributes |
| @property | `connection_count`, `active_count`, `available_count`, `is_healthy` |
| Composition | `ConnectionPool` holds and manages a list of connector objects |
| Factory Pattern | `ConnectionPool` creates connectors from a class and kwargs |
| Inheritance | `SQLiteConnector` inherits from `DatabaseConnector` |

---

## DE Context

This project mirrors the core architecture of production database tools:

| This Project | Production Equivalent |
|---|---|
| `DatabaseConnector` | `sqlalchemy.engine.Engine` base |
| `SQLiteConnector` | `psycopg2`, `pymysql`, `cx_Oracle` |
| `ConnectionPool` | `sqlalchemy.pool.QueuePool` |
| `__enter__` / `__exit__` | `with engine.connect() as conn:` |
| `execute()` returning dicts | `pandas.read_sql()` output format |

Understanding connection pooling is one of the most important performance concepts in data engineering. Every pipeline that reads from or writes to a database benefits from this pattern.

---

## How to Run

```bash
# Clone the repository
git clone https://github.com/Thiyane24/database-connection-pool
cd database-connection-pool

# Run the tests
python test.py
```

No external dependencies — standard library only.

---

## Requirements

- Python 3.8+
- No third-party libraries required

---

## Bugs Fixed During Development

**`_connection` was `None` when `close_all()` was called** — The `ConnectionPool` was creating connector objects but never calling `connect()` on them. Adding `connection.connect()` inside the `__init__` loop before appending to `_available` resolved it.

**`cursor.description` was `None` for INSERT queries** — After an `INSERT` or `CREATE TABLE` statement, `cursor.description` returns `None` because there are no result columns. Added a guard clause to return an empty list `[]` for these cases instead of crashing.

**Duplicate records on every run** — The `CREATE TABLE IF NOT EXISTS` statement prevented table recreation but the `INSERT` statements still ran every time. Fixed by adding `DROP TABLE IF EXISTS` before the create statement to reset the table on each test run.

---

## Part of

This project is part of my **OOP Python Data Engineering Series** — 7 projects building from beginner to intermediate DE skills.

| # | Project | Status |
|---|---|---|
| 01 | CSV Data Parser & Cleaner | ✅ Complete |
| 02 | Pipeline Runner | ✅ Complete |
| 03 | Database Connection Pool | ✅ Complete |
| 04 | Schema Registry | ⏳ Upcoming |
| 05 | Data Quality Framework | ⏳ Upcoming |
| 06 | Mini Message Queue | ⏳ Upcoming |
| 07 | Batch Job Scheduler | ⏳ Upcoming |

---

## Author

**Thiyane Xavier**
IT Diploma Student @ MAHSA University, Malaysia
Aspiring Data Engineer | Python | SQL | AWS

[![LinkedIn](https://img.shields.io/badge/LinkedIn-Thiyane%20Xavier-blue)](https://www.linkedin.com/in/thiyane-xavier-9aa09a345/)
[![GitHub](https://img.shields.io/badge/GitHub-Thiyane24-black)](https://github.com/Thiyane24)
