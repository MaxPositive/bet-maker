runl:
    uvicorn src:init_app --reload
clear:
    docker system prune -a

clear-all:
    docker system prune -a && docker volume prune -a

run:
    docker compose up

mm *args:
    alembic revision --autogenerate -m "{{args}}"

migrate:
    alembic upgrade head

downgrade *args:
    alembic downgrade "{{args}}"

test:
    pytest

dtest:
    docker exec -it app poetry run pytest