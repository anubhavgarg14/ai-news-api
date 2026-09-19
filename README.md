# AI News API

An AI-powered backend that scrapes tech news, understands it, and answers plain-English questions about it — grounded in real articles, with citations, not guesses.



## What it does

1. **Scrapes** live tech articles from Hacker News automatically
2. **Summarizes and tags** each article using an AI model (`gpt-4o-mini`)
3. **Stores** everything in PostgreSQL, including a meaning-based "fingerprint" (embedding) of each article chunk, powered by `pgvector`
4. **Answers questions** in plain English via a `/ask/` endpoint — retrieving the most relevant article chunks first, then generating an answer *only* from that retrieved text (a pattern called RAG — Retrieval-Augmented Generation), with citations and a `supported: true/false` flag showing whether the answer was actually backed by evidence

## Why it's interesting

- **Grounded, not hallucinated.** The model is instructed to answer only from retrieved context, and to say "Not enough information" when the articles don't cover the question — verified directly against out-of-scope test questions.
- **Tested with real numbers, not vibes.** A 12-question automated evaluation suite (`week6/evaluations/`) checks retrieval accuracy, answer accuracy, and end-to-end accuracy against known-correct fixtures.
- **A real bug, found and fixed at the root cause.** One evaluation case failed because the model paraphrased an exact model name ("Kobo Clara" instead of "Kobo Clara BW"). Traced back to the source text, diagnosed as a missing precision instruction in the answer-generation prompt, fixed with one added line — evaluation went from 11/12 to **12/12 (100%)**.
- **Fully containerized.** Builds and runs cleanly via Docker, verified to produce identical results (12/12) whether running directly or inside its packaged container.

## Tech stack

`Python` · `FastAPI` · `Uvicorn` · `PostgreSQL` + `pgvector` · `OpenAI API` (`gpt-4o-mini`) · `SQLAlchemy` · `Pydantic` · `Docker` · `uv`

## Architecture

```
Scraper (Hacker News)
      │
      ▼
Enrichment  ──▶  AI summary + tags
      │
      ▼
Chunking + Embedding  ──▶  stored in Postgres/pgvector
      │
      ▼
/search/  ──▶  meaning-based retrieval of relevant chunks
      │
      ▼
/ask/  ──▶  AI generates a grounded answer + citations from retrieved chunks
```

## Evaluation results

```
Retrieval accuracy: 12/12 (100.0%)
Answer accuracy:    12/12 (100.0%)
End-to-end accuracy: 12/12 (100.0%)
```

Run it yourself:

```bash
uv run python -m week6.evaluations.run_evaluation --base-url http://localhost:8001
```

## Running it locally

**1. Clone and install dependencies:**

```bash
git clone https://github.com/anubhavgarg14/ai-news-api.git
cd ai-news-api
uv sync
```

**2. Set up environment variables** — copy `.env.example` (or create `.env`) with:

```
OPENAI_API_KEY=your-key-here
POSTGRES_USER=ai_news
POSTGRES_PASSWORD=your-password
POSTGRES_DB=ai_news
DATABASE_URL=postgresql://ai_news:your-password@localhost:5432/ai_news
```

**3. Start the database:**

```bash
docker compose up -d
```

**4. Run the full pipeline** (scrape → enrich → index):

```bash
uv run python -m app.pipeline
```

**5. Start the API server:**

```bash
uv run uvicorn app.main:app --reload --port 8001 --env-file .env
```

**6. Try it** — open the Swagger UI at `http://localhost:8001/docs`, or send a question directly:

```bash
curl -X POST http://localhost:8001/ask/ \
  -H "Content-Type: application/json" \
  -d '{"question": "Which Kobo model is the only one stated to have been hardware-tested?", "limit": 5}'
```

## Running it in Docker

```bash
docker build -t ai-news-api .
docker run -p 8080:8080 --env-file .env.docker ai-news-api
```

(Note: inside a container, `localhost` refers to the container itself — point `DATABASE_URL` in `.env.docker` at `host.docker.internal` instead of `localhost` to reach a database running on your host machine.)

## Deployment status

Fully containerized and deployment-ready for Google Cloud Run — the Dockerfile builds and runs correctly, and the containerized app passes the full evaluation suite. Live deployment is pending a GCP billing account setup.

## Project structure

```
app/
├── agents/          # AI calls: enrichment, embedding, answer generation
├── api/routes/       # FastAPI endpoints (news, search, ask, health)
├── database/         # Models, connection, repository (Postgres + pgvector)
├── schemas/          # Pydantic data shapes
├── scrapers/          # Hacker News scraper
├── services/          # Indexing pipeline
├── main.py
└── pipeline.py
week6/evaluations/     # Automated evaluation suite (fixtures, scoring, runner)
Dockerfile
docker-compose.yml
```

## License

MIT
