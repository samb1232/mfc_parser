# MFC Parser and API

## Overview

The MFC Parser and API project scrapes data from the MFC website, stores it in a SQLite database, and provides an API to interact with the data. It uses Flask for the API, SQLAlchemy for database operations, and Celery with Redis for background task processing.

## Features

- Web scraping and data parsing from the MFC website.
- Storage of parsed data in a SQLite database.
- API endpoints to update data, check update status, and retrieve data by ID.
- Background task processing with Celery.

## Setup

### Prerequisites

- Python 3.x
- Redis

### Installation

1. **Install dependencies**:

```bash
pip install -r requirements.txt
```

3. **Start Redis**:

```bash
redis-server
```

### Running the Application

1. **Start the Celery worker**:

```bash
celery -A tasks.celery worker --loglevel=info
```

2. **Run the Flask application**:

```bash
python app.py
```

The Flask API will be available at `http://localhost:5000`.

## API Endpoints

### `/update_mfc_db`

- **Method**: POST
- **Description**: Triggers the background task to update the MFC database.
- **Response**: `{"status": "Update started"}`

### `/is_updating`

- **Method**: GET
- **Description**: Checks the status of the update task.
- **Response**: `{"status": "Update in progress"}` or `{"status": "Update completed"}` or `{"status": "No update in progress"}`

### `/get_situation_by_id/<ticket_id>`

- **Method**: GET
- **Description**: Retrieves the content of a situation by its ID.
- **Response**:
  ```json
  {
    "id": "<ticket_id>",
    "text": "<ticket_text>",
    "topic": "<ticket_topic>",
    "link": "<ticket_link>"
  }
  ```
  or `{"error": "Ticket not found"}`
