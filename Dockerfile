#базовый образ питона
FROM python:3.12.4-slim

# рабочая папка внутри контейнера 
WORKDIR /code

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock ./

# команда, чтобы не создавать виртуальное окружение внутри контейнера
# --no-root не устанавливать сам проект как пакет
RUN poetry config virtualenvs.create false \
    && poetry install --no-root --only main 

COPY ./app ./app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]