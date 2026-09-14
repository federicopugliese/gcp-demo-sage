# Cartella `data/`

Metti qui i documenti `.md` che vuoi far conoscere a Sage. Ogni file diventa una fonte
citabile nelle risposte (il nome del file compare come `source` nei chunk indicizzati).

Due file di esempio sono già presenti per poter testare subito la pipeline end-to-end senza
dover procurarsi contenuti propri.

Per indicizzare (o re-indicizzare, dopo aver modificato un file) tutti i documenti presenti
qui, esegui dalla cartella `backend/`:

```bash
uv run python utils/ingest_documents.py
```

Lo script chunka ogni file per intestazioni Markdown (`#`, `##`, ...) e per dimensione, calcola
l'embedding di ogni chunk con il modello configurato in `SAGE_EMBEDDING_MODEL`, e lo scrive
nella collection Firestore `chunks` (nome configurabile con `SAGE_FIRESTORE_COLLECTION`).
