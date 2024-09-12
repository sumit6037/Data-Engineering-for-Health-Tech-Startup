
# MongoDB Change Stream to BigQuery Pipeline

This project sets up a real-time data pipeline between a MongoDB collection and BigQuery using Google Cloud Pub/Sub. The pipeline listens for changes (inserts and deletes) in a MongoDB collection, publishes these changes to a Pub/Sub topic, and ingests them into BigQuery. The changes are serialized using an Avro schema for efficient message passing.

## Key Components

- **MongoDB Change Streams**: Monitors inserts and deletes in a MongoDB collection.
- **Google Cloud Pub/Sub**: Publishes changes to a Pub/Sub topic for real-time ingestion.
- **Avro Schema**: Used for efficient message serialization.
- **BigQuery**: Stores change events for further analysis and reporting.

## Step-by-Step Guide

### 1. Create a BigQuery Dataset

1. Navigate to **Google Cloud Console** and go to the BigQuery section.
2. **Create a new dataset** for storing the MongoDB change events.
3. **Add a new table** to your dataset with the following schema:

   | Field name   | Type   |
   |--------------|--------|
   | id           | STRING |
   | source_data  | STRING |
   | Timestamp    | STRING |

   This table will store raw MongoDB changes, including the document ID, the document content in JSON format, and a timestamp.

### 2. Configure Google Cloud Pub/Sub

#### Define a Pub/Sub Schema

1. In **Google Cloud Console**, navigate to **Pub/Sub**.
2. Click **Schemas** in the sidebar and then **Create Schema**.
3. Provide a schema name, such as `mdb-to-bq-schema`.
4. Select **Avro** as the schema type.
5. Define the schema fields to match the BigQuery table:

   ```json
   {
     "type": "record",
     "name": "MongoDBCDC",
     "fields": [
       {"name": "id", "type": "string"},
       {"name": "source_data", "type": "string"},
       {"name": "Timestamp", "type": "string"},
       {"name": "Operation", "type": "string"}
     ]
   }


#### Create a Pub/Sub Topic

1. From the **Pub/Sub** section, click **Topics**, then click **Create Topic**.
2. Name the topic, e.g., `MongoDBCDC`.
3. Enable **Use schema**, and select the schema you just created.
4. Click **Create Topic**.

#### Create a Subscription to Write to BigQuery

1. In the topic view, click **Create Subscription**.
2. Provide a subscription ID, e.g., `mdb-cdc`.
3. Set **Delivery Type** to **Write to BigQuery**.
4. Select the BigQuery dataset and table you created earlier.
5. Enable **Use topic schema** to ensure that the messages follow the defined schema.
