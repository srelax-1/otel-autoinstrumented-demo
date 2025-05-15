
# Create directory for the loki volume
create-dir:
	mkdir -p ./loki/wal

up:
	docker compose up --build -d

down:
	docker compose down

start: create-dir up

# Help target to show usage
help:
	@echo "Usage:"
	@echo "  make create-dir   # Create ./loki/wal directory"
	@echo "  make up           # Run docker compose up -d"
	@echo "  make down         # Run docker compose down"
	@echo "  make start        # Create dir and run docker compose up -d"