variable "project_id" {
  description = "ID del progetto GCP. Ogni studente lo sostituisce con il proprio (its-ict-<nome>-<cognome>)."
  type        = string
  default     = "its-ict-template-sage"
}

variable "region" {
  description = "Regione GCP per tutte le risorse."
  type        = string
  default     = "europe-west6"
}

variable "app_name" {
  description = "Nome base usato per Cloud Run, Artifact Registry e il service account applicativo."
  type        = string
  default     = "sage"
}

variable "docs_bucket_suffix" {
  description = "Suffisso del bucket dei documenti sorgente. Il nome finale è <project_id>-<suffisso>."
  type        = string
  default     = "sage-docs"
}

variable "firestore_collection" {
  description = "Nome della collection Firestore che contiene i chunk indicizzati."
  type        = string
  default     = "chunks"
}

variable "embedding_dimension" {
  description = "Dimensione del vettore embedding: deve corrispondere al modello configurato nel backend (SAGE_EMBEDDING_MODEL)."
  type        = number
  default     = 768
}

variable "bq_dataset" {
  description = "Dataset BigQuery per l'analytics delle domande."
  type        = string
  default     = "sage_analytics"
}

variable "bq_table" {
  description = "Tabella BigQuery in cui il backend scrive una riga per ogni domanda."
  type        = string
  default     = "question_log"
}

variable "container_image" {
  description = "Immagine container servita da Cloud Run. Un placeholder pubblico al primo apply: la pipeline di deploy (.github/workflows/deploy.yml) la aggiorna dopo la prima build."
  type        = string
  default     = "us-docker.pkg.dev/cloudrun/container/hello"
}

variable "allow_unauthenticated" {
  description = "Se true, l'API di Sage è raggiungibile senza autenticazione (comodo per il corso). Metti false per richiedere IAM invoker su Cloud Run."
  type        = bool
  default     = true
}
