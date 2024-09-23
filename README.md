# Interview Server

This is a conversations server for Mock Interview and Mental Health Platform.

It uses http restful api to communicate with the client.

## Prerequisites

1. Download [Ollama](https://ollama.com/download) and install it.

2. Download `llama3.1` using the following command:

```bash
ollama pull llama3.1
```

3. Verify that the `llama3.1` is downloaded by running the following command:

```bash
ollama list
```

## Installation

1. Clone the repository
2. Start the docker container

```bash
docker-compose up -d
```

3. Rename the `.env.example` file to `.env` and update the values

```bash
cp .env.example .env
```

3. Install the dependencies

```bash
pip install -r requirements.txt
```

4. Run the server

```bash
python -m app
```

## Documentation

After running the server, you can access the documentation at `http://localhost:8002/docs`.
