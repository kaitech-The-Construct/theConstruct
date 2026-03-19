import os
from google.cloud import pubsub_v1
from services.pubsub.config.config import settings
from callbacks.callbacks import callback_cloud, callback_xmark, callback_inj



async def process_pubsub_messages():

    """Processes Pub/Sub messages from multiple subscriptions.

    Args:
        subscriptions (list): A list of Pub/Sub subscription names.
    """

    subscriber_client = pubsub_v1.SubscriberClient()
    project_id = settings.project_id
    subscriptions = settings.subscriptions

    # Subscribe to the Pub/Sub subscriptions and start listening
    for subscription in subscriptions:
        subscription_path = subscriber_client.subscription_path(
            f"{project_id}", subscription
        )
        if subscription == "injective-sub":
            streaming_pull_future = subscriber_client.subscribe(
                subscription_path, callback=callback_inj
            )
        # Keep the function running to continue processing messages
        try:
            # Process messages concurrently using an asyncio event loop
            await streaming_pull_future.result()
        except Exception as e:
            print(f"Exception while processing subscription {subscription}: {str(e)}")