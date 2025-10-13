from faststream.kafka.fastapi import KafkaBroker
from src.config import settings


kafka_broker = KafkaBroker(bootstrap_servers=settings.kafka_servers)