# Database Concurrency Examples with Python

This repository contains Python scripts to demonstrate common concurrency problems in relational databases (Percona MySQL and PostgreSQL). The examples include:

- Dirty Read
- Phantom Read
- Lost Update
- Non-Repeatable Read

Each example is implemented for both **Percona MySQL** and **PostgreSQL**.

---

## Prerequisites

1. **Python 3.8 or higher** installed on your system.
2. **Docker** and **Docker Compose** installed to run Percona MySQL and PostgreSQL containers.
3. Ensure ports `3306` (MySQL) and `5432` (PostgreSQL) are free on your host machine.

---

## Setup Instructions

### 1. Clone the Repository

Clone this repository to your local machine:

```bash
git clone https://github.com/alexeysirenko/prjctr-9-transaction-isolation
cd prjctr-9-transaction-isolation
```

### 2. Start Databases Using Docker Compose

This project includes a `docker-compose.yml` file to run both Percona MySQL and PostgreSQL containers.

To start the databases, run:

```bash
docker-compose up -d
```

This will:

- Start a Percona MySQL instance (`percona-db`) on port `3306`.
- Start a PostgreSQL instance (`postgres-db`) on port `5432`.

### 3. Initialize Databases

Once the containers are running, initialize the databases and tables:

#### Percona MySQL

Run the initialization script:

```bash
docker exec -i percona-db mysql -u testuser -ptestpassword testdb < percona/create-tables.sql
```

#### PostgreSQL

Run the initialization script:

```bash
docker exec -i postgres-db psql -U testuser -d testdb < postgres/create-tables.sql
```

---

## Setting Up Python

### 1. Create a Virtual Environment

Create a virtual environment to isolate the dependencies:

```bash
python3 -m venv venv
```

Activate the virtual environment:

- **Linux/macOS**:

  ```bash
  source venv/bin/activate
  ```

- **Windows**:
  ```bash
  venv\Scripts\activate
  ```

### 2. Install Dependencies

Install the required Python packages using `pip`:

```bash
pip install -r requirements.txt
```

---

## Running the Scripts

Each script demonstrates a specific concurrency issue. Run them as follows:

### Dirty Read (Percona)

```bash
python percona/dirty_read.py
```

### Dirty Read (PostgreSQL)

Does not reproduce (`read uncommited` not supported)

```bash
python postgres/dirty_read.py
```

### Phantom Read (Percona)

Only with `read commited`, problem does not occur on `repeatable read`

```bash
python percona/phantom_read.py
```

### Phantom Read (PostgreSQL)

Occurs by default

```bash
python postgres/phantom_read.py
```

### Lost Update (Percona)

```bash
python percona/lost_update.py
```

### Lost Update (PostgreSQL)

```bash
python postgres/lost_update.py
```

### Non-Repeatable Read (Percona)

Adding `FOR UPDATE` into the First read causes a deadlock
Reproduces only with `REPEATABLE READ`

```bash
python percona/non_repeatable_read.py
```

### Non-Repeatable Read (PostgreSQL)

Adding `FOR UPDATE` into the First read causes a deadlock
Reproduces with default isolation level, which is `REPEATABLE READ`

```bash
python postgres/non_repeatable_read.py
```
