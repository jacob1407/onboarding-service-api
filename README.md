# venv
python -m venv venv
source venv/bin/activate

# installing packages
pip install -r requirements.txt
- if you're on mac, you may need to run `brew install postgresql` beforehand

# docker commands
docker build -t onboarding-service-api .
docker run -p 8080:8080 onboarding-service-api

docker compose up --build

# view db in terminal
docker exec -it onboarding-db psql -U myuser -d onboarding
- list tables: \dt

# to add new db script
alembic revision --autogenerate -m "script description"
alembic upgrade head
