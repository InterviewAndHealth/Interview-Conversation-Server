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

### Need to do some changes in dependencies file
1. Open /home/kirti/anaconda3/envs/sasefied/lib/python3.12/site-packages/langchain_core/messages/tool.py
3. First import the required module:
    ```
    from uuid import UUID, uuid4
    ```
2. In line 120:
    Replacee this line:
    ```
        tool_call_id = values["tool_call_id"]
        if isinstance(tool_call_id, (UUID, int, float)):
            values["tool_call_id"] = str(uuid4())
    ```
    with this line:
    ```
        values["tool_call_id"] = str(uuid4())
    ```

## Documentation

After running the server, you can access the documentation at `http://localhost:8002/docs`.
