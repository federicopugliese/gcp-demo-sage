FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

# Le dipendenze cambiano meno spesso del codice: installarle in un layer separato
# sfrutta la cache di Docker sulle build successive. README.md serve già qui: pyproject.toml
# lo dichiara come `readme`, e il build backend (uv_build) lo richiede per costruire il
# pacchetto `sage` nel secondo `uv sync` sotto.
COPY pyproject.toml uv.lock README.md ./
RUN uv sync --frozen --no-dev --no-install-project

COPY src ./src
RUN uv sync --frozen --no-dev

# Cloud Run assegna la porta dinamicamente tramite la variabile PORT: un container che
# resta in ascolto su una porta fissa non è raggiungibile.
ENV PORT=8080
EXPOSE 8080

CMD ["sh", "-c", "uv run uvicorn sage.webapp.app:app --host 0.0.0.0 --port ${PORT}"]
