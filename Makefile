runl:
	uvicorn src:init_app --reload

run:
	docker compose up

dtest:
	docker exec -it app poetry run pytest