import os

from dotenv import load_dotenv

load_dotenv()

INFLUX_DB_HOST = os.getenv("INFLUX_DB_HOST", "localhost")
INFLUX_DB_USER = os.getenv("INFLUX_DB_USER", "admin")
INFLUX_DB_PASSWORD = os.getenv("INFLUX_DB_PASSWORD", "password")
INFLUX_DB_PORT = os.getenv("INFLUX_DB_PORT", 8086)
INFLUX_USE_SSL = os.getenv("INFLUX_USE_SSL", False)
INFLUX_USE_VERIFY_SSL = os.getenv("INFLUX_USE_VERIFY_SSL", False)
INFLUX_DB_BUCKET = os.getenv("INFLUX_DB_BUCKET", "bridgeml")
INFLUX_DB_ORG = os.getenv("INFLUX_DB_ORG", "influxdata")
