# La regione europe-west6

Il progetto Sage viene distribuito nella regione GCP europe-west6, che corrisponde al data
center di Zurigo, in Svizzera. Le risorse del corso (bucket, Firestore, Cloud Run, dataset
BigQuery) sono create in questa regione per due motivi principali.

# Latenza

Zurigo è geograficamente vicina agli studenti del corso, quindi le richieste verso l'API di
Sage e le query verso Firestore hanno una latenza di rete più bassa rispetto a una regione
extra-europea.

# Residenza dei dati

Mantenere le risorse in una regione europea aiuta a rispettare i requisiti di residenza dei
dati quando si trattano informazioni che devono restare all'interno dell'Unione Europea o
dello Spazio Economico Europeo. Non tutti i servizi GCP sono disponibili in tutte le regioni:
prima di scegliere una regione per un nuovo servizio è buona pratica verificarne la
disponibilità nella documentazione ufficiale.
