cd backend
python -m uvicorn src.api.main:app --reload 

cd frontend 
npm run dev

cd airflow
docker compose down
docker compose build --no-cache
docker compose up