export $(cat .env | xargs)
gcloud app logs read
