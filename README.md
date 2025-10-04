# Text Analysis API

This project is a **Text Analysis API** built with **FastAPI**. It integrates with **Firebase**, **Google Cloud Pub/Sub**, and **Firestore** to provide a scalable and efficient text analysis service. The API uses AI-powered text analyzers to process and analyze text, providing structured outputs such as sentiment, keywords, and summaries.

---

## Features

- **FastAPI** for building RESTful APIs.
- **Firebase Authentication** for secure user management.
- **Google Cloud Firestore** for storing user and task data.
- **Google Cloud Pub/Sub** for asynchronous task processing.
- **AI-Powered Text Analysis** using OpenAI models.
- **Dockerized** for easy deployment.
- **Celery** for background task processing.

---

## Project Structure

```
.
├── app/
│   ├── core/               # Core utilities (Firebase, Firestore, Pub/Sub)
│   ├── OpenAI/             # AI-related modules (analyzers, prompts, schemas)
│   ├── routes/             # API routes
│   ├── tasks.py            # Task processing logic
│   ├── main.py             # FastAPI entry point
├── docker-compose.yml      # Docker Compose configuration
├── Dockerfile.api          # Dockerfile for the API service
├── Dockerfile.worker       # Dockerfile for the worker service
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

---

## Getting Started

### Prerequisites

- Python 3.11+
- Docker & Docker Compose
- Google Cloud credentials (Service Account JSON)
- Firebase project setup

### Installation

1. Clone the repository:
    ```bash
    git clone <repository-url>
    cd text_analysis/backend
    ```

2. Create a `.env` file:
    ```bash
    touch .env
    ```

3. Add your environment variables to `.env`:
    ```env
    FIREBASE_CREDENTIALS_PATH=app/core/creds.json
    GCP_PROJECT=kai-developer-test
    PUBSUB_TOPIC=process-text-task
    PUBSUB_SUBSCRIPTION=process-text-sub
    ```

4. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

---

## Running the Project

### Using Docker Compose

1. Build and start the services:
    ```bash
    docker-compose up --build
    ```

2. Access the API at [http://localhost:8080](http://localhost:8080).

### Without Docker

1. Start the FastAPI server:
    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 8080
    ```

2. Start the worker service:
    ```bash
    python -m app.worker
    ```

---

## API Endpoints

### `/api/submit-text` (POST)
Submit text for analysis.

**Request Body:**
```json
{
  "text": "Your text here"
}
```

**Response:**
```json
{
  "task_id": "unique-task-id",
  "status": "submitted",
  "user_id": "user-id"
}
```

### `/api/create-user` (POST)
Create a new user.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "display_name": "User Name"
}
```

**Response:**
```json
{
  "uid": "user-id",
  "email": "user@example.com",
  "display_name": "User Name"
}
```

---

## Technologies Used

- **FastAPI**: High-performance web framework.
- **Firebase Admin SDK**: User authentication and management.
- **Google Cloud Firestore**: NoSQL database for storing data.
- **Google Cloud Pub/Sub**: Messaging service for task distribution.
- **OpenAI**: AI-powered text analysis.
- **Docker**: Containerization for deployment.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Firebase Documentation](https://firebase.google.com/docs)
- [Google Cloud Pub/Sub Documentation](https://cloud.google.com/pubsub/docs)
- [OpenAI Documentation](https://platform.openai.com/docs)
