.PHONY: help build run interactive stop clean logs shell

help:
	@echo "Syllabo Docker Commands:"
	@echo "  make build      - Build the Docker image"
	@echo "  make run        - Run the application interactively"
	@echo "  make interactive - Run in interactive mode"
	@echo "  make stop       - Stop all containers"
	@echo "  make clean      - Remove containers and images"
	@echo "  make logs       - View application logs"
	@echo "  make shell      - Open shell in container"

build:
	docker-compose build

run:
	docker-compose run --rm syllabo

interactive:
	docker-compose run --rm syllabo python main.py interactive

stop:
	docker-compose down

clean:
	docker-compose down --rmi all --volumes --remove-orphans

logs:
	docker-compose logs -f syllabo

shell:
	docker-compose run --rm syllabo /bin/bash

# Specific commands
analyze:
	docker-compose run --rm syllabo python main.py analyze

search:
	docker-compose run --rm syllabo python main.py search --topic "$(TOPIC)"

quiz:
	docker-compose run --rm syllabo python main.py quiz