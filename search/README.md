# Search Platform

Full-text search service for BFSI platform documents, customers, audit records, and agent decisions.

## Modules

| Module | Purpose |
|--------|---------|
| `search-common` | DTOs: `SearchDocument`, `SearchRequest`, `SearchResponse` |
| `search-client` | In-memory (dev) and Elasticsearch (prod) stores |
| `search-api` | Deployable service on port **8370** |

## Run

```bash
mvn package -DskipTests -pl search/search-api -am
java -jar search/search-api/target/search-api-0.1.0-SNAPSHOT.jar
```

Via API Gateway: `POST http://localhost:8000/api/search/search`

## API

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health + backend type |
| POST | `/api/v1/search` | Full-text search |
| POST | `/api/v1/index` | Index a document |
| GET | `/api/v1/indices` | List index types |

## Configuration

```env
SEARCH_PORT=8370
SEARCH_BACKEND=memory          # or elasticsearch
ELASTICSEARCH_HOST=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_INDEX_PREFIX=bfsi
```

Index mappings: `search/elasticsearch/mappings/`
