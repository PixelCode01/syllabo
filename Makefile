.PHONY: help build run interactive stop clean logs shell publish build-exe install-deps release clean-dev clean-dev-windows

help:
	@echo "Syllabo Commands:"
	@echo ""
	@echo "Development:"
	@echo "  make build      - Build the Docker image"
	@echo "  make run        - Run the application interactively"
	@echo "  make interactive - Run in interactive mode"
	@echo "  make stop       - Stop all containers"
	@echo "  make clean      - Remove containers and images"
	@echo "  make logs       - View application logs"
	@echo "  make shell      - Open shell in container"
	@echo ""
	@echo "Distribution:"
	@echo "  make build-exe  - Build standalone executables"
	@echo "  make publish    - Publish Docker image to registry"
	@echo "  make release    - Create complete release package"
	@echo ""
	@echo "Maintenance:"
	@echo "  make install-deps - Install development dependencies"
	@echo "  make clean-dev    - Clean development environment (Linux/macOS)"
	@echo "  make clean-dev-windows - Clean development environment (Windows)"

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
# Publishing and Distribution
publish:
	@echo "Publishing Docker image..."
	./docker-publish.sh

publish-windows:
	@echo "Publishing Docker image (Windows)..."
	docker-publish.bat

# Build standalone executables
build-exe:
	@echo "Building standalone executables..."
	python build.py

# Install development dependencies
install-deps:
	pip install -r requirements.txt
	pip install pyinstaller

# Create a complete release
release: install-deps build-exe build
	@echo "Creating complete release package..."
	@echo "✓ Executables built"
	@echo "✓ Docker image built"
	@echo "Next steps:"
	@echo "  1. Test the executables in dist/"
	@echo "  2. Run 'make publish' to publish Docker image"
	@echo "  3. Create GitHub release with executables"

# Clean development environment
clean-dev:
	@echo "Cleaning development environment..."
	@if [ -f cleanup.sh ]; then ./cleanup.sh; else echo "cleanup.sh not found"; fi

clean-dev-windows:
	@echo "Cleaning development environment (Windows)..."
	@cleanup.bat