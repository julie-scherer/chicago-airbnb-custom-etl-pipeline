PROJECT_NAME=chicago-airbnb-database

include .env

up:
	@if [ ! -f .env ]; then cp example.env .env ; fi
	docker-compose up --remove-orphans --build -d

down:
	docker-compose down --volumes --rmi all

clean:
	docker rm -vf ${DOCKER_CONTAINER}
	docker rmi -f ${DOCKER_IMAGE}

logs: 
	docker-compose logs -f

psql:
	docker exec -it ${PROJECT_NAME}-postgres-1 \
    	psql -U ${POSTGRES_USER} -d ${POSTGRES_DB}
