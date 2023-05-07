include example.env

.PHONY: up
up:
	chmod +x scripts/deploy-docker-pipeline.sh
	./scripts/deploy-docker-pipeline.sh

.PHONY: down
down:
	chmod +x scripts/close-docker.sh
	./scripts/close-docker.sh
