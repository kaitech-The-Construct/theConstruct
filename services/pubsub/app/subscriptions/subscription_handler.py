import os
from google.cloud import pubsub_v1

from callbacks.callbacks import callback_cloud, callback_xmark, callback_inj



async def process_pubsub_messages():

    """Processes Pub/Sub messages from multiple subscriptions.

    Args:
        subscriptions (list): A list of Pub/Sub subscription names.
    """

    # Create a Pub/Sub client
    subscriber_client = pubsub_v1.SubscriberClient()
    # Project ID
    project_id = os.environ.get("PROJECTID")
    project_id = project_id or "api-project-371618"

    # List Subscriptions
    subscriptions = ["injective-sub", "xmark-sub", "cloud-data-sub"]

    # Subscribe to the Pub/Sub subscriptions and start listening
    for subscription in subscriptions:
        subscription_path = subscriber_client.subscription_path(
            f"{project_id}", subscription
        )
        if subscription == "xmark-sub":
            streaming_pull_future = subscriber_client.subscribe(
                subscription_path, callback=callback_xmark
            )
        if subscription == "cloud-data-sub":
            streaming_pull_future = subscriber_client.subscribe(
                subscription_path, callback=callback_cloud
            )
        if subscription == "injective-sub":
            streaming_pull_future = subscriber_client.subscribe(
                subscription_path, callback=callback_inj
            )
        # Keep the function running to continue processing messages
        await streaming_pull_future.result()