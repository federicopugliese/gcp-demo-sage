# sage (backend)

Backend FastAPI di Sage. Vedi il [README principale del repo](../../README.md) per la guida completa
all'uso e alla configurazione.

Comandi rapidi (da questa cartella):

```bash
uv sync                                    # installa le dipendenze
uv run uvicorn sage.webapp.app:app --reload  # avvia il server in locale
uv run pytest                               # esegue i test
uv run ruff check .                         # lint
```
