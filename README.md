## Running the application

By default, the dev server is started on port 9000.

### With docker

```sh
$ docker build . -t acompanha-legis-data
```

```sh
$ docker run -p 9000:9000 acompanha-legis-data
```

### Without docker

```sh
$ poetry install
```

```sh
$ poetry run python3 ./deputados.py
```

```sh
$ poetry run python3 ./deputados_expenses.py
```

```sh
$ poetry run python3 ./deputados_digest.py
```

To initialize the server (default on port 9000):

```sh
$ poetry run python3 ./dev_server.py
```