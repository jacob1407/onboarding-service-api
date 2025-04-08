# venv
python -m venv venv
source venv/bin/activate

# docker commands
docker build -t onboarding-service-api .
docker run -p 8080:8080 onboarding-service-api

docker compose up --build

# view db in terminal
docker exec -it onboarding-db psql -U myuser -d onboarding
- list tables: \dt