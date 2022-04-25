#!/bin/bash

export ACCOUNT_NUM="644348144159"
export PROJECT_ID="strong-maker-345805"
export REPO="eerichmond/ml-wildfire-prediction"

gcloud config set project "${PROJECT_ID}"
gcloud config set run/region "us-west1"

setup() {
  gcloud auth login

  gcloud iam service-accounts create "ml-wildfire-service" \
    --project "${PROJECT_ID}" \
    --display-name="ML Wildfire Service"

  gcloud services enable iamcredentials.googleapis.com \
    --project "${PROJECT_ID}"

  gcloud iam workload-identity-pools create "eerichmond" \
    --project="${PROJECT_ID}" \
    --location="global" \
    --display-name="eerichmond pool"

  # Output identity pool ID
  pool_id = $(gcloud iam workload-identity-pools describe "eerichmond" \
    --project="${PROJECT_ID}" \
    --location="global" \
    --format="value(name)")
  export WORKLOAD_IDENTITY_POOL_ID=${pool_id}
  # export WORKLOAD_IDENTITY_POOL_ID=projects/644348144159/locations/global/workloadIdentityPools/eerichmond

  gcloud iam workload-identity-pools providers create-oidc "github" \
    --project="${PROJECT_ID}" \
    --location="global" \
    --workload-identity-pool="eerichmond" \
    --display-name="github provider" \
    --attribute-mapping="google.subject=assertion.sub,attribute.actor=assertion.actor,attribute.repository=assertion.repository" \
    --issuer-uri="https://token.actions.githubusercontent.com"

  gcloud iam service-accounts add-iam-policy-binding "ml-wildfire-service@${PROJECT_ID}.iam.gserviceaccount.com" \
    --project="${PROJECT_ID}" \
    --role="roles/iam.workloadIdentityUser" \

  # Output workload identity provider
  gcloud iam workload-identity-pools providers describe "github" \
    --project="${PROJECT_ID}" \
    --location="global" \
    --workload-identity-pool="eerichmond" \
    --format="value(name)"

  # Setup Artifact Registry for Docker images
  gcloud services enable artifactregistry.googleapis.com

  gcloud artifacts repositories create "ml-wildfire" \
    --repository-format="docker" \
    --location="us-west1"

  # Setup Cloud Run
  gcloud services enable run.googleapis.com

  gcloud run deploy "ml-wildfire" \
    --service-account="ml-wildfire-service@${PROJECT_ID}.iam.gserviceaccount.com" \
    --image="us-west1-docker.pkg.dev/strong-maker-345805/ml-wildfire/ml-wildfire:latest" \
    --port="8000" \
    --region="us-west1"

  gcloud projects add-iam-policy-binding ${PROJECT_ID} \
    --member="serviceAccount:ml-wildfire-service@${PROJECT_ID}.iam.gserviceaccount.com" \
    --role="roles/run.admin"

  gcloud iam service-accounts add-iam-policy-binding \
    --project="${PROJECT_ID}" \
    --role="roles/run.admin" \
    --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${REPO}"

}

setup
