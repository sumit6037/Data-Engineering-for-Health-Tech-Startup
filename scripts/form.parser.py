import pandas as pd
from google.cloud import documentai_v1 as documentai
from google.cloud import storage
from google.cloud import bigquery
import pandas_gbq


def online_process(
    project_id: str,
    location: str,
    processor_id: str,
    gcs_file_path: str,
    mime_type: str,
) -> documentai.Document:
    """
    Processes a document using the Document AI Online Processing API from GCS.
    """
    opts = {"api_endpoint": f"{location}-documentai.googleapis.com"}

    # Instantiates a client
    documentai_client = documentai.DocumentProcessorServiceClient(client_options=opts)

    # The full resource name of the processor
    resource_name = documentai_client.processor_path(project_id, location, processor_id)

    # Configure the GCS document as input
    gcs_document = documentai.GcsDocument(gcs_uri=gcs_file_path, mime_type=mime_type)
    input_config = documentai.RawDocument(content=gcs_document, mime_type=mime_type)

    # Configure the process request
    request = documentai.ProcessRequest(name=resource_name, raw_document=input_config)

    # Use the Document AI client to process the sample form
    result = documentai_client.process_document(request=request)

    return result.document


def trim_text(text: str):
    """
    Remove extra space characters from text (blank, newline, tab, etc.)
    """
    return text.strip().replace("\n", " ")


def download_file_from_gcs(bucket_name: str, source_blob_name: str, destination_file_name: str):
    """
    Downloads a file from Google Cloud Storage.
    """
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(source_blob_name)
    blob.download_to_filename(destination_file_name)
    print(f"Downloaded {source_blob_name} from bucket {bucket_name} to {destination_file_name}.")


def upload_to_bigquery(df: pd.DataFrame, project_id: str, dataset_id: str, table_id: str):
    """
    Ingests the Pandas DataFrame into BigQuery.
    """
    table_full_id = f"{project_id}.{dataset_id}.{table_id}"

    pandas_gbq.to_gbq(
        df,
        table_full_id,
        project_id=project_id,
        if_exists="replace",  # Change to 'append' if you want to append data
    )
    print(f"Dataframe uploaded to BigQuery table {table_full_id}.")


PROJECT_ID = "YOUR_PROJECT_ID"
LOCATION = "YOUR_PROJECT_LOCATION"  # Format is 'us' or 'eu'
PROCESSOR_ID = "FORM_PARSER_ID"  # Create processor in Cloud Console
BUCKET_NAME = "YOUR_BUCKET_NAME"
SOURCE_BLOB_NAME = "intake-form.pdf"  # The path to your PDF in GCS
LOCAL_FILE_PATH = "intake-form.pdf"
MIME_TYPE = "application/pdf"

# Download the PDF file from the GCS bucket
download_file_from_gcs(BUCKET_NAME, SOURCE_BLOB_NAME, LOCAL_FILE_PATH)

# Process the document using Document AI
document = online_process(
    project_id=PROJECT_ID,
    location=LOCATION,
    processor_id=PROCESSOR_ID,
    gcs_file_path=f"gs://{BUCKET_NAME}/{SOURCE_BLOB_NAME}",
    mime_type=MIME_TYPE,
)

# Extract fields and confidence from the document
names = []
name_confidence = []
values = []
value_confidence = []

for page in document.pages:
    for field in page.form_fields:
        # Get the extracted field names and values
        names.append(trim_text(field.field_name.text_anchor.content))
        name_confidence.append(field.field_name.confidence)

        values.append(trim_text(field.field_value.text_anchor.content))
        value_confidence.append(field.field_value.confidence)

# Create a Pandas Dataframe
df = pd.DataFrame(
    {
        "Field Name": names,
        "Field Name Confidence": name_confidence,
        "Field Value": values,
        "Field Value Confidence": value_confidence,
    }
)

print(df)

# Upload the dataframe to BigQuery
DATASET_ID = "your_dataset_id"
TABLE_ID = "your_table_id"
upload_to_bigquery(df, project_id=PROJECT_ID, dataset_id=DATASET_ID, table_id=TABLE_ID)

