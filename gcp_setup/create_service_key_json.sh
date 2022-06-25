ACCOUNT_NUM="644348144159"
PROJECT_ID="strong-maker-345805"

service="ml-wildfire-service@${PROJECT_ID}.iam.gserviceaccount.com"

gcloud iam service-accounts keys create ~/.ssh/gcp-ml-wildfire-service.json --iam-account=${service}
