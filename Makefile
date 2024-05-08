.PHONY: help build up down clean build-no-cache restart
include .env

help:
  @echo "Usage: make <target>"
  @echo "Available targets:"
  @echo "  build           Build Docker images"
  @echo "  up              Start Docker containers"
  @echo "  down            Stop Docker containers"
  @echo "  clean           Down Container and remove Volums and Network"
  @echo "  clean-all       Remove Docker containers and images"
  @echo "  build-no-cache  Build Docker images without cache"
  @echo "  restart         Restart Docker containers"
  @echo "  cli-web         connect to web bash"
  @echo "  cli-db          connect to db bash wirh postgres user"
  @echo "  test-cases      connect to web bash for run test"
  @echo "  logs            show logs in terminal"

build:
	  docker-compose build

up:
	  docker-compose up -d

down:
	  docker-compose down

clean:
	  docker-compose down -v --remove-orphans

clean-all:
	  docker-compose down --rmi all -v

build-no-cache:
	  docker-compose build --no-cache

restart: down up

logs:
	  docker-compose logs -f

cli-web:
    docker compose exec web /bin/bash

cli-db:
    docker compose exec -it db psql -U ${POSTGRES_USER}

test-cases:
    docker compose exec web python manage.py test
