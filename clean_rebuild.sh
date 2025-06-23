docker compose down
docker volume prune -f 
docker compose up --build --force-recreate


docker system prune -a --volumes
docker stop $(docker ps -q)
docker rm -f $(docker ps -a -q)
docker ps -a

# Stop all containers
docker stop $(docker ps -aq)

# Remove all containers
docker rm $(docker ps -aq)

# Remove all volumes
docker volume rm $(docker volume ls -q)