# AI Document RAG & Booking System
````markdown

A FastAPI application that allows document ingestion, AI-powered retrieval-augmented generation (RAG),
and user booking storage. Users can ingest PDFs or text files, choose fixed or semantic chunking, store
embeddings in Pinecone, and submit booking information via AI-assisted chat.

## Features

- Ingest PDF and text documents.
- Choose between fixed or semantic chunking.
- Generate embeddings with SentenceTransformers.
- Store embeddings in Pinecone for semantic search.
- Submit booking information through the `/chat` endpoint.
- FastAPI docs for interactive API exploration.


````
## Setup
### 1. Clone the repository
```bash
git clone <your-repo-url>
cd <your-project-folder>
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scripts\activate      # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root:

```
api_key = <your_pinecone_api_key>
GEMINI_API_KEY = <your_google_genai_api_key>
DATABASE_URL = postgresql+psycopg2://username:password@localhost:5432/booking-info
```

### 5. Run the FastAPI server

```bash
uvicorn main:app --reload
```

### 6. Explore API documentation

* Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Endpoints

### Document Ingestion

`POST /ingest` – Upload PDF or text files with query parameter `chunk_type` (`fixed` or `semantic`).

### Chat / Booking

`POST /chat` – Send a JSON payload:

```json
{
  "text": "How AI can be helpful for todays world?",
  "userid": 1,
  "search_type": "semantic"
}
```

The AI decides whether the input is a booking request or a question:

* If booking, the data is parsed and stored in PostgreSQL.
* If a question, it performs RAG-based retrieval using the Pinecone embeddings.

### Notes

* Ensure PostgreSQL is running and the database exists.
* Use ISO format for date (`YYYY-MM-DD`) and time (`HH:MM:SS`) in bookings.
* Fixed and semantic chunk embeddings are stored in separate Pinecone indexes to avoid mixing.

