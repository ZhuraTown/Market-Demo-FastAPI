from faststream.kafka import KafkaBroker

from src.events.broker import kafka_broker

async def get_kafka_broker() -> KafkaBroker:
    return kafka_broker