#!/usr/bin/env bash
set -euo pipefail

# Bootstrap one-time: crea Workload Identity Federation + un service account CI per UN
# progetto GCP, così le pipeline GitHub Actions possono autenticarsi senza chiavi statiche
# (mai una chiave di service account salvata come secret).
#
# Uso:
#   ./setup-gcp-once.sh <PROJECT_ID> <GITHUB_OWNER>/<GITHUB_REPO>
#
# Esempio:
#   ./setup-gcp-once.sh its-ict-mario-rossi mario-rossi/gcp-demo-sage
#
# Va eseguito una sola volta per progetto, da un account con i permessi per gestire IAM
# (es. il Project Owner assegnato quando crei il progetto).

PROJECT_ID="${1:?Uso: $0 <PROJECT_ID> <GITHUB_OWNER>/<GITHUB_REPO>}"
GITHUB_REPO="${2:?Uso: $0 <PROJECT_ID> <GITHUB_OWNER>/<GITHUB_REPO>}"

POOL_ID="github-actions-pool"
PROVIDER_ID="github-provider"
SA_NAME="github-deployer"
SA_EMAIL="${SA_NAME}@${PROJECT_ID}.iam.gserviceaccount.com"

echo "==> Abilito le API necessarie al bootstrap"
gcloud services enable \
  iam.googleapis.com \
  iamcredentials.googleapis.com \
  cloudresourcemanager.googleapis.com \
  sts.googleapis.com \
  --project "$PROJECT_ID"

echo "==> Creo il Workload Identity Pool (se non esiste già)"
gcloud iam workload-identity-pools create "$POOL_ID" \
  --project "$PROJECT_ID" \
  --location="global" \
  --display-name="GitHub Actions" \
  || echo "    Pool già esistente, continuo"

echo "==> Creo il provider OIDC per GitHub, ristretto a questo repository"
gcloud iam workload-identity-pools providers create-oidc "$PROVIDER_ID" \
  --project "$PROJECT_ID" \
  --location="global" \
  --workload-identity-pool="$POOL_ID" \
  --display-name="GitHub provider" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository" \
  --attribute-condition="assertion.repository=='${GITHUB_REPO}'" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  || echo "    Provider già esistente, continuo"

echo "==> Creo il service account usato dalle pipeline CI/CD"
gcloud iam service-accounts create "$SA_NAME" \
  --project "$PROJECT_ID" \
  --display-name="GitHub Actions deployer" \
  || echo "    Service account già esistente, continuo"

# NOTA didattica: roles/editor è volutamente ampio, per tenere semplice il bootstrap di un
# progetto usa-e-getta a uso corso (Terraform deve poter abilitare API, creare bucket,
# Firestore, BigQuery, IAM...). In un progetto reale si sostituirebbe con un set di ruoli
# granulari (run.admin, artifactregistry.writer, datastore.owner, bigquery.admin,
# storage.admin, iam.serviceAccountUser, serviceusage.serviceUsageAdmin,
# resourcemanager.projectIamAdmin). Nota bene: questo è il service account che orchestra
# il deploy, non quello con cui gira l'app — quello (sage_run in devops/cloud/iam.tf) ha
# solo i permessi minimi necessari a runtime.
echo "==> Assegno roles/editor al service account CI (vedi nota nello script)"
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${SA_EMAIL}" \
  --role="roles/editor" \
  --condition=None

echo "==> Collego il service account al Workload Identity Pool"
PROJECT_NUMBER=$(gcloud projects describe "$PROJECT_ID" --format="value(projectNumber)")
gcloud iam service-accounts add-iam-policy-binding "$SA_EMAIL" \
  --project "$PROJECT_ID" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_ID}/attribute.repository/${GITHUB_REPO}"

echo
echo "Fatto. Configura queste variabili nell'ambiente GitHub Actions del repository"
echo "(Settings -> Secrets and variables -> Actions -> Variables):"
echo
echo "  PROJECT_ID         = ${PROJECT_ID}"
echo "  PROJECT_NUMBER     = ${PROJECT_NUMBER}"
echo "  REGION             = europe-west6"
echo "  WIF_PROVIDER       = projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${POOL_ID}/providers/${PROVIDER_ID}"
echo "  WIF_SERVICE_ACCOUNT = ${SA_EMAIL}"
echo "  APPROVERS          = <il tuo username GitHub>"
echo
echo "Vedi setup.md per il resto della configurazione."
