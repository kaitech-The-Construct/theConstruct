import os
from google.cloud import pubsub_v1


# Create Pub/Sub clients
publisher_client = pubsub_v1.PublisherClient()




def send_message_to_pubsub(url, topic):

    """Sends a message to the specified Pub/Sub topic.

    Args:
        url: The URL to send to Pub/Sub.
        topic: The name of the Pub/Sub topic to send the message to.
    """

    # Project ID
    project_id = os.environ.get("PROJECTID")


    # Encode the URL as UTF-8.

    data = url.encode("utf-8")

    # Create the topic name.

    topic_name = f"projects/{project_id}/topics/{topic}"

    # Publish the message to Pub/Sub.

    future = publisher_client.publish(topic_name, data)

    # Print the result of the publish operation.

    print(f"Published message to Pub/Sub: {future.result()}, data: {data}")