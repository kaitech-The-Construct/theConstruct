import os
from google.cloud import pubsub_v1

# /home/ec2-user
# credential_path = "api-project-371618-5425bc261363.json"
# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

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
    project_id = project_id or "api-project-371618"

    # Encode the URL as UTF-8.

    data = url.encode("utf-8")

    # Create the topic name.

    topic_name = f"projects/{project_id}/topics/{topic}"

    # Publish the message to Pub/Sub.

    future = publisher_client.publish(topic_name, data)

    # Print the result of the publish operation.

    print(f"Published message to Pub/Sub: {future.result()}, data: {data}")