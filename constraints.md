# Constraints

## Functional Constraints

1. Supported field types are limited to:
   - `text`
   - `email`
   - `select`
   - `checkbox`
2. `select` fields must include at least one option.
3. Non-`select` fields must not include `options`.
4. Form title is required.
5. At least one field is required per form.
6. Response submission must include all form field labels.

## AI Safety Constraints

1. AI-generated output must pass schema validation before use.
2. Invalid AI output is rejected with `422`.
3. If no `AI_API_KEY` is configured, only mock generation is used.
4. Generated structures must map to supported field types only.

## API Constraints

1. All API errors return JSON payloads.
2. Validation failures return `422`.
3. Not-found resources return `404`.
4. Unexpected failures return `500` without exposing internals.

## Data Constraints

1. MySQL is the default datastore.
2. ORM access is SQLAlchemy only (no raw SQL).
3. Field options and response answers are stored as JSON columns.

## Operational Constraints

1. Logging is enabled for API request/response lifecycle and errors.
2. Backend tests are executed with pytest.
3. Frontend communicates through Axios and expects JSON API contracts.
