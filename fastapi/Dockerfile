# syntax=docker/dockerfile:1.7
# ---------- deps ----------
FROM python:3.12-slim AS deps

WORKDIR /build

COPY requirements.txt .

RUN --mount=type=cache,target=/root/.cache/pip \
    pip install \
    --prefix=/install \
    -r requirements.txt

# ----------- runtime ------

FROM deps AS runtime

COPY --from=deps /install /usr/local

WORKDIR /app

COPY . .

CMD [  "uvicorn",  "app.main:app",  "--host",  "0.0.0.0",  "--port",  "8000"]