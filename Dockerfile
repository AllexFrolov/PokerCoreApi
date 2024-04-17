FROM gcc:latest as build

RUN apt-get update;\
    apt-get install -y cmake libzmq3-dev 
    
COPY ./app/core/montecarlo ./app/core/montecarlo
COPY ./shell/build.sh ./

RUN ./build.sh



FROM python:3.10.9-slim-bullseye

RUN pip install poetry

WORKDIR /app

COPY --from=build ./app/core/montecarlo/build ./core/montecarlo/build
COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false &&\
    poetry install --no-interaction --no-ansi --without dev

COPY ./app .

EXPOSE 8001

CMD ["flask", "run"]
