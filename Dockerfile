FROM python:3.10.4-slim-buster

WORKDIR /acompanha-legis

COPY . .

RUN pip install poetry

RUN poetry install

RUN poetry run python ./deputados.py 
RUN poetry run python ./deputados_expenses.py 
RUN poetry run python ./deputados_digest.py 

CMD ["poetry", "run", "python", "dev_server.py"]
