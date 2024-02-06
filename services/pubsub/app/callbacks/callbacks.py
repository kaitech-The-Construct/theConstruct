
# Callbacks for subscriptions
import requests


def callback_inj(message):
    """
    Callback for transaction messages
    """
    try:
        # Process transaction messages
        transaction_data = message.data.decode("utf-8")
        process_transaction(transaction_data)
        message.ack()
        print(f"Processed Injective transaction data.")
    except Exception as e:
        print(f"Error processing Injective transaction data: {str(e)}")