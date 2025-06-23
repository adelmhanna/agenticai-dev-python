docker compose down && docker compose up --build
docker compose up --build --force-recreate

docker inspect --format "{{.Name}} {{.State.Health.Status}}" $(docker ps -q)


docker volume prune
#Clear unused volumes to reset  data