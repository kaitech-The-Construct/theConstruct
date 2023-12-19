
# Callbacks for subscriptions

import requests

# Xmark Resource Data
def callback_xmark(message):
    try:
        # Process the URL from the received message
        url = message.data.decode("utf-8")
        # Call Cloud Function
        process_url_with_cloud_function(url=url, name="data-processor-xmark-xaoktxu34q-uw")
        message.ack()
        print(f"Processed message from Pub/Sub. Link: {url}")
        
    except Exception as e:
        url = message.data.decode("utf-8")
        print(f"Error processing message: {str(e)}. Link: {url}")


# Cloud Data
def callback_cloud(message):
    try:
        # Process the URL from the received message
        url = message.data.decode("utf-8")
        # Call Cloud Function
        process_url_with_cloud_function(url=url, name="data-processor-xmark-xaoktxu34q-uw")
        message.ack()
        print(f"Processed message from Pub/Sub. Link: {url}")
        
    except Exception as e:
        url = message.data.decode("utf-8")
        print(f"Error processing message: {str(e)}. Link: {url}")

# Injective Data
def callback_inj(message):
    try:
        # Process the URL from the received message
        url = message.data.decode("utf-8")
        # Call Cloud Function
        process_url_with_cloud_function(url=url, name="data-processor-injective-xaoktxu34q-uc")
        message.ack()
        print(f"Processed message from Pub/Sub. Link: {url}")
    except Exception as e:
        url = message.data.decode("utf-8")
        print(f"Error processing message: {str(e)}. Link: {url}")


# Process url by calling appropriate cloud function         
def process_url_with_cloud_function(url, name):

    # Define the Cloud Function URL
    cloud_function_url = f"https://{name}.a.run.app/processUrl"

    # Define the input data as a dictionary
    data = {
        "url": url
    }

    try:
        # Send a POST request to the Cloud Function
        response = requests.post(cloud_function_url, json=data)

        # Check the response
        if response.status_code == 200:
            # Request was successful
            # result = response.json()
            return response
        else:
            # Request encountered an error
            print(f"Error {response.status_code}: {response.text}")
            return {"error": f"Error {response.status_code}: {response.text}"}
    except Exception as e:
        # Handle any exceptions that may occur during the request
        return {"error": f"An error occurred: {str(e)}"}
    