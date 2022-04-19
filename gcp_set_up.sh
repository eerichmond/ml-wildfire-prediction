#!/bin/bash

export PROJECT_ID=strong-maker-345805
export WORKLOAD_IDENTITY_POOL_ID=projects/644348144159/locations/global/workloadIdentityPools/eerichmond
export REPO=eerichmond/ml-wildfire-prediction

gcloud auth login

gcloud config set project ${PROJECT_ID}

gcloud config set run/region us-west1

setup() {
  gcloud iam service-accounts create "ml-wildfire-service" --project "${PROJECT_ID}"

  gcloud services enable iamcredentials.googleapis.com --project "${PROJECT_ID}"

  gcloud iam workload-identity-pools create "eerichmond" --project="${PROJECT_ID}" --location="global" --display-name="eerichmond pool"

  # Output identity pool ID
  pool_id = $(gcloud iam workload-identity-pools describe "eerichmond" --project="${PROJECT_ID}" --location="global" --format="value(name)")
  export WORKLOAD_IDENTITY_POOL_ID=${pool_id}

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
    --member="principalSet://iam.googleapis.com/${WORKLOAD_IDENTITY_POOL_ID}/attribute.repository/${REPO}"

  # Output workload identity provider
  gcloud iam workload-identity-pools providers describe "github" \
    --project="${PROJECT_ID}" \
    --location="global" \
    --workload-identity-pool="eerichmond" \
    --format="value(name)"
}

# setup
