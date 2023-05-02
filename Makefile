include example.env

.PHONY: up
up:
	chmod +x scripts/run-docker.sh
	./scripts/run-docker.sh

.PHONY: down
down:
	chmod +x scripts/close-docker.sh
	./scripts/close-docker.sh
