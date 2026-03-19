import os
from google.cloud import pubsub_v1
from services.pubsub.config.config import settings

# Create Pub/Sub clients
publisher_client = pubsub_v1.PublisherClient()

def send_message_to_pubsub(data, topic):
    """Publishes multiple messages to a Pub/Sub topic."""
    project_id = settings.project_id
    topic_name = f"projects/{project_id}/topics/{topic}"
    data_bytes = str(data).encode("utf-8")  # Convert data to bytes
    
    future = publisher_client.publish(topic_name, data_bytes)
    print(f"Published message to Pub/Sub: {future.result()}")