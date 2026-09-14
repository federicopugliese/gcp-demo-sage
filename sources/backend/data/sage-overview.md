# Cos'è Sage

Sage è l'assistente Q&A del progetto guida del corso: risponde a domande in linguaggio
naturale su un insieme di documenti caricati in precedenza. Ogni domanda è indipendente
dalle altre: Sage non mantiene memoria di conversazione tra una richiesta e la successiva.

# Come funziona una richiesta

Quando arriva una domanda, l'API calcola l'embedding del testo e lo usa per cercare in
Firestore i chunk di documento più simili dal punto di vista semantico. I chunk trovati
vengono inseriti nel prompt inviato al modello linguistico, che genera una risposta basata
solo su quel contenuto. Questo approccio si chiama RAG, Retrieval-Augmented Generation, e
riduce il rischio che il modello inventi informazioni non presenti nei documenti.

# Perché Firestore

Firestore supporta nativamente un tipo di campo vettoriale, quindi lo stesso database che
contiene il testo dei chunk può anche eseguire la ricerca per similarità, senza bisogno di
un database vettoriale separato. Ogni chunk indicizzato porta con sé il testo, l'embedding
e alcuni metadati come il documento di origine e la sezione, così le risposte di Sage
possono citare le fonti da cui provengono.
