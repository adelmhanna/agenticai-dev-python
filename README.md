# AgenticAI Dev Python

A modular FastAPI application that demonstrates how to orchestrate and health-check multiple backend services (databases, message brokers, AI models, and more) in a Docker-based environment.  
This project can serve as a quick-start scaffold for agentic AI platforms, service health dashboards, and integration prototypes.

---

## 🚀 Features

- **FastAPI**-powered REST APIs and HTML landing/status pages
- Modular connectors for:
  - Qdrant (vector DB)
  - MongoDB (document store)
  - Neo4j (graph DB)
  - MinIO (object storage)
  - Postgres (relational DB)
  - Ollama (LLM/AI)
  - Temporal (workflow orchestration)
  - Mosquitto (MQTT broker)
- Status and health-check endpoints for each service
- Docker Compose support for local development

---

## 🏁 Getting Started

### 1. **Clone the repository**
```bash
git clone https://github.com/adelmhanna/agenticai-dev-python.git
cd agenticai-dev-python
2. Configure environment
Copy or edit environment variables as needed in your docker-compose.yml.

3. Start with Docker Compose
bash
Copy
Edit
docker-compose up --build
This will start FastAPI plus all required services.

4. Access the app
Main app: http://localhost:8000

Status dashboard: http://localhost:8000/status

API endpoints: e.g., /api/test/qdrant, /api/test/mongodb, etc.

🧑‍💻 API Examples
Service	Endpoint	Description
Qdrant	/api/test/qdrant	Vector DB test search
MongoDB	/api/test/mongodb	Find document
Neo4j	/api/test/neo4j	Graph DB node query
MinIO	/api/test/minio	List buckets
Postgres	/api/test/postgres	User query
Ollama	/api/test/ollama	LLM/AI model response
Temporal	/api/test/temporal	Workflow test
Mosquitto	/api/test/mosquitto	Pub/sub test

🛠️ Project Structure
css
Copy
Edit
.
├── app/
│   ├── routes/
│   │   └── status.py
│   └── services/
│       ├── qdrant.py
│       ├── mongodb.py
│       ├── ...
├── main.py
├── docker-compose.yml
└── README.md
📝 About
This project is maintained by Adel Hanna and is open for collaboration and improvement.
Contributions, issues, and PRs are welcome!


