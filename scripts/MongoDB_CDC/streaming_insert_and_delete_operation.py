import threading
import pymongo
from google.cloud import pubsub_v1
import avro.schema
import avro.io
import json
import time
import io
import datetime
from bson import ObjectId
from google.api_core.exceptions import NotFound
from google.pubsub_v1.types import Encoding

# Custom JSON Encoder to handle ObjectId and datetime
class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return str(obj)
        return super(CustomEncoder, self).default(obj)

# Replace these placeholders with your actual values
MONGODB_URI = '<YOUR_MONGODB_URI>'
PUB_SUB_TOPIC = '<YOUR_PUB_SUB_TOPIC>'
AVSC_FILE = '/path/to/document-message.json'  # replace with the path to your Avro schema file

# Initialize MongoDB client
client = pymongo.MongoClient(MONGODB_URI)
db = client.get_database("<YOUR_DB_NAME>")
collection = db.get_collection("<YOUR_COLLECTION_NAME>")

# Initialize Pub/Sub client
publisher_client = pubsub_v1.PublisherClient()
topic_path = publisher_client.topic_path("<YOUR_PROJECT_ID>", PUB_SUB_TOPIC)

# Function to publish a document as a message to Pub/Sub
def publish_document_as_message(document, operation_type):
    avro_schema = avro.schema.parse(open(AVSC_FILE).read())
    writer = avro.io.DatumWriter(avro_schema)
    bytes_io = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_io)

    # Prepare the message data
    message_data = {
        "id": str(document["_id"]),
        "source_data": json.dumps(document, cls=CustomEncoder),
        "Timestamp": str(int(time.time())),
        "Operation": operation_type
    }

    # Get the topic encoding type
    try:
        topic = publisher_client.get_topic(request={"topic": topic_path})
        encoding = topic.schema_settings.encoding
    except NotFound:
        print(f"{PUB_SUB_TOPIC} not found.")
        exit(1)

    # Encode the data based on encoding type
    if encoding == Encoding.BINARY:
        writer.write(message_data, encoder)
        data = bytes_io.getvalue()
    elif encoding == Encoding.JSON:
        data_str = json.dumps(message_data)
        data = data_str.encode("utf-8")
    else:
        print(f"No encoding specified in {topic_path}. Abort.")
        exit(1)

    # Publish the message
    future = publisher_client.publish(topic_path, data)
    print(f"Published message ID: {future.result()}")

# Function to publish a delete operation to Pub/Sub
def publish_delete_as_message(document_id, operation_type):
    avro_schema = avro.schema.parse(open(AVSC_FILE).read())
    writer = avro.io.DatumWriter(avro_schema)
    bytes_io = io.BytesIO()
    encoder = avro.io.BinaryEncoder(bytes_io)

    document_id_str = str(document_id)
    delete_message_data = {
        "id": document_id_str,
        "source_data": "",
        "Timestamp": str(int(time.time())),
        "Operation": operation_type
    }

    # Get the topic encoding type
    try:
        topic = publisher_client.get_topic(request={"topic": topic_path})
        encoding = topic.schema_settings.encoding
    except NotFound:
        print(f"{PUB_SUB_TOPIC} not found.")
        exit(1)

    # Encode the data based on encoding type
    if encoding == Encoding.BINARY:
        writer.write(delete_message_data, encoder)
        data = bytes_io.getvalue()
    elif encoding == Encoding.JSON:
        data_str = json.dumps(delete_message_data)
        data = data_str.encode("utf-8")
    else:
        print(f"No encoding specified in {topic_path}. Abort.")
        exit(1)

    # Publish the delete message
    future = publisher_client.publish(topic_path, data)
    print(f"Published delete message ID: {future.result()}")

# Function to monitor MongoDB for inserts
def monitor_collection_for_inserts():
    with collection.watch([{"$match": {"operationType": "insert"}}]) as stream:
        print("Monitoring for inserts...")
        for change in stream:
            document = change["fullDocument"]
            publish_document_as_message(document, operation_type="insert")

# Function to monitor MongoDB for deletes
def monitor_collection_for_deletes():
    with collection.watch([{"$match": {"operationType": "delete"}}]) as stream:
        print("Monitoring for deletes...")
        for change in stream:
            document_id = change["documentKey"]["_id"]
            publish_delete_as_message(document_id, operation_type="delete")

# Close the MongoDB connection after a specified interval
def close_change_stream(time_interval_ms=60000):
    time.sleep(time_interval_ms / 1000)
    client.close()

if __name__ == "__main__":
    # Create threads for monitoring inserts and deletes
    inserts_thread = threading.Thread(target=monitor_collection_for_inserts)
    deletes_thread = threading.Thread(target=monitor_collection_for_deletes)

    # Start the threads
    inserts_thread.start()
    deletes_thread.start()

    # Wait for both threads to finish
    inserts_thread.join()
    deletes_thread.join()

    # Close the MongoDB change stream after a specified time interval
    close_change_stream()
