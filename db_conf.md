docker compose exec -T db pg_dump -U biteforecast_db > dump.sql    

docker compose exec -T db psql -U admin -d biteforecast_db < dump.sql