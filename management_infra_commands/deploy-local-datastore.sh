export $(cat .env | xargs)
gcloud beta emulators datastore start

