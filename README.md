To setup:
pyenv shell 3.12.0
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

To run: fastmcp run server.py:mcp --transport sse --port 3333 --log-level DEBUG