# AI-Powered Dynamic Form Builder

A small production-ready full-stack project for building and filling dynamic forms with an AI-assisted field generation endpoint.

## Tech Stack

- Backend: Flask REST API
- Frontend: React (functional components + hooks)
- Database: MySQL via SQLAlchemy ORM
- Validation: Marshmallow
- Testing: pytest

## Project Structure

```text
backend/
  app.py
  config.py
  extensions.py
  models/
  routes/
  services/
  schemas/
  tests/
  requirements.txt

frontend/
  components/
  pages/
  services/
  hooks/
  App.jsx
  main.jsx
  styles.css
```

## Architecture

The backend follows a clean layered flow:

- Routes layer: HTTP handling, JSON in/out, request parsing
- Schemas layer: input/output validation and normalization
- Services layer: business logic and orchestration
- Models layer: SQLAlchemy entities and relationships

Request flow:

1. Route receives request.
2. Schema validates payload.
3. Service executes business logic.
4. Model persistence through SQLAlchemy.
5. Route serializes response.

## Database Design

- Form: `id`, `title`, `description`, `created_at`
- Field: `id`, `form_id`, `type`, `label`, `options` (JSON)
- Response: `id`, `form_id`, `answers` (JSON), `submitted_at`

Relationships:

- A Form has many Fields
- A Form has many Responses

## API Endpoints

- `POST /forms`
- `GET /forms`
- `GET /forms/<id>`
- `POST /responses`
- `GET /responses/<form_id>`
- `POST /ai/generate-form`
- `GET /health`

## AI Usage

The AI generation endpoint accepts a text prompt and returns structured form fields.

- If `OPENAI_API_KEY` is configured, the app calls OpenAI Chat Completions.
- You can set `OPENAI_MODEL` (default: `gpt-4o-mini`).
- If OpenAI call fails or no key is configured, the app uses deterministic mock generation.
- AI output is validated against strict schema rules before returning.
- Invalid generated structures are rejected with `422`.

## Observability and Error Handling

- Request logging via Flask `before_request` and `after_request` hooks
- Structured JSON errors for:
  - validation failures (`422`)
  - not found (`404`)
  - unexpected server errors (`500`)

## Backend Setup

```bash
cd backend
python -m pip install -r requirements.txt
python app.py
```

Database configuration (MySQL):

```bash
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=dynamic_form_builder
```

Alternative connection string (overrides MYSQL_*):

```bash
DATABASE_URL=mysql+pymysql://root:your_password@localhost:3306/dynamic_form_builder
```

Optional AI environment variables:

```bash
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

Run tests:

```bash
cd backend
python -m pytest -q
```

## Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

By default, Vite proxies API calls to `http://localhost:5000`.

## Tech Decisions

- Flask + Blueprints: lightweight REST API with modular route groups
- SQLAlchemy ORM: portability and maintainable data layer without raw SQL
- Marshmallow: explicit schema validation and consistent error paths
- React hooks: simple stateful UI with controlled inputs and dynamic rendering

## Tradeoffs

- MySQL setup is slightly heavier than SQLite, but gives better production parity and concurrency behavior
- No auth/role model included to keep scope focused on form lifecycle and AI generation
- AI endpoint currently uses deterministic mock logic when no provider key is available, which improves reliability but limits generation diversity

## Notes

- Backend tests pass: `4 passed`
