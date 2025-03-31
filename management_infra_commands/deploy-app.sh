export $(cat .env | xargs)
gcloud app deploy

