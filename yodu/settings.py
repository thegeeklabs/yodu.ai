import os

from dotenv import load_dotenv

load_dotenv()

ES_HOST = os.getenv("ES_HOST", "localhost")
ES_USER = os.getenv("ES_USER", "user")
ES_PASSWORD = os.getenv("ES_PASSWORD", "password")
ES_PORT = os.getenv("ES_PORT", 9200)
