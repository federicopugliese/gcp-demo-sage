# Infrastruttura di Sage (Terraform)

Un solo ambiente: queste risorse coprono l'intero progetto di corso, non c'è una
separazione dev/test/prod. Ogni studente applica questo modulo sul proprio progetto GCP.

## Risorse create

| File | Risorsa | A cosa serve |
|---|---|---|
| `services.tf` | `google_project_service` | Abilita le API GCP usate dal progetto |
| `storage.tf` | `google_storage_bucket` | Bucket `<project_id>-sage-docs` per i documenti sorgente |
| `firestore.tf` | `google_firestore_database`, `google_firestore_index` | Firestore Native + indice vettoriale sul campo `embedding` della collection `chunks` |
| `bigquery.tf` | `google_bigquery_dataset`, `google_bigquery_table` | Dataset `sage_analytics` e tabella `question_log` per l'analytics delle domande |
| `artifact_registry.tf` | `google_artifact_registry_repository` | Repository Docker per le immagini dell'API |
| `iam.tf` | `google_service_account`, `google_project_iam_member` | Service account runtime di Cloud Run, a privilegio minimo |
| `cloud_run.tf` | `google_cloud_run_v2_service`, `google_cloud_run_v2_service_iam_member` | Il servizio che espone `/api/ask` |

Niente Secret Manager: Sage chiama Vertex AI con Application Default Credentials, non
servono API key esterne da custodire come segreto.

## Perché l'immagine Cloud Run non è gestita da Terraform

`cloud_run.tf` imposta `container_image` su un placeholder pubblico e poi lo ignora
(`lifecycle.ignore_changes`). L'immagine reale viene pubblicata dalla pipeline applicativa
(`.github/workflows/deploy.yml`, `gcloud run deploy --image ...`), tenuta volutamente
separata dalla pipeline Terraform (`.github/workflows/terraform.yml`): una modifica al
codice non richiede di rieseguire un piano Terraform, e viceversa.

## Comandi

```bash
cd devops/cloud

# una tantum: crea il bucket di state se non esiste già
gcloud storage buckets create gs://<project_id>-tfstate \
  --project <project_id> --location europe-west6 --uniform-bucket-level-access

cp backend.hcl.example backend.hcl        # e modifica il bucket
cp terraform.tfvars.example terraform.tfvars  # e modifica project_id

terraform init -backend-config=backend.hcl
terraform plan  -var-file=terraform.tfvars
terraform apply -var-file=terraform.tfvars
```

In CI, lo stesso flusso gira nel workflow `terraform.yml`: `plan` su ogni pull request che
tocca `devops/cloud/**`, poi un job `approval` che attende un'approvazione manuale su una
issue GitHub prima di eseguire `apply` sul piano già salvato.
