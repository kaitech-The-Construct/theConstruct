from google.cloud import firestore


# Initialize Firestore client
db = firestore.Client()


def write_wallet_address_to_firestore(response):
    """Writes a wallet address to Firestore.

    Args:
        response (dict): The response from the wallet service.

    Returns:
        str: The custom document ID.
    """
    try:
        # Create a reference to the "test_task_events" collection
        collection_ref = db.collection("users")

        # Convert the TaskEvent object to a JSON string
        data = response.dict()

        # Generate a custom document ID
        doc_ref = collection_ref.document()

        # Update the document with the generated ID

        doc_ref.set({"wallet_address": data, "timestamp": firestore.SERVER_TIMESTAMP})
        # Return the custom document ID
        return doc_ref.id

    except Exception as e:
        # Handle any errors that occur during the Firestore operation
        print(f"Error writing to Firestore: {e}")
        return None
    finally:
        # Close the Firestore client
        db.close()


def write_data_to_firestore(response):
    """Writes data to Firestore.

    Args:
        response (dict): The response from the task service.

    Returns:
        str: The custom document ID.
    """
    try:
        # Create a reference to the "test_task_events" collection
        collection_ref = db.collection("test_events")

        # Convert the TaskEvent object to a JSON string
        data = response.dict()

        # Generate a custom document ID
        doc_ref = collection_ref.document()

        # Update the document with the generated ID
        doc_ref.set(data)

        doc_ref.update(
            {"event_id": doc_ref.id, "timestamp": firestore.SERVER_TIMESTAMP}
        )
        # Return the custom document ID
        return doc_ref.id

    except Exception as e:
        # Handle any errors that occur during the Firestore operation
        print(f"Error writing to Firestore: {e}")
        return None
    finally:
        # Close the Firestore client
        db.close()
